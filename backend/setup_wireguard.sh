#!/bin/bash

# Проверяем, установлен ли WireGuard
if ! command -v wg &> /dev/null; then
    echo "WireGuard не установлен. Устанавливаем..."
    sudo apt update
    sudo apt install -y wireguard
fi

# Генерируем ключи для сервера
if [ ! -f /etc/wireguard/server_private.key ]; then
    wg genkey | sudo tee /etc/wireguard/server_private.key
    sudo cat /etc/wireguard/server_private.key | wg pubkey | sudo tee /etc/wireguard/server_public.key
fi

# Создаем базовую конфигурацию сервера
SERVER_PRIVATE_KEY=$(sudo cat /etc/wireguard/server_private.key)

cat << EOF | sudo tee /etc/wireguard/wg0.conf
[Interface]
PrivateKey = ${SERVER_PRIVATE_KEY}
Address = 10.0.0.1/24
ListenPort = 51820
SaveConfig = true

# Включаем форвардинг пакетов
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
EOF

# Включаем IP форвардинг
echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Устанавливаем правильные разрешения
sudo chmod 600 /etc/wireguard/wg0.conf
sudo chmod 600 /etc/wireguard/server_private.key
sudo chmod 600 /etc/wireguard/server_public.key

# Запускаем WireGuard
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

echo "WireGuard успешно настроен!"
echo "Публичный ключ сервера:"
sudo cat /etc/wireguard/server_public.key 