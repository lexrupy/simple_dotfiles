#!/bin/env python3

import os
import subprocess
import sys
import time

import pyotp


def carregar_segredo_totp(label_desejado, caminho_arquivo="~/.secrets/secrets.txt"):
    caminho_completo = os.path.expanduser(caminho_arquivo)
    
    if not os.path.exists(caminho_completo):
        print(f"{label_desejado}: NOKEY")
        return None

    with open(caminho_completo, 'r') as arquivo:
        for linha in arquivo:
            if linha.strip().startswith('#') or not linha.strip():
                continue
            if ':' in linha:
                label, code = linha.strip().split(':', 1)
                if label == label_desejado:
                    return code.strip()
    print(f"{label_desejado}: NOKEY")
    return None


def copiar_clipboard(texto):
    subprocess.run(["xclip", "-selection", "clipboard"], input=texto.encode())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    label_alvo = sys.argv[1]
    modo_copy = ("--copy" in sys.argv)

    secret_key = carregar_segredo_totp(label_alvo)

    if not secret_key:
        sys.exit(1)

    totp = pyotp.TOTP(secret_key)
    code = totp.now()

    if modo_copy:
        copiar_clipboard(code)
        sys.exit(0)

    # Segundos restantes do ciclo TOTP (30s)
    falta = 30 - (int(time.time()) % 30)

    if falta <= 5:
        label_fmt = f"%{{F#FF0000}}{label_alvo}: {code}%{{F-}}"
    else:
        label_fmt = f"{label_alvo}: {code}"

    print(f"{label_fmt}")
