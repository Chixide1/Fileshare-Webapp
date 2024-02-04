import os
import uuid
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient
from . import models

def create_blob_client(file_name):
    load_dotenv()

    kvuri = os.environ["KV_URI"]
    creds = DefaultAzureCredential()
    client = SecretClient(vault_url=kvuri, credential=creds)

    retrieved_secret = client.get_secret("fileshare-sa-key")
    storage_key = retrieved_secret.value
    
    return BlobClient(
    account_url=os.environ["ACCOUNT_URL"],
    container_name=('upload'),
    blob_name=file_name,
    credential=storage_key
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

# def handle_uploaded_file(f,n):
#     with open(n, "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)