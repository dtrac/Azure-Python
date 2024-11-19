import requests
import os

# Define the local proxy settings
proxies = {
    "http": "http://127.0.0.1:3128",
    "https": "http://127.0.0.1:3128",
}

# Separator function for clarity
def print_separator(test_name):
    print(f"\n{'='*30}")
    print(f"Running Test: {test_name}")
    print(f"{'='*30}\n")

# First test with an invalid PEM file
print_separator("Test 1: Invalid PEM File")
os.environ['REQUESTS_CA_BUNDLE'] = '/Users/dan/mitmproxy-testing/certs.pem'
print(f"Using CA bundle: {os.getenv('REQUESTS_CA_BUNDLE')}")

try:
    response = requests.get("https://login.microsoftonline.com", proxies=proxies)
    print("First request successful:", response.status_code)
except requests.exceptions.SSLError as e:
    print(f"SSL error occurred for first request: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# Second test with a valid PEM file
print_separator("Test 2: Valid PEM File")
os.environ['REQUESTS_CA_BUNDLE'] = '/Users/dan/squid/ssl_cert/squid.pem'
print(f"Using CA bundle: {os.getenv('REQUESTS_CA_BUNDLE')}")

try:
    response = requests.get("https://login.microsoftonline.com", proxies=proxies)
    print("Second request successful:", response.status_code)
    print("Response snippet (first 100 chars):", response.text[:100])
except requests.exceptions.SSLError as e:
    print(f"SSL error occurred for second request: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

