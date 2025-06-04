import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore_async, firestore
from google.cloud.firestore_v1 import Increment, ArrayUnion, ArrayRemove
from typing import List, Dict, Any, Optional

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
        doc_ref = db.collection(collection_name).document()
        await doc_ref.set(data)
        return doc_ref.id

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
        docs = [doc.to_dict() async for doc in docs_ref]
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
