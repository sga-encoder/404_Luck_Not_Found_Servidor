import os
import threading
import time
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore_async, firestore
from google.cloud.firestore_v1 import Increment, ArrayUnion, ArrayRemove
from typing import Callable, List, Dict, Any, Optional
from .pretty_printer import PrettyPrinter

# Variable global para controlar la inicialización
_firebase_initialized = False
_initialization_lock = threading.Lock()

async def retry_with_backoff(func, max_retries=3, initial_delay=1.0):
    """
    Ejecuta una función con reintentos automáticos y backoff exponencial.
    Útil para manejar errores temporales de JWT o conectividad.
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            error_msg = str(e).lower()
            
            # Verificar si es un error que vale la pena reintentar
            if any(keyword in error_msg for keyword in ['jwt', 'token', 'signature', 'expired', 'timeout', 'connection']):
                if attempt < max_retries - 1:  # No hacer delay en el último intento
                    delay = initial_delay * (2 ** attempt)  # Backoff exponencial
                    print(f"🔄 Intento {attempt + 1} falló ({type(e).__name__}), reintentando en {delay:.1f}s...")
                    time.sleep(delay)
                    continue
            
            # Si no es un error reinentable o ya agotamos los intentos
            raise e
    
    # Si llegamos aquí, todos los intentos fallaron
    raise last_exception

def initialize_firebase():
    """
    Inicializa Firebase de forma segura, evitando múltiples inicializaciones.
    Incluye manejo robusto de errores JWT.
    """
    global _firebase_initialized
    
    with _initialization_lock:
        if _firebase_initialized:
            return
        
        try:
            # Verificar si ya hay una app inicializada
            firebase_admin.get_app()
            _firebase_initialized = True
            return
        except ValueError:
            # No hay app inicializada, proceder con la inicialización
            pass

        # Buscar el archivo JSON en la raíz del proyecto
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        json_path = os.path.join(project_root, 'lucknotfound-e5006-firebase-adminsdk-fbsvc-82f498eb10-clean.json')
        
        print(f"🔍 Buscando archivo JSON en: {json_path}")
        
        if not os.path.exists(json_path):
            print(f"❌ Archivo JSON no encontrado en: {json_path}")
            print("📂 Contenido del directorio raíz:")
            try:
                for item in os.listdir(project_root):
                    if item.endswith('.json'):
                        print(f"   - {item}")
            except Exception as e:
                print(f"   Error listando directorio: {e}")
            
            raise FileNotFoundError(f"No se pudo encontrar el archivo de credenciales JSON")

        try:
            print("📁 Archivo JSON encontrado, validando...")
            
            # Leer y validar el archivo JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Validar campos esenciales
            required_fields = ['project_id', 'private_key', 'client_email', 'type']
            for field in required_fields:
                if field not in json_data:
                    raise ValueError(f"Campo requerido '{field}' no encontrado en el archivo JSON")
            
            # Validar formato de clave privada
            private_key = json_data['private_key']
            if not private_key.startswith('-----BEGIN PRIVATE KEY-----'):
                raise ValueError("Formato de clave privada incorrecto")
            
            print(f"📋 Project ID: {json_data['project_id']}")
            print(f"📧 Client Email: {json_data['client_email']}")
            
            # Configurar opciones específicas para evitar problemas JWT
            firebase_options = {
                'projectId': json_data['project_id'],
                'databaseURL': f"https://{json_data['project_id']}-default-rtdb.firebaseio.com/"
            }
            
            # Inicializar Firebase con configuración específica
            cred = credentials.Certificate(json_path)
            firebase_admin.initialize_app(cred, options=firebase_options)
            
            _firebase_initialized = True
            print("✅ Firebase inicializado correctamente")
            
            # Pequeña pausa para asegurar la inicialización completa
            time.sleep(0.1)
            
        except json.JSONDecodeError as e:
            print(f"❌ Error de formato JSON: {e}")
            raise
        except ValueError as e:
            print(f"❌ Error de validación: {e}")
            raise
        except Exception as e:
            print(f"❌ Error inicializando Firebase: {e}")
            print(f"   Tipo de error: {type(e).__name__}")
            
            # Si es un error JWT, proporcionar información específica
            if "Invalid JWT Signature" in str(e) or "JWT" in str(e):
                print("🎯 Error JWT detectado. Posibles soluciones:")
                print("   1. Regenerar las credenciales desde Firebase Console")
                print("   2. Verificar que el reloj del sistema esté sincronizado")
                print("   3. Asegurar conectividad a internet estable")
                print("   4. Verificar que el proyecto Firebase esté activo")
            
            raise

class Firestore:
    """
    Clase para gestionar operaciones de Firestore de manera asíncrona.
    """
    
    @staticmethod
    async def get_async_client():
        """
        Obtiene el cliente asíncrono de Firestore con reintentos automáticos.
        """
        async def _get_client():
            initialize_firebase()
            return firestore_async.client()
        
        # Usar reintentos para manejar errores temporales de JWT
        return await retry_with_backoff(_get_client)
    
    @staticmethod
    async def add_data(collection_name: str, data: dict) -> str:
        """
        Agrega un documento a una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            data (dict): Datos a agregar.

        Returns:
            str: ID del documento agregado.
        """
        db = await Firestore.get_async_client()
        doc_ref = await db.collection(collection_name).add(data)
        return doc_ref[1].id 

    @staticmethod
    async def add_data_with_id(collection_name: str, data: dict, id: str) -> str:
        """
        Agrega un documento con un ID específico a una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            data (dict): Datos a agregar.
            id (str): ID del documento.

        Returns:
            str: ID del documento agregado.
        """
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document(id)
        await doc_ref.set(data)
        return doc_ref.id

    @staticmethod
    async def get_data(collection_name: str, id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un documento de una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            id (str): ID del documento.

        Returns:
            Optional[Dict[str, Any]]: Datos del documento o None si no existe.
        """
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document(id)
        doc = await doc_ref.get()
        return doc.to_dict() if doc.exists else None

    @staticmethod
    async def get_collection_data(collection_name: str) -> List[Optional[Dict[str, Any]]]:
        """
        Obtiene todos los documentos de una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.

        Returns:
            List[Optional[Dict[str, Any]]]: Lista de documentos.
        """
        db = await Firestore.get_async_client()
        docs_ref = db.collection(collection_name).stream()
        docs = []
        async for doc in docs_ref:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            docs.append(doc_data)
        return docs
        
    @staticmethod
    async def update_data(collection_name: str, id: str, data: dict) -> str:
        """
        Actualiza un documento en una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            id (str): ID del documento.
            data (dict): Datos a actualizar.

        Returns:
            str: ID del documento actualizado.
        """
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document(id)
        await doc_ref.update(data)
        return doc_ref.id
        
    @staticmethod
    async def delete_data(collection_name: str, id: str) -> str:
        """
        Elimina un documento de una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            id (str): ID del documento.

        Returns:
            str: ID del documento eliminado.
        """        
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document(id)
        await doc_ref.delete()
        return doc_ref.id    
    @staticmethod
    def add_realtime_listener(collection_name: str, document_id: str, callback, error_callback, test: bool = False):
        """
        Agrega un listener en tiempo real para un documento específico en Firestore.

        Args:
            collection_name (str): Nombre de la colección
            document_id (str): ID del documento a escuchar
            callback (Callable): Función que se ejecuta cuando hay cambios. Recibe (doc_data, changes, read_time, related_data)
                - doc_data: Diccionario con los datos del documento principal (o None si no existe/eliminado)
                - changes: Lista de cambios (puede ser vacía o contener solo un cambio para listener de documento)
                - read_time: Tiempo de lectura del snapshot
                - related_data: Diccionario donde la clave es el campo_en_documento (ej: 'jugadores')
                y el valor es una lista de diccionarios con los datos completos de los documentos relacionados.
            error_callback (Callable, optional): Función que se ejecuta en caso de error. Recibe (exception)
            test (bool): Si es True, imprime información de debug
            related_collections (List[List[str]], optional): Lista de colecciones relacionadas a obtener.
                Formato: [['coleccion_destino', 'campo_en_documento']]
                Ejemplo: [['usuarios', 'jugadores']] obtiene datos de 'usuarios' usando IDs del campo 'jugadores'
                Espera que el campo 'campo_en_documento' sea una lista de IDs (strings).

        Returns:
            function: Función para detener el listener (la función unsubscribe)
        """
        initialize_firebase() # Asegura que Firebase esté inicializado

        # Usar cliente SÍNCRONO para listeners (como ya lo tenías)
        db = firestore.client()

        def on_snapshot(doc_snapshot, changes, read_time):
            """
            Callback interno que maneja los cambios del documento principal
            y carga datos de las colecciones relacionadas especificadas.
            """
            try:
                # Inicializamos el diccionario para almacenar los datos relacionados
                # Siempre lo inicializamos, aunque esté vacío si no hay related_collections
                related_data: Dict[str, List[Dict[str, Any]]] = {}

                # Verificar si es una lista de documentos (menos común para listener de 1 doc)
                if isinstance(doc_snapshot, list):
                    print(f"⚠️  Advertencia: Se recibió una lista ({len(doc_snapshot)} items) en lugar de un documento para {collection_name}/{document_id}. Procesando el primero si existe.")
                    if doc_snapshot:
                        # Tomar el primer documento de la lista si no está vacía
                        doc_snapshot = doc_snapshot[0]
                    else:
                        # Si la lista está vacía o es inválida, notificar el callback con None
                        if callback:
                            # Asegúrate de pasar un diccionario vacío para related_data si no hay documento principal
                            callback(None, changes, read_time, related_data)
                        return # Salir si no hay documento principal válido

                # Procesar el documento individual
                if hasattr(doc_snapshot, 'exists') and doc_snapshot.exists:
                    print(f"📡 Cambio detectado en documento: {doc_snapshot.id}")
                    doc_data = doc_snapshot.to_dict()
                    doc_data['id'] = doc_snapshot.id # Añade el ID del documento principal
                
                    # Llamar al callback del usuario con los datos del documento principal
                    # y los datos relacionados que acabamos de obtener
                    if callback:
                        # Pasa doc_data (el diccionario) y related_data
                        callback(doc_data, changes, read_time, related_data)

                    # --- Código existente: Imprimir detalles si está en modo test ---
                    if test:
                        print("   📊 Datos detallados del documento (incluye datos relacionados):")
                        # Combinamos doc_data y related_data para una impresión completa si test es True
                        full_output_data = {**doc_data, **{"_related_data": related_data}} # Usa un prefijo para _related_data para claridad

                        # Asegúrate de tener PrettyPrinter importado y configurado o usa json
                        if 'PrettyPrinter' in globals() or 'PrettyPrinter' in locals():
                            PrettyPrinter.print_dynamic_data(full_output_data, indent="      ")
                        else:
                            # Impresión alternativa si PrettyPrinter no está disponible
                            import json
                            try:
                                print(json.dumps(full_output_data, indent=6))
                            except TypeError as e:
                                print(f"    Error imprimiendo datos con json: {e}. Aquí están los datos sin formato:")
                            print(full_output_data)


                else:
                    # --- Código existente: Documento principal no existe o fue eliminado ---
                    print(f"📡 Documento {collection_name}/{document_id} no existe o fue eliminado")
                    if callback:
                        # Pasa None para indicar que el documento no existe.
                        # Pasa related_data (que estará vacío) también.
                        callback(None, changes, read_time, related_data) # Pasamos related_data vacío

            except Exception as e:
                # --- Código existente: Manejar errores generales del listener ---
                print(f"❌ Error general en listener para {collection_name}/{document_id}: {e}")
                if error_callback:
                    error_callback(e)

        # Obtener la referencia del documento
        doc_ref = db.collection(collection_name).document(document_id)

        # Iniciar el listener. La función on_snapshot definida arriba es el callback.
        doc_watch = doc_ref.on_snapshot(on_snapshot)
        print(f"🎧 Listener iniciado para {collection_name}/{document_id}")

        # Retornar función para detener el listener
        return doc_watch.unsubscribe

    @staticmethod
    def add_collection_listener(collection_name: str, callback: Callable, query_filter: Dict = None, error_callback: Callable = None):
        """
        Agrega un listener en tiempo real para una colección completa en Firestore.
        
        Args:
            collection_name (str): Nombre de la colección
            callback (Callable): Función que se ejecuta cuando hay cambios
            query_filter (Dict, optional): Filtros para la consulta (ej: {'estado': 'activa'})
            error_callback (Callable, optional): Función que se ejecuta en caso de error
            
        Returns:
            function: Función para detener el listener
        """
        initialize_firebase()
        
        callback_done = threading.Event()
        
        def on_snapshot(col_snapshot, changes, read_time):
            """Callback interno que maneja los cambios de la colección"""
            try:
                docs_data = []
                for doc in col_snapshot:
                    doc_data = doc.to_dict()
                    doc_data['id'] = doc.id  # Agregar el ID al documento
                    docs_data.append(doc_data)
                
                print(f"📡 Cambios detectados en colección {collection_name}: {len(changes)} cambios")
                
                # Llamar al callback del usuario
                callback(docs_data, changes, read_time)
                
            except Exception as e:
                print(f"❌ Error en listener de colección: {e}")
                if error_callback:
                    error_callback(e)
            finally:
                callback_done.set()        # Crear referencia a la colección
        db = firestore.client()
        collection_ref = db.collection(collection_name)
        
        # Aplicar filtros si se proporcionan
        if query_filter:
            for field, value in query_filter.items():
                collection_ref = collection_ref.where(field, '==', value)
        
        # Iniciar el listener
        col_watch = collection_ref.on_snapshot(on_snapshot)
        
        print(f"🎧 Listener de colección iniciado para {collection_name}")
        
        # Retornar función para detener el listener
        return col_watch.unsubscribe

