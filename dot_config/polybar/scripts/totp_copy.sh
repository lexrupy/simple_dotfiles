#!/bin/bash

export DISPLAY=:0
export XAUTHORITY="$HOME/.Xauthority"

SECRET_FILE="$HOME/.secrets/secrets.txt"
secret=$(cut -d':' -f2 "$SECRET_FILE")

code=$(oathtool --base32 --totp "$secret")

echo -n "$code" | xclip -selection clipboard

