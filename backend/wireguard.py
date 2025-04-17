import base64
import os
import subprocess
from typing import Tuple
from nacl.public import PrivateKey
from sqlalchemy.orm import Session
from models import ClientConfig
import ipaddress
import requests

def generate_keypair() -> Tuple[str, str]:
    try:
        # Generating a private key
        private = PrivateKey.generate()
        
        # Convert to WireGuard format
        private_key = base64.b64encode(private.encode()).decode('utf-8')
        public_key = base64.b64encode(private.public_key.encode()).decode('utf-8')
        
        return private_key, public_key
    except Exception as e:
        raise Exception(f"Key generation error: {str(e)}")

def generate_client_ip(db: Session) -> str:
    # We get all existing IP addresses
    existing_ips = db.query(ClientConfig.assigned_ip).all()
    existing_ips = [ip[0] for ip in existing_ips if ip[0]]
    
    # Starting with 10.0.0.2 (10.0.0.1 is reserved for the server)
    for i in range(2, 255):
        candidate_ip = f"10.0.0.{i}"
        if candidate_ip not in existing_ips:
            return candidate_ip
    
    raise Exception("No available IP addresses")

def get_next_available_ip(used_ips: list, location: str) -> str:
    config = SERVER_CONFIGS.get(location)
    if not config:
        raise ValueError(f"Unknown location: {location}")
    
    network = ipaddress.IPv4Network(config["subnet"])
    used_ips_set = set(used_ips)
    
    for ip in network.hosts():
        ip_str = str(ip)
        if ip_str == config["server_ip"]:
            continue
        if ip_str not in used_ips_set:
            return ip_str
    raise Exception(f"There are no available IP addresses in the subnet {config['subnet']}")

def generate_client_keys() -> Tuple[str, str]:
    try:
        # Generating a private key
        private_key = subprocess.run(
            ['wg', 'genkey'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Generating a public key from a private one
        public_key = subprocess.run(
            ['wg', 'pubkey'],
            input=private_key,
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        print(f"Generated private key: {private_key}")
        print(f"Generated public key: {public_key}")

        if not private_key or not public_key:
            raise Exception("Failed to generate keys: Empty key(s) generated")

        return private_key, public_key
    except subprocess.CalledProcessError as e:
        print(f"Error generating keys: {e.stderr}")
        raise Exception(f"Failed to generate client keys: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error while generating keys: {str(e)}")
        raise

def add_peer_to_server(client_public_key: str, client_ip: str) -> None:
    try:
        # Check the existence of the wg0 interface
        subprocess.run(
            ['/usr/bin/sudo', '/sbin/ip', 'link', 'show', 'wg0'],
            check=True,
            capture_output=True
        )
        
        # Checking the input data
        if not client_public_key:
            raise ValueError("Client public key is required")
        if not client_ip:
            raise ValueError("Client IP is required")

        print(f"Adding peer with public key: {client_public_key} and IP: {client_ip}")
        
        # Adding a peer
        cmd = [
            '/usr/bin/sudo', '/usr/bin/wg', 'set', 'wg0',
            'peer', client_public_key,
            'allowed-ips', f'{client_ip}/32'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Add peer command output: {result.stdout}")
        
        # Check that the peer has been added
        check_result = subprocess.run(
            ['/usr/bin/sudo', '/usr/bin/wg', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Current WireGuard configuration:\n{check_result.stdout}")
        
        # Saving the configuration
        save_result = subprocess.run(
            ['/usr/bin/sudo', '/usr/bin/wg-quick', 'save', 'wg0'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Save configuration output: {save_result.stdout}")
        
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")
        raise Exception(f"Failed to add peer to server: {e.stderr}")
    except ValueError as e:
        print(f"Validation error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise

def get_server_public_key() -> str:
    try:
        result = subprocess.run(
            ['sudo', 'wg', 'show', 'wg0', 'public-key'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to get server public key: {e.stderr}")

def generate_client_config(private_key: str, client_ip: str, server_public_key: str, server_endpoint: str, location: str) -> str:
    config = f"""[Interface]
PrivateKey = {private_key}
Address = {client_ip}/32
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = {server_endpoint}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
    return config

# Server configuration
SERVER_CONFIGS = {
    "sweden": {
        "public_key": "lagHVCshn3TLoxIANoXHGwdqXGmqE3dAww1A3Uyigxs=",
        "endpoint": "51.21.167.201:51820",
        "subnet": "10.0.0.0/24",
        "server_ip": "10.0.0.1"
    },
    "london": {
        "public_key": "HHFjvE02xOGypOw02VuidiwkUa2e1iXi98OGCQud1QE=", 
        "endpoint": "18.130.235.215:51820",
        "subnet": "10.1.0.0/24",
        "server_ip": "10.1.0.1"
    }
}

async def add_peer_to_remote_server(client_public_key: str, client_ip: str, location: str) -> None:
    try:
        server_config = SERVER_CONFIGS.get(location)
        if not server_config:
            raise ValueError(f"Unknown location: {location}")
            
        # Get the IP and port from endpoint (format: IP:PORT)
        server_ip = server_config["endpoint"].split(":")[0]
        
        # Sending a request to a remote server
        response = requests.post(
            f"http://{server_ip}:8001/api/add-peer",
            json={
                "public_key": client_public_key,
                "allowed_ip": client_ip
            },
            timeout=10
        )
        
        if not response.ok:
            raise Exception(f"Failed to add peer to remote server: {response.text}")
            
        print(f"Successfully added peer to remote server {location}")
        
    except Exception as e:
        print(f"Error adding peer to remote server: {str(e)}")
        raise 