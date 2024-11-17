import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import SubscriptionClient

# Load environment variables from a .env file
load_dotenv()

# Azure credentials (replace with your own credentials)
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")

# Authenticate using the service principal
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Create a subscription client to list subscriptions and verify authentication
subscription_client = SubscriptionClient(credential)

# List subscriptions to test authentication
for subscription in subscription_client.subscriptions.list():
    print(f"Subscription ID: {subscription.subscription_id}, Subscription Name: {subscription.display_name}")
