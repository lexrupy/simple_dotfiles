#!/usr/bin/env bash

sudo apt update && sudo apt upgrade
flatpak update

# atualiza o widget imediatamente
polybar-msg hook updates 1 >/dev/null 2>&1

echo
echo "Pressione ENTER para fechar..."
read

