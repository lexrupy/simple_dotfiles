#!/bin/bash
#
#
new=$(find /home/alexandre/Imagens/wallpapers/*.jpg -type f | shuf | sed -n 1p)
cp $new /usr/share/backgrounds/ldm/wall.jpg
