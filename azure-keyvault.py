import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Load environment variables for credentials (optional if using DefaultAzureCredential)
load_dotenv() # Uncomment if you use a .env file

# URL of your Azure Key Vault
key_vault_url = os.getenv("KEY_VAULT_URL", "https://dantpython.vault.azure.net/")

# Authenticate with Azure
credential = DefaultAzureCredential()

# Create a client to interact with Key Vault
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Name of the secret you want to retrieve
secret_name = "test-secret-name"

try:
    # Retrieve the secret
    secret = client.get_secret(secret_name)
    print(f"Secret value: {secret.value}")
except Exception as e:
    print(f"An error occurred: {e}")
