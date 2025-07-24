#!/bin/env python3
import tkinter as tk
import subprocess
import signal

# CAMERAS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
CAMERAS = [1, 11, 4, 2, 9, 3, 6, 7, 8]
DVR_IP = "10.216.62.6"
DVR_PORT = "554"
RES = 1
ROWS = 3
COLS = 3

# Cria 4 frames para os vídeos
frames = []
streams = []
processes = []


def embed_mplayer(parent, rtsp_url):
    parent.update()
    xid = str(parent.winfo_id())
    # cmd = [ "mplayer", "-quiet", "-wid", xid, "-noborder", "-geometry", "0:0", "-vo", "x11", rtsp_url, ]
    cmd = [
        "mpv",
        "--wid=" + xid,
        "--no-border",
        "--geometry=0:0",  # ignorado com wid, mas deixa por garantia
        "--fullscreen=no",
        "--quiet",
        "--cache=yes",
        "--cache-secs=3.0",
        "--framedrop=vo",
        "--no-keepaspect",  # Ignora proporção original
        "--video-unscaled=no",  # Permite redimensionar
        "--autofit-larger=100%x100%",  # Garante que tente preencher
        rtsp_url,
    ]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def on_close():
    for proc in processes:
        try:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                proc.kill()
            except Exception:
                pass
        except Exception:
            pass
    root.destroy()


root = tk.Tk()
root.title("Mosaico RTSP")
root.geometry("640x480")
root.protocol("WM_DELETE_WINDOW", on_close)
# root.attributes("-fullscreen", True)


for camera in CAMERAS:
    streams.append(
        f"rtsp://{DVR_IP}:{DVR_PORT}/cam/realmonitor?channel={camera}&subtype={RES}&unicast=true&proto=Onvif"  # Embute os mplayers
    )

# Configura o grid principal para redimensionar corretamente
for r in range(ROWS):
    root.rowconfigure(r, weight=1)
for c in range(COLS):
    root.columnconfigure(c, weight=1)

# Cria os frames e os vídeos
for index, rtsp_url in enumerate(streams):
    if index >= ROWS * COLS:
        break
    r = index // COLS
    c = index % COLS
    frame = tk.Frame(root, bg="black")
    frame.grid(row=r, column=c, sticky="nsew")
    proc = embed_mplayer(frame, rtsp_url)
    processes.append(proc)

root.mainloop()
