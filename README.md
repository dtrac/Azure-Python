# Azure Python Scripts 🚀

This repository contains Python scripts for interacting with **Azure Storage**, **Azure Key Vault** and **Azure Management** APIs. The scripts authenticate to Azure using **service principals** and retrieve secrets from Key Vault and list Azure subscriptions.

## Prerequisites 📋

To run these scripts, you'll need:
- Python 3.x
- Azure subscription with access to **Azure Key Vault** and **Azure Management APIs**
- Required Python packages (`azure-identity`, `azure-keyvault-secrets`, `python-dotenv`, `azure-mgmt-resource`)

## Installation 🛠️

1. Clone the repository ⬇️:
   ```bash
   git clone https://github.com/yourusername/azure-python-scripts.git
   cd azure-python-scripts
2. Install the required dependencies ⚙️:
   ```bash
   pip install -r requirements.txt
3. Set up environment variables 🌿 by creating a .env file. The .env file should include the following variables:
   ```bash
   KEY_VAULT_URL=https://your-keyvault-name.vault.azure.net/
   AZURE_TENANT_ID=your-tenant-id
   AZURE_CLIENT_ID=your-client-id
   AZURE_CLIENT_SECRET=your-client-secret

❗ **Make sure to add .env to your .gitignore to avoid accidental commits of sensitive information.** ❗

## Scripts 💻
1. azure-keyvault.py - Access a Secret from Azure Key Vault
This script authenticates using DefaultAzureCredential, connects to Azure Key Vault, and retrieves a secret.
2. azure-auth.py - This script uses a service principal to authenticate with Azure and lists available subscriptions.
3. azure-storage.py - This script uses a service principal to connect to Azure storage and retrieve a blob from a container.
## Troubleshooting ⚠️
Make sure your Azure service principal has the necessary permissions to access the Key Vault and list subscriptions.
Verify that your .env file is properly configured with the correct values.