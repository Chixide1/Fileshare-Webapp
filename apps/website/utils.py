import os
import uuid
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient, generate_blob_sas, BlobSasPermissions
from . import models
import datetime

def get_storage_key():
    load_dotenv()

    kvuri = os.environ["KV_URI"]
    creds = DefaultAzureCredential(AZURE_CLIENT_ID=os.environ["AZURE_CLIENT_ID"])
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

def delete_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        msg = f" has already expired and been deleted"
        return msg
    blob_client.delete_blob()
    msg = f" was successfully deleted"
    return msg

def generate_sas(file_name):
    sa = get_storage_key()

    blob_client = create_blob_client(file_name)

    if not blob_client.exists():
        return

    start_time = datetime.datetime.now(datetime.timezone.utc)
    expiry_time = start_time + datetime.timedelta(days=1)

    sas_token = generate_blob_sas(
        account_name=blob_client.account_name,
        container_name=blob_client.container_name,
        blob_name=blob_client.blob_name,
        account_key=sa,
        permission=BlobSasPermissions(read=True),
        expiry=expiry_time,
        start=start_time
    )
    sas_url = f"{blob_client.url}?{sas_token}"
    return sas_url