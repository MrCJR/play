import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from core.file import FileManager
from core.decoder import Decoder
from core.renderer import Renderer

# 播放线程类，继承自 QThread，用于在单独线程中播放视频
class PlayThread(QThread):
    # 定义信号，用于通知主线程播放完成
    finished = pyqtSignal()
    # 定义信号，用于通知主线程播放过程中出现错误
    error = pyqtSignal(str)

    def __init__(self, decoder, renderer, filename):
        super().__init__()
        # 解码器实例
        self.decoder = decoder
        # 渲染器实例
        self.renderer = renderer
        # 要播放的视频文件路径
        self.filename = filename
        # 播放状态标志
        self.playing = True

    def run(self):
        try:
            # 调用解码器的 decode 方法对视频文件进行解码
            decoded_video = self.decoder.decode(self.filename, self.playing)
            if decoded_video is not None:
                # 若解码成功，调用渲染器的 render_video 方法渲染视频
                self.renderer.render_video(decoded_video, self.playing)
            else:
                # 若解码失败，发出错误信号
                self.error.emit("解码失败。")
        except Exception as e:
            # 捕获异常并发出错误信号
            self.error.emit(str(e))
        finally:
            # 无论播放是否成功，都发出播放完成信号
            self.finished.emit()

# 视频播放器窗口类，继承自 QWidget
class VideoPlayerWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 窗口标题
        self.title = "简易视频播放器"
        # 初始化界面
        self.initUI()
        # 文件管理器实例
        self.file_manager = FileManager()
        # 解码器实例
        self.decoder = Decoder()
        # 渲染器实例
        self.renderer = Renderer(self)
        # 播放状态标志
        self.playing = False

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle(self.title)
        # 创建垂直布局
        layout = QVBoxLayout()
        # 创建播放按钮
        self.play_button = QPushButton('播放', self)
        # 为播放按钮的点击事件绑定 _toggle_play 方法
        self.play_button.clicked.connect(self._toggle_play)
        # 将播放按钮添加到布局中
        layout.addWidget(self.play_button)
        # 创建用于显示视频文件名的标签
        self.label = QLabel('未加载文件', self)
        # 将标签添加到布局中
        layout.addWidget(self.label)
        # 设置窗口的布局
        self.setLayout(layout)

    def _toggle_play(self):
        if not self.playing:
            # 若当前未播放，弹出文件选择对话框
            filename, _ = QFileDialog.getOpenFileName(self, '打开文件')
            if filename:
                # 若用户选择了文件，更新标签显示文件名
                self.label.setText(f"正在播放: {filename}")
                # 更新播放状态标志
                self.playing = True
                # 更新播放按钮文本为“暂停”
                self.play_button.setText("暂停")
                # 创建播放线程实例
                self.play_thread = PlayThread(self.decoder, self.renderer, filename)
                # 为播放完成信号绑定 _play_finished 方法
                self.play_thread.finished.connect(self._play_finished)
                # 为错误信号绑定 _play_error 方法
                self.play_thread.error.connect(self._play_error)
                # 启动播放线程
                self.play_thread.start()
        else:
            # 若当前正在播放，更新播放状态标志
            self.playing = False
            # 更新播放按钮文本为“播放”
            self.play_button.setText("播放")

    def _play_finished(self):
        # 播放完成后，更新播放状态标志
        self.playing = False
        # 更新播放按钮文本为“播放”
        self.play_button.setText("播放")

    def _play_error(self, error_msg):
        from PyQt5.QtWidgets import QMessageBox
        # 弹出错误消息框显示错误信息
        QMessageBox.critical(self, "错误", error_msg)
        # 更新播放状态标志
        self.playing = False
        # 更新播放按钮文本为“播放”
        self.play_button.setText("播放")