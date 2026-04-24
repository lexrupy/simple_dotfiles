#!/usr/bin/env python3
import email
import imaplib
import re
import subprocess
import sys
import time
from pathlib import Path

IMAP_SERVER = "imap.gmail.com"
IMAP_USER = "lexrupy@gmail.com"
IMAP_PASS = Path("~/.secrets/pmsc2faclient.txt").expanduser().read_text().strip()

SAVE_FILE = Path("~/.cache/2fa_code.txt").expanduser()
TTL_FILE = Path("~/.cache/2fa_ttl.txt").expanduser()
IN_SEARCH_FILE = Path("~/.cache/2fa_in_search.txt").expanduser()

CACHE_TTL = 50

ANIMATION_FRAMES = [
    "[○●○○]",
    "[○○●○]",
    "[○○○●]",
    "[○○●○]",
    "[○●○○]",
    "[●○○○]",
]


def get_current_animation_frame():
    # Usa o timestamp atual para ciclar entre os frames
    # Assim, a cada segundo o Polybar recebe o próximo frame
    index = int(time.time()) % len(ANIMATION_FRAMES)
    return ANIMATION_FRAMES[index]


def extrair_codigo(html):
    m = re.search(r"<h1><b>([0-9a-zA-Z]{6})</b></h1>", html)
    if m:
        return m.group(1)
    return None


def touch_ttl():
    TTL_FILE.parent.mkdir(parents=True, exist_ok=True)
    TTL_FILE.touch()


def write_code(code):
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SAVE_FILE.write_text(code.strip() + "\n")


def cache_valido():
    if not TTL_FILE.exists():
        return 0

    age = time.time() - TTL_FILE.stat().st_mtime
    restante = CACHE_TTL - age

    if restante <= 0:
        SAVE_FILE.unlink()
        TTL_FILE.unlink()
        return 0

    return restante


def read_cached_code():
    if not SAVE_FILE.exists():
        return None

    return SAVE_FILE.read_text().strip()


def copy_to_clipboard(text):
    subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())


def preencher_navegador(codigo):
    try:
        # procura janela com esse título
        result = (
            subprocess.check_output(
                ["xdotool", "search", "--name", "PMSC - Verificação 2FA"]
            )
            .decode()
            .strip()
            .splitlines()
        )

        if not result:
            return False

        win = result[-1]  # última janela encontrada

        # ativa janela
        subprocess.run(["xdotool", "windowactivate", "--sync", win])

        time.sleep(0.2)

        # cola no primeiro campo
        subprocess.run(["xdotool", "key", "ctrl+a"])
        subprocess.run(["xdotool", "type", "--delay", "50", codigo])

        return True

    except Exception:
        return False


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
                html = part.get_payload(decode=True).decode(
                    part.get_content_charset("utf-8")
                )
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
        M.store(msg_id, "+X-GM-LABELS", "\\Trash")

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


def print_status(tempo_restante=0):
    codigo = read_cached_code()
    if codigo:
        # Apenas o código fica vermelho se faltar menos de 10s
        if tempo_restante < 10:
            display_codigo = f"%{{F#ff0000}}{codigo}%{{F-}}"
        else:
            display_codigo = codigo
        print(f"PMSC: {display_codigo}")
    else:
        print("PMSC: ######")


def main():
    tempo_restante = cache_valido()
    # --- CHAMADA REGULAR DO POLYBAR (interval = 1) ---
    if "--check" not in sys.argv:
        if tempo_restante > 0:
            print_status(tempo_restante)
        elif IN_SEARCH_FILE.exists():
            # Se o arquivo de trava existe, apenas printa o frame da vez
            print(f"PMSC: {get_current_animation_frame()}")
        else:
            print("PMSC: ######")
        return

    # --- CHAMADA DO CLIQUE (click-left) ---
    if "--check" in sys.argv:
        if IN_SEARCH_FILE.exists():
            return

        if tempo_restante > 0:
            codigo = read_cached_code()
            if codigo:
                copy_to_clipboard(codigo)
            return

        # Cria a trava e inicia a busca
        try:
            IN_SEARCH_FILE.touch()

            # Como o Polybar já está rodando a animação via 'get_current_animation_frame',
            # aqui no --check nós apenas fazemos a busca bloqueante.
            codigo = obter_com_retentativas(3)

            if codigo:
                write_code(codigo)
                touch_ttl()
                copy_to_clipboard(codigo)
                preencher_navegador(codigo)
        finally:
            # Remove a trava para parar a animação no Polybar
            if IN_SEARCH_FILE.exists():
                IN_SEARCH_FILE.unlink()


if __name__ == "__main__":
    main()
