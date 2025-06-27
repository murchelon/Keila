#!/bin/bash

# Script em: sudo nano /usr/local/bin/ativar_wifi.sh

LOG_FILE="/tmp/ativar_wifi.log"

log_msg() {
    echo "[$(date '+%d/%m/%Y %H:%M:%S')]  $1" >> "$LOG_FILE"
}

log_cmd() {
    log_msg "$1"
    OUTPUT=$(eval "$2" 2>&1)
    log_msg "$OUTPUT"
}

log_msg "=== Início do script ativar_wifi.sh ==="
sleep 2

log_cmd "Desbloqueando Wi-Fi ..." "/usr/sbin/rfkill unblock wifi"
sleep 2

log_cmd "Ativando a interface wlan0 ..." "/usr/sbin/ip link set wlan0 up"
sleep 2

log_cmd "Iniciando o serviço wpa_supplicant@wlan0 ..." "/usr/bin/systemctl start wpa_supplicant@wlan0"
sleep 2

IP_EXISTE=$(/usr/sbin/ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

if [ -z "$IP_EXISTE" ]; then
    log_cmd "Solicitando IP via DHCP ..." "/usr/sbin/dhclient wlan0"
else
    log_msg "Interface wlan0 já possui IP: $IP_EXISTE"
    # Se quiser renovar IP, descomente a linha abaixo:
    # log_cmd "Renovando IP via DHCP ..." "/usr/sbin/dhclient -r wlan0 && /usr/sbin/dhclient wlan0"
fi

sleep 2
log_msg "=== Fim do script ==="