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

# Obtener el cliente asíncrono de Firestore
async def get_async_firestore_client():
    db = firestore_async.client()
    return db

async def add_data(collection_name: str, data: dict) -> str:
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document()
    await doc_ref.set(data)
    return doc_ref.id

async def add_data(collection_name: str, data: dict, id: str) -> str:
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    await doc_ref.set(data)
    return doc_ref.id

async def get_data(collection_name: str, id: str) -> dict:
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    doc = await doc_ref.get()
    return doc.to_dict()

async def update_data(collection_name: str, id: str, data: dict) -> str:
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    await doc_ref.update(data)
    return doc_ref.id

async def delete_data(collection_name: str, id: str) -> str:
    db = await get_async_firestore_client()
    doc_ref = db.collection(collection_name).document(id)
    await doc_ref.delete()
    return doc_ref.id
