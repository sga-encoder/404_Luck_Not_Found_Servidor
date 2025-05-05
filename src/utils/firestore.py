import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore_async

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

async def get_async_firestore_client():
    """
    Obtiene el cliente asíncrono de Firestore.

    Returns:
        firestore_async.client: Cliente asíncrono de Firestore.
    """
    db = firestore_async.client()
    return db

async def add_data(collection_name: str, data: dict) -> str:
    """
    Agrega un documento a una colección en Firestore.

    Args:
        collection_name (str): Nombre de la colección.
        data (dict): Datos a agregar.

    Returns:
        str: ID del documento agregado.
    """
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document()
    await doc_ref.set(data)
    return doc_ref.id

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
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    await doc_ref.set(data)
    return doc_ref.id

async def get_data(collection_name: str, id: str) -> dict:
    """
    Obtiene un documento de una colección en Firestore.

    Args:
        collection_name (str): Nombre de la colección.
        id (str): ID del documento.

    Returns:
        dict: Datos del documento.
    """
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    doc = await doc_ref.get()
    return doc.to_dict()

async def get_collection_data(collection_name: str) -> list[dict]:
    """
    Obtiene todos los documentos de una colección en Firestore.

    Args:
        collection_name (str): Nombre de la colección.

    Returns:
        list[dict]: Lista de documentos en la colección.
    """
    db = await get_async_firestore_client()
    docs_ref = db.collection(collection_name).stream()
    docs = [doc.to_dict() async for doc in docs_ref]
    return docs	

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
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    await doc_ref.update(data)
    return doc_ref.id

async def delete_data(collection_name: str, id: str) -> str:
    """
    Elimina un documento de una colección en Firestore.

    Args:
        collection_name (str): Nombre de la colección.
        id (str): ID del documento.

    Returns:
        str: ID del documento eliminado.
    """
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    await doc_ref.delete()
    return doc_ref.id