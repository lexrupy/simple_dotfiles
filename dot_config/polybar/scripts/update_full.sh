#!/usr/bin/env bash


export SUDO_ASKPASS=/usr/bin/ssh-askpass

sudo -A apt update && sudo -A apt upgrade
flatpak update

# atualiza o widget imediatamente
polybar-msg action "#updates.hook.0" #>/dev/null 2>&1

echo
echo "Pressione ENTER para fechar..."
read

