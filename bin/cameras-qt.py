#!/bin/env python3

import math
import time
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QDrag
from PyQt5.QtCore import QTimer, Qt, QMimeData


CAMERAS = [1, 11, 4, 2, 9, 3, 6, 7, 8]
DVR_IP = "10.216.62.6"
DVR_PORT = "554"
RES = 1

count = len(CAMERAS)
cols = int(math.ceil(math.sqrt(count)))
rows = int(math.ceil(count / cols))


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

        for index, cam in enumerate(CAMERAS):
            viewer = CameraViewer(cam)
            row = index // cols
            col = index % cols
            viewer.setAcceptDrops(True)
            self.layout.addWidget(viewer, row, col)
            self.viewers.append(viewer)
            self.original_positions[viewer] = (row, col)

    def toggle_fullscreen(self, viewer):
        if not self.fullscreen_mode:
            for v in self.viewers:
                if v != viewer:
                    v.hide()
            viewer.change_res(0)
            self.layout.addWidget(viewer, 0, 0, rows, cols)
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
                reply = QMessageBox.question(
                    self,
                    "Encerrar",
                    "Deseja realmente sair?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if reply == QMessageBox.Yes:
                    QApplication.quit()
            self._last_esc_time = now
        else:
            super().keyPressEvent(event)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        cam_id = int(e.mimeData().text())
        source = find_viewer_by_camera(cam_id)
        target_pos = layout.indexOf(self).row(), layout.indexOf(self).column()
        swap_layout_positions(source, self)
        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MosaicoRTSP()
    window.showMaximized()
    sys.exit(app.exec_())
