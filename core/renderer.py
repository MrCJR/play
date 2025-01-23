import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer

class Renderer:
    def __init__(self, parent):
        # 父窗口实例
        self.parent = parent
        # 创建用于显示视频帧的标签
        self.video_label = QLabel(parent)
        # 显示标签
        self.video_label.show()
        # 初始化定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def render_video(self, frames, playing):
        self.frames = frames
        self.frame_index = 0
        self.playing = playing
        # 启动定时器，每 40 毫秒更新一帧
        self.timer.start(40)

    def update_frame(self):
        if not self.playing or self.frame_index >= len(self.frames):
            self.timer.stop()
            return
        frame = self.frames[self.frame_index]
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_label.setPixmap(pixmap)
        self.parent.update()
        self.frame_index += 1