#!/bin/env python3

import os
import math
import time
import sys
import cv2
import configparser
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QMessageBox,
    QInputDialog,
    QMenu,
    QAction,
    QSplashScreen,
)
from PyQt5.QtGui import QImage, QPixmap, QDrag
from PyQt5.QtCore import QTimer, Qt, QMimeData

ALL_CAMERAS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
DVR_IP = "10.216.62.6"
DVR_PORT = "554"
RES = 1

CONFIG_FILE = os.path.expanduser("~/.config/cameras-qt/config.ini")


# count = len(IALLCAMERAS)
# cols = int(math.ceil(math.sqrt(count)))
# rows = int(math.ceil(count / cols))


class CameraViewer(QLabel):
    def __init__(self, camera):
        super().__init__()
        self.rtsp_url = ""
        self.camera = camera
        self.res = RES
        self.setScaledContents(True)
        self.setStyleSheet("background-color: black;")
        self.init_capture()
        self.last_esc_time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(25)  # fps

    def init_capture(self):
        self.cap = cv2.VideoCapture(self.init_camera(), cv2.CAP_GSTREAMER)

    def init_camera(self):
        self.rtsp_url = f"rtsp://{DVR_IP}:{DVR_PORT}/cam/realmonitor?channel={self.camera}&subtype={self.res}&unicast=true&proto=Onvif"
        gst = (
            f"rtspsrc location={self.rtsp_url} latency=0 ! "
            "rtph264depay ! avdec_h264 ! videoconvert ! appsink sync=false"
        )
        return gst

    def change_res(self, new_res):
        self.res = new_res
        self.cap.release()
        time.sleep(0.3)
        self.init_capture()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            time.sleep(0.5)
            self.init_capture()
            return
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.setPixmap(QPixmap.fromImage(img))

    def close(self):
        self.timer.stop()
        self.cap.release()

    def mouseDoubleClickEvent(self, event):
        self.parent().toggle_fullscreen(self)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.acceptProposedAction()

    def dropEvent(self, e):
        if not e.mimeData().hasText():
            return
        cam_id = int(e.mimeData().text())
        parent = self.parent()
        source = next((v for v in parent.viewers if v.camera == cam_id), None)
        target = self
        if source and source != target:
            parent.swap_viewers(source, target)
        e.acceptProposedAction()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drag_start_pos = e.globalPos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) and (
            e.globalPos() - self.drag_start_pos
        ).manhattanLength() > QApplication.startDragDistance():
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(str(self.camera))
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)


