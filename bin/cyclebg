#!/bin/bash
#
# #
# new=$(find /home/alexandre/Imagens/wallpapers/*.jpg -type f | shuf | sed -n 1p)
# cp $new /usr/share/backgrounds/ldm/wall.jpg
#
#


# Pega os IPs de interfaces LAN e Wi-Fi
LAN_IP=$(ip -o -4 addr show | grep -E 'enp|eth' | awk '{print " LAN: " $4}' | cut -d/ -f1)
WIFI_IP=$(ip -o -4 addr show | grep -E 'wlp|wlan|wlo' | awk '{print "WiFi: " $4}' | cut -d/ -f1)

# Texto a ser impresso
TEXT="$LAN_IP\n$WIFI_IP"

# Seleciona imagem aleatória
WALL=$(find /home/alexandre/Imagens/wallpapers/ -name '*.jpg' | shuf -n 1)

# Cria uma imagem temporária com o IP desenhado
TMP_IMG="/tmp/wallpaper_with_ip.jpg"

# Desenha o texto (IP) na imagem
convert "$WALL" -gravity SouthEast -pointsize 26 -fill white -font Agave-Nerd-Font-Mono-Regular -undercolor '#00000080' -annotate +20+20 "$TEXT" "$TMP_IMG"

# Copia para o local final
cp "$TMP_IMG" /usr/share/backgrounds/ldm/wall.jpg
