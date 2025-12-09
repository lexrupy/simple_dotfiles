#!/usr/bin/env python3
import email
import imaplib
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

IMAP_SERVER = "imap.gmail.com"
IMAP_USER   = "lexrupy@gmail.com"
IMAP_PASS   = Path("~/.secrets/pmsc2faclient.txt").expanduser().read_text().strip()

SAVE_FILE = os.path.expanduser("~/.cache/2fa_code.txt")

ANIMATION_FRAMES = [
        "[○●○○]",
        "[○○●○]",
        "[○○○●]",
        "[○○●○]",
        "[○●○○]",
        "[●○○○]",
    ]


def animation_worker(stop_event):
    i = 0
    while not stop_event.is_set():
        write_code(ANIMATION_FRAMES[i % len(ANIMATION_FRAMES)])
        i += 1
        time.sleep(1)  # velocidade da animação

def extrair_codigo(html):
    m = re.search(r"<h1><b>([0-9a-zA-Z]{6})</b></h1>", html)
    if m:
        return m.group(1)
    return None

def write_code(code):
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    with open(SAVE_FILE, "w") as f:
        f.write(code.strip() + "\n")

def read_cached_code():
    if not os.path.exists(SAVE_FILE):
        return None
    return Path(SAVE_FILE).read_text().strip()

def copy_to_clipboard(text):
    subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())


def obter_ultimo_codigo():
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(IMAP_USER, IMAP_PASS)

    pastas = ["INBOX", "[Gmail]/Spam"]

    emails_encontrados = []

    # Buscar nas duas pastas
    for pasta in pastas:
        try:
            status, _ = M.select(pasta)
            if status != "OK":
                continue
        except:
            continue

        status, data = M.search(None, '(SUBJECT "Token acesso 2FA PMSC")')
        if status != "OK":
            continue

        ids = data[0].split()
        for msg_id in ids:
            emails_encontrados.append((pasta, msg_id))

    if not emails_encontrados:
        return None

    # Usa o último email encontrado
    pasta, msg_id = emails_encontrados[-1]

    # Reabre a pasta correta para fazer o fetch
    M.select(pasta)
    status, msg_data = M.fetch(msg_id, "(RFC822)")
    if status != "OK":
        return None

    msg = email.message_from_bytes(msg_data[0][1])

    # Extract HTML
    html = None
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                html = part.get_payload(decode=True).decode(part.get_content_charset("utf-8"))
                break
    else:
        if msg.get_content_type() == "text/html":
            html = msg.get_payload(decode=True).decode(msg.get_content_charset("utf-8"))

    if not html:
        return None

    codigo = extrair_codigo(html)

    #  Move email para a Lixeira se achou código
    if codigo:
        # Seleciona pasta original novamente
        M.select(pasta)
        # Move para lixeira (Gmail aceita este comando)
        M.store(msg_id, '+X-GM-LABELS', '\\Trash')

    return codigo



def obter_com_retentativas_fib(n):
    """
    n = número de tentativas adicionais
    n=0 → somente uma tentativa imediata
    n=1 → imediata + 2 segundos
    n=2 → imediata + 2s + 3s
    n=3 → imediata + 2s + 3s + 5s
    ...
    """

    # primeira tentativa imediata
    delays = [0]

    # gerar delays adicionais seguindo Fibonacci suave
    fib = [2, 3]  
    for i in range(n):
        if i < 2:
            delays.append(fib[i])
        else:
            next_delay = delays[-1] + delays[-2]
            delays.append(next_delay)

    # executar tentativas
    for delay in delays:
        if delay > 0:
            time.sleep(delay)

        codigo = obter_ultimo_codigo()
        if codigo:
            return codigo

    return None



def obter_com_retentativas(n):
    """
    n = número de tentativas adicionais
    n=0 → somente uma tentativa imediata
    n=1 → imediata + 1s
    n=2 → imediata + 1s + 2s
    n=3 → imediata + 1s + 2s + 3s
    ...
    """
    # delays: [0, 1, 2, 3 ...]
    delays = [i for i in range(n + 1)]



    for delay in delays:
        if delay > 0:
            time.sleep(delay)
            

        
        codigo = obter_ultimo_codigo()
        if codigo:
            return codigo

    return None


def main():
    # --- CLI: clique no polybar ---
    if "--check" in sys.argv:
        save_path = Path(SAVE_FILE)

        try:
            current = save_path.read_text().strip()
        except FileNotFoundError:
            current = ""

        # Se contiver um frame → animação ainda rodando
        if current in ANIMATION_FRAMES:
            return

        stop_event = threading.Event()
        # inicia animação em thread separada
        t = threading.Thread(target=animation_worker, args=(stop_event,))
        t.start()


        codigo = obter_com_retentativas(3)

        # parar animação
        stop_event.set()
        t.join()

        if codigo:
            write_code(codigo)
            copy_to_clipboard(codigo)
        else:
            write_code("######")
        return


    # --- Exec normal (polling) ---
    codigo = read_cached_code()
    if codigo:
        print("PMSC:", codigo)
    else:
        print("PMSC: ------")


if __name__ == "__main__":
    main()
