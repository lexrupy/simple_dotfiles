#!/bin/bash

mkdir -p mirror

for img in *.jpg; do
    # Redimensiona mantendo proporção, sem esticar
    # convert "$img" -resize 1920x1080\> "$img"

    # Cria versão espelhada horizontalmente
    convert "$img" -flop "espelhados/$img"
done