# Funciones de ayuda para operaciones de Firestore
def increment(num: float):
    """Incrementa un valor numérico en Firestore."""
    return Increment(num)

def decrement(num: float):
    """Decrementa un valor numérico en Firestore."""
    return Increment(-num)

def array_union(array: list):
    """Añade elementos a un array sin duplicados."""
    return ArrayUnion(array)

def array_remove(array: list):
    """Remueve elementos de un array."""
    return ArrayRemove(array)

# Funciones globales para mantener compatibilidad con código existente
async def get_async_firestore_client():
    """Obtiene el cliente asíncrono de Firestore."""
    return await Firestore.get_async_client()

async def add_data(collection_name: str, data: dict) -> str:
    """Agrega un documento a una colección."""
    return await Firestore.add_data(collection_name, data)

async def add_data_with_id(collection_name: str, data: dict, id: str) -> str:
    """Agrega un documento con ID específico."""
    return await Firestore.add_data_with_id(collection_name, data, id)

async def get_data(collection_name: str, id: str) -> Optional[Dict[str, Any]]:
    """Obtiene un documento por ID."""
    return await Firestore.get_data(collection_name, id)

async def get_collection_data(collection_name: str) -> List[Optional[Dict[str, Any]]]:
    """Obtiene todos los documentos de una colección."""
    return await Firestore.get_collection_data(collection_name)

async def update_data(collection_name: str, id: str, data: dict) -> str:
    """Actualiza un documento."""
    return await Firestore.update_data(collection_name, id, data)

async def delete_data(collection_name: str, id: str) -> str:
    """Elimina un documento."""
    return await Firestore.delete_data(collection_name, id)

# Funciones de listener en tiempo real
def add_realtime_listener(collection_name: str, document_id: str, callback: Callable, error_callback: Callable = None, test: bool = False):
    """Agrega un listener en tiempo real para un documento."""
    return Firestore.add_realtime_listener(collection_name, document_id, callback, error_callback, test)

def add_collection_listener(collection_name: str, callback: Callable, query_filter: Dict = None, error_callback: Callable = None ):
    """Agrega un listener en tiempo real para una colección."""
    return Firestore.add_collection_listener(collection_name, callback, query_filter, error_callback)
