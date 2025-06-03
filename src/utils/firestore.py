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

# Inicializar Firebase al importar el módulo
initialize_firebase()

class Firestore:
    """
    Clase para manejar las operaciones con Firestore.
    """
    @staticmethod
    async def get_async_client():
        """
        Obtiene el cliente asíncrono de Firestore.

        Returns:
            firestore_async.client: Cliente asíncrono de Firestore.
        """
        db = firestore_async.client()
        return db

    @staticmethod
    async def add_data(collection_name: str, data: dict) -> str:
        """
        Agrega un documento a una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            data (dict): Datos a agregar.

<<<<<<< HEAD
        Returns:
            str: ID del documento agregado.
        """
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document()
        await doc_ref.set(data)
        return doc_ref.id
=======
async def get_data(collection_name: str, id: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene un documento de una colección en Firestore.
>>>>>>> aa13894fdefe2996a091058a08dc8658054cd535

    @staticmethod
    async def add_data_with_id(collection_name: str, data: dict, id: str) -> str:
        """
        Agrega un documento con un ID específico a una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            data (dict): Datos a agregar.
            id (str): ID del documento.

<<<<<<< HEAD
        Returns:
            str: ID del documento agregado.
        """
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document(id)
        await doc_ref.set(data)
        return doc_ref.id
=======
async def get_collection_data(collection_name: str) -> List[Optional[Dict[str, Any]]]:
    """
    Obtiene todos los documentos de una colección en Firestore.
>>>>>>> aa13894fdefe2996a091058a08dc8658054cd535

    @staticmethod
    async def get_data(collection_name: str, id: str) -> dict:
        """
        Obtiene un documento de una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.
            id (str): ID del documento.

        Returns:
            dict: Datos del documento.
        """
        db = await Firestore.get_async_client()
        doc_ref = db.collection(collection_name).document(id)
        doc = await doc_ref.get()
        return doc.to_dict()

    @staticmethod
    async def get_collection_data(collection_name: str) -> list:
        """
        Obtiene todos los documentos de una colección en Firestore.

        Args:
            collection_name (str): Nombre de la colección.

        Returns:
            list[dict]: Lista de documentos en la colección.
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

<<<<<<< HEAD
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
def ingrement(num: int):
    return firestore.Increment(num)
=======
def increment(num: float):
    return Increment(num)
>>>>>>> aa13894fdefe2996a091058a08dc8658054cd535

def decrement(num: float):
    return Increment(-num)

def array_union(array: list):
    return ArrayUnion(array)

def array_remove(array: list):
<<<<<<< HEAD
    return firestore.ArrayRemove(array)

# Funciones globales para mantener compatibilidad con código existente
async def get_async_firestore_client():
    return await Firestore.get_async_client()

async def add_data(collection_name: str, data: dict) -> str:
    return await Firestore.add_data(collection_name, data)

async def add_data_with_id(collection_name: str, data: dict, id: str) -> str:
    return await Firestore.add_data_with_id(collection_name, data, id)

async def get_data(collection_name: str, id: str) -> dict:
    return await Firestore.get_data(collection_name, id)

async def get_collection_data(collection_name: str) -> list:
    return await Firestore.get_collection_data(collection_name)

async def update_data(collection_name: str, id: str, data: dict) -> str:
    return await Firestore.update_data(collection_name, id, data)

async def delete_data(collection_name: str, id: str) -> str:
    return await Firestore.delete_data(collection_name, id)
=======
    return ArrayRemove(array)
>>>>>>> aa13894fdefe2996a091058a08dc8658054cd535
