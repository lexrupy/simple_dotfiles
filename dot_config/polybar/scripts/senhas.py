#!/usr/bin/env python3
import atexit
import os
import sys
import tkinter as tk

ARQ = os.path.expanduser("~/.secrets/senhas.txt")
LOCKFILE = os.path.expanduser("~/.cache/senhas.lock")

def ler_pid_lock():
    if not os.path.exists(LOCKFILE):
        return None
    try:
        with open(LOCKFILE, "r") as f:
            pid = int(f.read().strip())
        return pid
    except Exception:
        return None


def pid_esta_ativo(pid):
    try:
        os.kill(pid, 0)  # não envia sinal, apenas verifica
        return True
    except ProcessLookupError:
        return False  # PID não existe
    except PermissionError:
        return True   # PID existe, mas não temos permissão


def pid_e_script(pid):
    try:
        nome_script = os.path.basename(__file__)
        with open(f"/proc/{pid}/cmdline", "r") as f:
            cmd = f.read()
        return nome_script in cmd
    except Exception:
        return False



def criar_lock():
    os.makedirs(os.path.dirname(LOCKFILE), exist_ok=True)
    pid = ler_pid_lock()
    if pid and pid_esta_ativo(pid) and pid_e_script(pid):
        # Processo ativo, não abrir outra instância
        sys.exit(0)

    # Grava PID atual
    with open(LOCKFILE, "w") as f:
        f.write(str(os.getpid()))
    atexit.register(remover_lock)

def remover_lock():
    if os.path.exists(LOCKFILE):
        os.unlink(LOCKFILE)

def carregar_senhas():
    dados = {}
    if not os.path.exists(ARQ):
        return dados

    with open(ARQ, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if ":" not in linha:
                continue
            app, senha = linha.split(":", 1)
            dados[app.strip()] = senha.strip()

    return dados


def modo_polybar(senhas):
    print("[SENHAS]")
    sys.exit(0)


def abrir_janela(senhas, delay=5):
    root = tk.Tk()
    root.title("+- Copiar Senha -+")
    # Tamanho reduzido
    root.geometry("230x230")

    # Pegar posição do ponteiro do mouse
    mx = root.winfo_pointerx()
    my = root.winfo_pointery()

    # Posicionar janela perto do clique (offset pequeno)
    root.geometry(f"+{mx-100}+{my+25}")

    root.bind("<Escape>", lambda e: (root.destroy(),))

    lista = tk.Listbox(root, width=40, height=15)
    lista.pack(padx=10, pady=10)

    apps = sorted(senhas.keys())
    for app in apps:
        lista.insert(tk.END, app)

    status = tk.Label(root, text="", fg="green")
    status.pack()

    def copiar(event):
        idx = lista.curselection()
        if not idx:
            return
        app = apps[idx[0]]
        senha = senhas.get(app)

        root.clipboard_clear()
        root.clipboard_append(senha)
        root.update()  # mantém clipboard mesmo após fechar a janela

        status.config(text=f"Senha de '{app}' copiada!")

        # Oculta a janela imediatamente
        root.withdraw()

        # Encerra após X segundos
        root.after(int(delay * 1000), root.destroy)

    lista.bind("<Double-Button-1>", copiar)

    root.mainloop()


def main():
    senhas = carregar_senhas()

    if "--show" not in sys.argv:

        modo_polybar(senhas)

        
    criar_lock()
    abrir_janela(senhas, delay=8)


if __name__ == "__main__":
    main()
