import os
import threading
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore_async, firestore
from google.cloud.firestore_v1 import Increment, ArrayUnion, ArrayRemove
from typing import Callable, List, Dict, Any, Optional

# Variable global para controlar la inicialización
_firebase_initialized = False

def initialize_firebase():
    """
    Inicializa Firebase de forma segura, evitando múltiples inicializaciones.
    """
    global _firebase_initialized
    
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
    
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener las variables de entorno
    private_key_id = os.getenv('PRIVATE_KEY_ID')
    private_key = os.getenv('PRIVATE_KEY')

    # Crear un diccionario con las credenciales necesarias
    cred_dict = {
        "type": "service_account",
        "project_id": "casino-virtual-7ddaa",
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": "firebase-adminsdk-fbsvc@casino-virtual-7ddaa.iam.gserviceaccount.com",
        "client_id": "104657042562380559855",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40casino-virtual-7ddaa.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    # Inicializar Firebase usando el diccionario de credenciales
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    _firebase_initialized = True

class Firestore:
    """
    Clase para gestionar operaciones de Firestore de manera asíncrona.
    """
    
    @staticmethod
    async def get_async_client():
        """
        Obtiene el cliente asíncrono de Firestore.
        """
        initialize_firebase()
        return firestore_async.client()
    
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
    def _print_dynamic_data(data, indent="", max_depth=3, current_depth=0):
        """
        Imprime datos de forma dinámica, adaptándose a cualquier estructura.
        
        Args:
            data: Los datos a imprimir (dict, list, o valor simple)
            indent: Indentación actual
            max_depth: Profundidad máxima para evitar recursión infinita
            current_depth: Profundidad actual
        """
        if current_depth > max_depth:
            print(f"{indent}[Datos muy profundos, truncados...]")
            return
        
        if isinstance(data, dict):
            # Determinar el tipo de documento dinámicamente
            doc_type = Firestore._detect_document_type(data)
            if doc_type and current_depth == 0:
                print(f"{indent}🏷️  Tipo detectado: {doc_type}")
            
            for key, value in data.items():
                icon = Firestore._get_field_icon(key, value)
                
                if isinstance(value, dict):
                    print(f"{indent}{icon} {key}:")
                    Firestore._print_dynamic_data(value, indent + "   ", max_depth, current_depth + 1)
                elif isinstance(value, list):
                    print(f"{indent}{icon} {key}: [{len(value)} elementos]")
                    if len(value) <= 5:  # Mostrar solo si hay pocos elementos
                        for i, item in enumerate(value):
                            if isinstance(item, (dict, list)):
                                print(f"{indent}   [{i}]:")
                                Firestore._print_dynamic_data(item, indent + "      ", max_depth, current_depth + 1)
                            else:
                                print(f"{indent}   [{i}] {item}")
                    else:
                        # Mostrar solo los primeros elementos
                        for i in range(3):
                            if isinstance(value[i], (dict, list)):
                                print(f"{indent}   [{i}]:")
                                Firestore._print_dynamic_data(value[i], indent + "      ", max_depth, current_depth + 1)
                            else:
                                print(f"{indent}   [{i}] {value[i]}")
                        print(f"{indent}   ... y {len(value) - 3} más")
                else:
                    # Valor simple
                    formatted_value = Firestore._format_value(value)
                    print(f"{indent}{icon} {key}: {formatted_value}")
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                print(f"{indent}[{i}]:")
                Firestore._print_dynamic_data(item, indent + "   ", max_depth, current_depth + 1)
        else:
            print(f"{indent}{Firestore._format_value(data)}")
    
    @staticmethod
    def _detect_document_type(data):
        """Detecta el tipo de documento basado en sus campos"""
        if not isinstance(data, dict):
            return None
        
        # Detectar diferentes tipos de documentos
        if 'juego' in data and 'jugadores' in data:
            return f"Sala de Juego - {data.get('juego', 'Desconocido')}"
        elif 'nombre' in data and 'email' in data:
            return "Usuario"
        elif 'partida_id' in data and 'movimiento' in data:
            return "Movimiento de Juego"
        elif 'cartas' in data or 'tablero' in data:
            return "Estado de Partida"
        elif 'timestamp' in data and 'evento' in data:
            return "Evento/Log"
        else:
            return "Documento Genérico"
    
    @staticmethod
    def _get_field_icon(field_name, value):
        """Obtiene un icono apropiado para el campo basado en su nombre y valor"""
        field_lower = field_name.lower()
        
        # Iconos basados en el nombre del campo
        if 'id' in field_lower:
            return "🆔"
        elif field_lower in ['juego', 'game', 'tipo_juego']:
            return "🎮"
        elif field_lower in ['jugadores', 'players', 'usuarios']:
            return "👥"
        elif field_lower in ['estado', 'status', 'state']:
            return "🎯"
        elif field_lower in ['turno', 'turn', 'turno_actual']:
            return "⏰"
        elif field_lower in ['fecha', 'timestamp', 'date', 'time', 'fecha_hora']:
            return "📅"
        elif field_lower in ['cartas', 'cards', 'mano']:
            return "🃏"
        elif field_lower in ['tablero', 'board', 'mesa']:
            return "🎲"
        elif field_lower in ['puntos', 'score', 'puntaje']:
            return "🏆"
        elif field_lower in ['dinero', 'money', 'coins', 'creditos']:
            return "💰"
        elif field_lower in ['nivel', 'level', 'rango']:
            return "⭐"
        elif field_lower in ['capacidad', 'max', 'limite']:
            return "📏"
        elif field_lower in ['activo', 'active', 'online']:
            return "🟢" if value else "🔴"
        elif field_lower in ['historial', 'history', 'log']:
            return "📚"
        elif isinstance(value, bool):
            return "✅" if value else "❌"
        elif isinstance(value, (int, float)) and value == 0:
            return "0️⃣"
        elif isinstance(value, list):
            return "📋"
        elif isinstance(value, dict):
            return "📁"
        else:
            return "📄"
    
    @staticmethod
    def _format_value(value):
        """Formatea un valor para mostrar de forma más legible"""
        if value is None:
            return "❌ None"
        elif isinstance(value, bool):
            return "✅ True" if value else "❌ False"
        elif isinstance(value, str) and len(value) > 50:
            return f'"{value[:47]}..."'
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return str(value)

    @staticmethod
    def add_realtime_listener(collection_name: str, document_id: str, callback: Callable, error_callback: Callable = None, test: bool = False):
        """
        Agrega un listener en tiempo real para un documento específico en Firestore.
        
        Args:
            collection_name (str): Nombre de la colección
            document_id (str): ID del documento a escuchar
            callback (Callable): Función que se ejecuta cuando hay cambios. Recibe (doc_snapshot, changes, read_time)
            error_callback (Callable, optional): Función que se ejecuta en caso de error
            
        Returns:
            function: Función para detener el listener
        """
        initialize_firebase()
        
        # Event para notificar al hilo principal
        callback_done = threading.Event()
        
        def on_snapshot(doc_snapshot, changes, read_time):
            """Callback interno que maneja los cambios del documento"""
            try:
                # Verificar si es una lista de documentos (error común)
                if isinstance(doc_snapshot, list):
                    print(f"⚠️  Advertencia: Se recibió una lista en lugar de un documento")
                    if doc_snapshot:
                        # Tomar el primer documento de la lista
                        doc_snapshot = doc_snapshot[0]
                    else:
                        callback(None, changes, read_time)
                        return
                
                # Procesar el documento individual
                if hasattr(doc_snapshot, 'exists') and doc_snapshot.exists:
                    print(f"📡 Cambio detectado en documento: {doc_snapshot.id}")
                    doc_data = doc_snapshot.to_dict()
                    doc_data['id'] = doc_snapshot.id
                    callback(doc_data, changes, read_time)
                    
                    if test:
                        if doc_data:
                            print("   📊 Datos detallados del documento:")
                            Firestore._print_dynamic_data(doc_data, indent="      ")
                        
                else:
                    print(f"📡 Documento {document_id} no existe o fue eliminado")
                    callback(None, changes, read_time)
                    
            except Exception as e:
                print(f"❌ Error en listener: {e}")
                if error_callback:
                    error_callback(e)
        
        # Usar cliente SÍNCRONO para listeners
        db = firestore.client()  # Cliente síncrono para listeners
        doc_ref = db.collection(collection_name).document(document_id)
        
        # Iniciar el listener
        doc_watch = doc_ref.on_snapshot(on_snapshot)
        
        print(f"🎧 Listener iniciado para {collection_name}/{document_id}")
        
        # Retornar función para detener el listener
        return doc_watch.unsubscribe

# Funciones globales para mantener compatibilidad con código existente
def add_realtime_listener(collection_name: str, document_id: str, callback: Callable, error_callback: Callable = None, test: bool = False):
    """Agrega un listener en tiempo real para un documento."""
    return Firestore.add_realtime_listener(collection_name, document_id, callback, error_callback, test)
