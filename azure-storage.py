import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Load environment variables from a .env file
load_dotenv()

# Azure Blob Storage details from environment variables
account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "dantpython")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME", "dant")
blob_name = os.getenv("AZURE_STORAGE_BLOB_NAME", "requests_example.py")
download_path = os.getenv("AZURE_STORAGE_DOWNLOAD_PATH", "downloaded_blob.py")

# Authenticate using DefaultAzureCredential (this handles different authentication methods)
credential = DefaultAzureCredential()

# Create a BlobServiceClient to interact with the Azure Blob service
blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=credential)

# Get a reference to the specific container and blob
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

# Download the blob to the specified path
try:
    with open(download_path, "wb") as download_file:
        download_stream = blob_client.download_blob()
        download_stream.readinto(download_file)
    print(f"Blob {blob_name} downloaded successfully to {download_path}")
except Exception as e:
    print(f"An error occurred while downloading the blob: {e}")
