import base64
import os
import subprocess
from typing import Tuple
from nacl.public import PrivateKey
from sqlalchemy.orm import Session
from models import ClientConfig
import ipaddress

def generate_keypair() -> Tuple[str, str]:
    """Генерирует пару ключей WireGuard"""
    try:
        # Генерируем приватный ключ
        private = PrivateKey.generate()
        
        # Конвертируем в формат WireGuard
        private_key = base64.b64encode(private.encode()).decode('utf-8')
        public_key = base64.b64encode(private.public_key.encode()).decode('utf-8')
        
        return private_key, public_key
    except Exception as e:
        raise Exception(f"Ошибка при генерации ключей: {str(e)}")

def generate_client_ip(db: Session) -> str:
    """Генерирует уникальный IP для нового клиента"""
    # Получаем все существующие IP
    existing_ips = db.query(ClientConfig.assigned_ip).all()
    existing_ips = [ip[0] for ip in existing_ips if ip[0]]
    
    # Начинаем с 10.0.0.2 (10.0.0.1 зарезервирован для сервера)
    for i in range(2, 255):
        candidate_ip = f"10.0.0.{i}"
        if candidate_ip not in existing_ips:
            return candidate_ip
    
    raise Exception("No available IP addresses")

def get_next_available_ip(used_ips: list) -> str:
    """Получает следующий доступный IP-адрес из подсети 10.0.0.0/24"""
    network = ipaddress.IPv4Network('10.0.0.0/24')
    used_ips_set = set(used_ips)
    
    # Начинаем с 10.0.0.2, так как 10.0.0.1 - адрес сервера
    for ip in network.hosts():
        ip_str = str(ip)
        if ip_str == '10.0.0.1':
            continue
        if ip_str not in used_ips_set:
            return ip_str
    raise Exception("Нет доступных IP-адресов")

def generate_client_keys() -> Tuple[str, str]:
    """Генерирует пару ключей для клиента"""
    try:
        # Генерируем приватный ключ
        private_key = subprocess.run(
            ['wg', 'genkey'],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Генерируем публичный ключ из приватного
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
    """Добавляет пир в конфигурацию сервера"""
    try:
        # Проверяем существование интерфейса wg0
        subprocess.run(
            ['/usr/bin/sudo', '/sbin/ip', 'link', 'show', 'wg0'],
            check=True,
            capture_output=True
        )
        
        # Проверяем входные данные
        if not client_public_key:
            raise ValueError("Client public key is required")
        if not client_ip:
            raise ValueError("Client IP is required")

        print(f"Adding peer with public key: {client_public_key} and IP: {client_ip}")
        
        # Добавляем пир
        cmd = [
            '/usr/bin/sudo', '/usr/bin/wg', 'set', 'wg0',
            'peer', client_public_key,
            'allowed-ips', f'{client_ip}/32'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Add peer command output: {result.stdout}")
        
        # Проверяем, что пир добавлен
        check_result = subprocess.run(
            ['/usr/bin/sudo', '/usr/bin/wg', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Current WireGuard configuration:\n{check_result.stdout}")
        
        # Сохраняем конфигурацию
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
    """Получает публичный ключ сервера из активной конфигурации"""
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

def generate_client_config(private_key: str, client_ip: str, server_public_key: str, server_endpoint: str) -> str:
    """
    Генерирует конфигурацию клиента WireGuard
    
    Args:
        private_key: Приватный ключ клиента
        client_ip: IP-адрес клиента
        server_public_key: Публичный ключ сервера
        server_endpoint: Endpoint сервера (IP:Port)
        
    Returns:
        str: Текст конфигурации WireGuard
    """
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

# Конфигурация сервера
SERVER_CONFIGS = {
    "sweden": {
        "public_key": "lagHVCshn3TLoxIANoXHGwdqXGmqE3dAww1A3Uyigxs=",
        "endpoint": "51.21.167.201:51820",
        "allowed_ips": "0.0.0.0/0",
    }
} 
