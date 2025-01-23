import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

# 渲染器类，用于将解码后的视频帧渲染到窗口上
class Renderer:
    def __init__(self, parent):
        # 父窗口实例
        self.parent = parent
        # 创建用于显示视频帧的标签
        self.video_label = QLabel(parent)
        # 显示标签
        self.video_label.show()

    def render_video(self, frames, playing):
        for frame in frames:
            if not playing:
                # 若播放状态为停止，跳出循环
                break
            # 获取视频帧的高度、宽度和通道数
            height, width, channel = frame.shape
            # 计算每行字节数
            bytes_per_line = 3 * width
            # 将 numpy 数组转换为 QImage 对象
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            # 将 QImage 对象转换为 QPixmap 对象
            pixmap = QPixmap.fromImage(q_img)
            # 在标签上显示 QPixmap 对象
            self.video_label.setPixmap(pixmap)
            # 更新父窗口
            self.parent.update()
            # 模拟帧率，暂停 40 毫秒
            cv2.waitKey(40)