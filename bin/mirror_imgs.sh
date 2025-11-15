#!/bin/bash

CONVERT_FLAG=false
MIRROR_DIR="mirror"

# Verifica parâmetro
if [[ "$1" == "--convert" ]]; then
    CONVERT_FLAG=true
fi

mkdir -p "$MIRROR_DIR"

if $CONVERT_FLAG; then
    echo "Convertendo todas as imagens para 1080p..."
    for img in *.jpg; do
        convert "$img" -resize 1920x1080\> "$img"
    done
fi

echo "Gerando espelhados..."
for img in *.jpg; do
    convert "$img" -flop "$MIRROR_DIR/$img"
done

echo "Pronto!"

