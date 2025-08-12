#!/bin/bash

CONFIG=~/.config/picom/picom.conf

while true; do
    if pgrep projecteur > /dev/null; then
        if grep -q '^#\s*"window_type = '\''tooltip'\''",\s*#PROJECTEUR_RUNNING' ~/.config/picom/picom.conf; then
            sed -i '/^#  "window_type = '\''tooltip'\''",\s*#PROJECTEUR_RUNNING/ s/^#  //' ~/.config/picom/picom.conf
        else
            echo "Linha NÃO está comentada."
        fi
    else
        if grep -q '^#\s*"window_type = '\''tooltip'\''",\s*#PROJECTEUR_RUNNING' ~/.config/picom/picom.conf; then
            echo "Linha está comentada."
        else
            sed -i '/^\s*"window_type = '\''tooltip'\''",\s*#PROJECTEUR_RUNNING/ s/^/#  /' ~/.config/picom/picom.conf
        fi
    fi

    # Espera 5 segundos antes de checar novamente
    sleep 5
done