class MosaicoRTSP(QWidget):
    def __init__(self):
        super().__init__()
        self.cameras = []
        self.config = configparser.ConfigParser()
        self.load_config()

        count = len(self.cameras)
        self.cols = int(math.ceil(math.sqrt(count)))
        self.rows = int(math.ceil(count / self.cols))

        self.viewers = []
        self._last_esc_time = 0
        self.setWindowTitle("Mosaico RTSP")
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.viewers = []
        self.fullscreen_mode = False
        self.original_positions = {}
        self.current_fullscreen = None

        self.viewer_del = None

        self.reload_cameras()

    def toggle_fullscreen(self, viewer):
        if not self.fullscreen_mode:
            for v in self.viewers:
                if v != viewer:
                    v.hide()
            viewer.change_res(0)
            self.layout.addWidget(viewer, 0, 0, self.rows, self.cols)
            self.fullscreen_mode = True
            self.current_fullscreen = viewer
        else:
            viewer.change_res(1)
            for v in self.viewers:
                v.show()
            for v, (r, c) in self.original_positions.items():
                self.layout.addWidget(v, r, c)
            self.fullscreen_mode = False
            self.current_fullscreen = None

    def swap_viewers(self, viewer1, viewer2):
        r1, c1 = self.original_positions[viewer1]
        r2, c2 = self.original_positions[viewer2]

        self.layout.removeWidget(viewer1)
        self.layout.removeWidget(viewer2)

        self.layout.addWidget(viewer1, r2, c2)
        self.layout.addWidget(viewer2, r1, c1)

        self.original_positions[viewer1], self.original_positions[viewer2] = (r2, c2), (
            r1,
            c1,
        )

    def reorganize_grid(self):
        count = len(self.cameras)
        self.cols = int(math.ceil(math.sqrt(count)))
        self.rows = int(math.ceil(count / self.cols))
        self.original_positions.clear()
        for i, viewer in enumerate(self.viewers):
            self.layout.removeWidget(viewer)
            row = i // self.cols
            col = i % self.cols
            self.layout.addWidget(viewer, row, col)
            self.original_positions[viewer] = (row, col)

    def remove_camera(self, cam):
        self.viewer_del = None
        # encontra viewer
        viewer = next((v for v in self.viewers if v.camera == cam), None)
        if not viewer:
            return
        # remove do layout e fecha
        self.layout.removeWidget(viewer)
        viewer.close()
        viewer.deleteLater()
        # remove das listas
        self.viewers.remove(viewer)
        self.cameras.remove(cam)
        # reorganiza grid
        self.reorganize_grid()
        # salva config
        self.save_config()

    def add_camera(self, cam):
        if cam in self.cameras:
            return
        viewer = CameraViewer(cam)
        viewer.setAcceptDrops(True)
        self.viewers.append(viewer)
        self.cameras.append(cam)
        # recalcula grid
        count = len(self.cameras)
        self.cols = int(math.ceil(math.sqrt(count)))
        self.rows = int(math.ceil(count / self.cols))
        # adiciona no layout na última posição
        index = len(self.viewers) - 1
        row = index // self.cols
        col = index % self.cols
        viewer.setAcceptDrops(True)
        self.layout.addWidget(viewer, row, col)
        self.original_positions[viewer] = (row, col)
        self.save_config()

    def closeEvent(self, event):
        for viewer in self.viewers:
            viewer.close()
        event.accept()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_F11) or (
            event.key() == Qt.Key_F and event.modifiers() & Qt.ControlModifier
        ):
            # alterna fullscreen da janela inteira
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        elif event.key() == Qt.Key_Escape:
            now = time.time()
            if self.fullscreen_mode:
                # Sai do fullscreen do viewer atual
                self.toggle_fullscreen(self.current_fullscreen)
            if hasattr(self, "_last_esc_time") and (now - self._last_esc_time) < 1.0:
                self.do_exit()
            self._last_esc_time = now
        else:
            super().keyPressEvent(event)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        cam_id = int(e.mimeData().text())
        source = find_viewer_by_camera(cam_id)
        # target_pos = layout.indexOf(self).row(), layout.indexOf(self).column()
        swap_layout_positions(source, self)
        e.accept()

    def do_exit(self):
        reply = QMessageBox.question(
            self,
            "Encerrar",
            "Deseja realmente sair?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            QApplication.quit()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            self.config.read(CONFIG_FILE)
            if "Cameras" in self.config:
                cameras_str = self.config["Cameras"].get("order", "")
                if cameras_str:
                    self.cameras = list(map(int, cameras_str.split(",")))
                else:
                    self.cameras = ALL_CAMERAS.copy()
            else:
                self.cameras = ALL_CAMERAS.copy()
        else:
            self.cameras = ALL_CAMERAS.copy()

    def save_config(self):
        if "Cameras" not in self.config:
            self.config["Cameras"] = {}
        self.config["Cameras"]["order"] = ",".join(str(cam) for cam in self.cameras)
        config_dir = os.path.dirname(CONFIG_FILE)
        os.makedirs(config_dir, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            self.config.write(f)

    def contextMenuEvent(self, event):
        widget_clicado = self.childAt(event.pos())
        menu = QMenu(self)
        add_action = QAction("Adicionar câmera", self)
        remove_action = QAction("Remover câmera", self)
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.do_exit)
        add_action.triggered.connect(self.add_camera_dialog)
        if isinstance(widget_clicado, CameraViewer):
            self.viewer_del = widget_clicado
            remove_action.setEnabled(True)
        else:
            self.viewer_del = None
            remove_action.setEnabled(False)
        remove_action.triggered.connect(self.remove_camera_dialog)
        menu.addAction(add_action)
        menu.addAction(remove_action)
        menu.addAction(exit_action)
        menu.exec(event.globalPos())

    def add_camera_dialog(self):

        disponiveis = [str(c) for c in ALL_CAMERAS if c not in self.cameras]
        if not disponiveis:
            QMessageBox.information(
                self, "Nenhuma disponível", "Todas as câmeras já foram adicionadas."
            )
            return
        cam_str, ok = QInputDialog.getItem(
            self, "Adicionar câmera", "Escolha a câmera:", disponiveis, 0, False
        )
        if ok and cam_str:
            self.add_camera(int(cam_str))

    def remove_camera_dialog(self):
        if self.viewer_del is None:
            return
        if not self.cameras:
            return

        reply = QMessageBox.question(
            self,
            "Remover câmera",
            "Deseja remover esta câmera?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # self.remover_viewer(self.viewer_selecionado_para_remocao)
            cam = self.viewer_del.camera
            self.remove_camera(cam)

    def reload_cameras(self):
        for v in self.viewers:
            v.close()
            self.layout.removeWidget(v)
            v.deleteLater()
        self.viewers.clear()
        count = len(self.cameras)
        self.cols = int(math.ceil(math.sqrt(count)))
        self.rows = int(math.ceil(count / self.cols))
        self.original_positions.clear()

        for index, cam in enumerate(self.cameras):
            viewer = CameraViewer(cam)
            row = index // self.cols
            col = index % self.cols
            viewer.setAcceptDrops(True)
            self.layout.addWidget(viewer, row, col)
            self.viewers.append(viewer)
            self.original_positions[viewer] = (row, col)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pixmap = QPixmap(400, 200)
    pixmap.fill(Qt.black)

    # splash = QSplashScreen(pixmap)
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.showMessage(
        "Carregando Câmeras...", Qt.AlignBottom | Qt.AlignCenter, Qt.white
    )
    splash.show()

    window = MosaicoRTSP()
    window.showMaximized()

    splash.finish(window)  # fecha o splash depois que a janela abriu

    sys.exit(app.exec_())
