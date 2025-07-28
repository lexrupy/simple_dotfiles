#!/bin/env python3

import tkinter as tk
import threading
import time
import subprocess
import signal
import shutil

if not shutil.which("mpv"):
    raise RuntimeError("MPV não encontrado. Instale com: sudo apt install mpv")

# CAMERAS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
ALL_CAMERAS = [1, 11, 4, 2, 9, 3, 6, 7, 8]
DVR_IP = "10.216.62.6"
DVR_PORT = "554"
RES = 1
ROWS = 3
COLS = 3
GAP = 1
fullscreen = False
last_geometry = None


cameras = []


class Camera:
    def __init__(self, parent, rtsp_url, width=320, height=240, index=1):
        self.parent = parent
        self.rtsp_url = rtsp_url
        self.process = None
        self.start_time = None
        self.camera_index = index

        self.frame = tk.Frame(
            parent, bg="black", width=width, height=height, takefocus=0
        )
        self.frame.grid_propagate(False)

        # Label "Conectando..."
        self.label = tk.Label(
            self.frame,
            text=f"Conectando camera {self.camera_index}...",
            fg="white",
            bg="black",
            font=("Arial", 12),
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.label.lift()

        # Botão "Reconectar"
        self.reconnect_btn = tk.Button(
            self.frame, text="Reconectar", command=self.restart_stream
        )
        # self.reconnect_btn.place(relx=0.5, rely=0.5, anchor="center")
        # self.reconnect_btn.lower()
        self.reconnect_btn.place_forget()

        self.frame.after(100, self.restart_stream)

    def embed_mpv(self):
        self.frame.update_idletasks()
        xid = str(self.frame.winfo_id())

        MPV_ARGS = [
            "--no-border",
            "--geometry=0:0",
            "--fullscreen=no",
            "--quiet",
            "--osc=no",
            "--no-osd-bar",
            "--cache=yes",
            "--cache-secs=3.0",
            "--framedrop=vo",
            "--no-keepaspect",
            "--video-unscaled=no",
            "--autofit-larger=100%x100%",
            #
            "--no-terminal",
            "--focus-on-open=no",
            # "--no-input-default-bindings",
            # "--input-conf=/dev/null",
            "--force-window=no",  # <--- Isso evita criar nova janela
        ]

        cmd = ["mpv", f"--wid={xid}", *MPV_ARGS, self.rtsp_url]
        return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    def restart_stream(self):
        self.reconnect_btn.place_forget()
        self.label.config(text=f"Conectando câmera {self.camera_index}...")
        self.label.lift()
        self.start_time = time.time()
        self.process = self.embed_mpv()
        threading.Thread(target=self.monitor_process, daemon=True).start()
        root.after(1000, lambda: root.focus_force())

    def monitor_process(self):
        # Aguarda processo estabilizar
        for _ in range(10):  # ~3s
            if self.process.poll() is not None:
                self.on_crash()
                return
            time.sleep(0.3)

        # Se chegou aqui, consideramos "conectado"
        self.label.lower()

        # Agora espera o processo morrer
        self.process.wait()
        self.on_crash()

    def kill_process(self):
        if self.process is not None:
            try:
                self.process.send_signal(signal.SIGTERM)
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                try:
                    self.process.kill()
                except Exception:
                    pass
            except Exception:
                pass

    def on_crash(self):
        # Só mostra o botão se o processo foi encerrado
        self.label.config(text="")
        self.reconnect_btn.place(relx=0.5, rely=0.5, anchor="center")


def on_close():
    for cam in cameras:
        cam.kill_process()
    root.destroy()


def periodic_refocus():
    try:
        dummy.focus_set()
        # root.focus_force()
    except:
        pass
    root.after(2000, periodic_refocus)


def toggle_fullscreen(event=None):
    global fullscreen, last_geometry
    fullscreen = not fullscreen
    if fullscreen:
        last_geometry = root.geometry()
        root.attributes("-fullscreen", True)
    else:
        root.attributes("-fullscreen", False)
        if last_geometry:
            root.geometry(last_geometry)


root = tk.Tk()
root.title("Mosaico RTSP")
root.geometry("640x400")
root.geometry(f"{COLS*320}x{ROWS*240}")
root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", lambda e: on_close())


for r in range(ROWS):
    root.rowconfigure(r, weight=1)
for c in range(COLS):
    root.columnconfigure(c, weight=1)

for idx, cam in enumerate(ALL_CAMERAS):
    url = f"rtsp://{DVR_IP}:{DVR_PORT}/cam/realmonitor?channel={cam}&subtype={RES}&unicast=true&proto=Onvif"
    stream = Camera(root, rtsp_url=url, index=cam)
    cameras.append(stream)
    r = idx // COLS
    c = idx % COLS
    stream.frame.grid(row=r, column=c, sticky="nsew", padx=GAP, pady=GAP)


dummy = tk.Label(root)
dummy.pack_forget()
dummy.focus_set()

periodic_refocus()

root.mainloop()
