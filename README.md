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
4. requests_proxy.py - This script relies on a working squid config (see below), but demonstrates the typical error messages seen when a TLS-inspecting proxy is in use and the client has an incorrect PEM file.

## Troubleshooting ⚠️

Make sure your Azure service principal has the necessary permissions to access the Key Vault and list subscriptions.
Verify that your .env file is properly configured with the correct values.

## Squid setup (macOS)

1. Install squid and check where it is installed:

   ```bash
   brew install squid
   brew info squid
   ==> squid: stable 6.12 (bottled), HEAD
   Advanced proxy caching server for HTTP, HTTPS, FTP, and Gopher
   https://www.squid-cache.org/
   Installed
   /usr/local/Cellar/squid/6.12 (180 files, 7.9MB) *
   Poured from bottle using the formulae.brew.sh API on 2024-11-18 at 20:49:16
   From: https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/s/squid.rb
   License: GPL-2.0-or-later
   ==> Dependencies
   Required: openssl@3 ✔
   ==> Options
   --HEAD
      Install HEAD version
   ==> Caveats
   To start squid now and restart at login:
   brew services start squid
   Or, if you don't want/need a background service you can just run:
   /usr/local/opt/squid/sbin/squid -N -d\ 1
   ==> Analytics
   install: 449 (30 days), 1,434 (90 days), 13,194 (365 days)
   install-on-request: 449 (30 days), 1,433 (90 days), 13,190 (365 days)

2. Configure squid proxy (squid.conf):

<details>
<summary>Click to expand squid.conf configuration snippet</summary>

   ```plaintext
   # Example rule allowing access from your local networks.
   # Adapt to list your (internal) IP networks from where browsing
   # should be allowed
   acl localnet src 0.0.0.1-0.255.255.255	# RFC 1122 "this" network (LAN)
   acl localnet src 10.0.0.0/8		# RFC 1918 local private network (LAN)
   acl localnet src 100.64.0.0/10		# RFC 6598 shared address space (CGN)
   acl localnet src 169.254.0.0/16 	# RFC 3927 link-local (directly plugged) machines
   acl localnet src 172.16.0.0/12		# RFC 1918 local private network (LAN)
   acl localnet src 192.168.0.0/16		# RFC 1918 local private network (LAN)
   acl localnet src fc00::/7       	# RFC 4193 local private network range
   acl localnet src fe80::/10      	# RFC 4291 link-local (directly plugged) machines

   acl SSL_ports port 443
   acl Safe_ports port 80		# http
   acl Safe_ports port 21		# ftp
   acl Safe_ports port 443		# https
   acl Safe_ports port 70		# gopher
   acl Safe_ports port 210		# wais
   acl Safe_ports port 1025-65535	# unregistered ports
   acl Safe_ports port 280		# http-mgmt
   acl Safe_ports port 488		# gss-http
   acl Safe_ports port 591		# filemaker
   acl Safe_ports port 777		# multiling http

   #
   # Recommended minimum Access Permission configuration:
   #
   # Deny requests to certain unsafe ports
   http_access deny !Safe_ports

   # Deny CONNECT to other than secure SSL ports
   http_access deny CONNECT !SSL_ports

   # Only allow cachemgr access from localhost
   http_access allow localhost manager
   http_access deny manager

   # limit only specific sites to have SSL inspection (with own CA)
   # The traffic of other sites will not be intercepted. 
   # see `ssl_bump` later
   acl bump_targets ssl::server_name .reddit.com

   # This default configuration only allows localhost requests because a more
   # permissive Squid installation could introduce new attack vectors into the
   # network by proxying external TCP connections to unprotected services.
   http_access allow localhost

   # The two deny rules below are unnecessary in this default configuration
   # because they are followed by a "deny all" rule. However, they may become
   # critically important when you start allowing external requests below them.

   # Protect web applications running on the same server as Squid. They often
   # assume that only local users can access them at "localhost" ports.
   http_access deny to_localhost

   # Protect cloud servers that provide local users with sensitive info about
   # their server via certain well-known link-local (a.k.a. APIPA) addresses.
   http_access deny to_linklocal

   #
   # INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS
   #

   # For example, to allow access from your local networks, you may uncomment the
   # following rule (and/or add rules that match your definition of "local"):
   # http_access allow localnet

   # And finally deny all other access to this proxy
   http_access deny all

   # Squid normally listens to port 3128
   #http_port 3128

   # setup ssl-bump with an own CA
   http_port 3128 ssl-bump generate-host-certificates=on tls-cert=<path to PEM>
   sslcrtd_program /usr/local/Cellar/squid/6.12/libexec/security_file_certgen -s /usr/local/var/lib/squid/ssl_db  -M 4MB
   #ssl_bump bump bump_targets
   tls_outgoing_options cafile=<path to PEM>

   # Bump the connection. Establish a secure connection with the server first, then establish a secure connection with the client, using a mimicked server certificate.
   ssl_bump server-first all
   # Ensure server certificate errors terminate the transaction
   sslproxy_cert_error deny all

   # Uncomment and adjust the following to add a disk cache directory.
   cache_dir ufs /usr/local/var/cache/squid 100 16 256

   # Leave coredumps in the first cache dir
   coredump_dir /usr/local/var/cache/squid

   #
   # Add any of your own refresh_pattern entries above these.
   #
   refresh_pattern ^ftp:		1440	20%	10080
   refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
   refresh_pattern .		0	20%	4320
   ```

</details>

1. Generate a self-signed CA SSL certificate which is configured in the squid.conf file above:

   ```bash
   $ openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout /path/to/the/squid.pem -out /path/to/the/squid.pem

2. Initializing the SSL Certificate Storage and configure file ownership:

   ```bash
    $/usr/local/Cellar/squid/6.12/libexec/security_file_certgen -c -s /usr/local/var/lib/squid/ssl_db -M 4MB
    $chown -R user /usr/local/var/cache/squid

3. Create squid cache:
   
   ```bash
   $squid -z

4. Start squid:

   ```bash
   $/usr/local/opt/squid/sbin/squid -N -d 1
   2024/11/19 16:03:40| Accepting SSL bumped HTTP Socket connections at conn13 local=[::]:3128 remote=[::] FD 31 flags=9
    listening port: 3128
   2024/11/19 16:03:40| Done reading /usr/local/var/cache/squid swaplog (2 entries)
   2024/11/19 16:03:40| Finished rebuilding storage from disk.
            2 Entries scanned
            0 Invalid entries
            0 With invalid flags
            2 Objects loaded
            0 Objects expired
            0 Objects canceled
            0 Duplicate URLs purged
            0 Swapfile clashes avoided
      Took 0.05 seconds (37.51 objects/sec).
   2024/11/19 16:03:40| Beginning Validation Procedure
   2024/11/19 16:03:40| Completed Validation Procedure
      Validated 2 Entries
      store_swap_size = 572.00 KB
   2024/11/19 16:03:41| storeLateRelease: released 0 objects

5. Run the requests_proxy.py script:

   ```bash
   python ./requests_proxy.py

   ==============================
   Running Test: Test 1: Invalid PEM File
   ==============================

   Using CA bundle: /Users/dan/mitmproxy-testing/certs.pem
   SSL error occurred for first request: HTTPSConnectionPool(host='www.yahoo.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1020)')))

   ==============================
   Running Test: Test 2: Valid PEM File
   ==============================

   Using CA bundle: /Users/dan/squid/ssl_cert/squid.pem
   Second request successful: 200
   Response snippet (first 100 chars): 

   <!-- Copyright (C) Microsoft Corporation. All rights reserved. -->
   <!DOCTYPE html>
   <html dir="


