import os
import uuid
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient
from . import models

def get_storage_key():
    load_dotenv()

    kvuri = os.environ["KV_URI"]
    creds = DefaultAzureCredential()
    client = SecretClient(vault_url=kvuri, credential=creds)

    retrieved_secret = client.get_secret("fileshare-sa-key")
    storage_key = retrieved_secret.value
    return storage_key

def create_blob_client(file_name):    
    sa = get_storage_key()

    return BlobClient(
    account_url=os.environ["ACCOUNT_URL"],
    container_name=('upload'),
    blob_name=file_name,
    credential=sa
    )

def save_file_url_to_db(file_url):
    new_file = models.File.objects.create(file_url=file_url)
    new_file.save()
    return new_file

def upload_file_to_blob(file):

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    file_name = f"{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    blob_client = create_blob_client(file_name=file_name)
    blob_client.upload_blob(data=file_io)
    file_object = save_file_url_to_db(blob_client.url)

    return file_object

def download_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content

def delete_blob(bloburl):
    sa = get_storage_key()
    blobclient = BlobClient.from_blob_url(bloburl,sa)
    blobclient.delete_blob()