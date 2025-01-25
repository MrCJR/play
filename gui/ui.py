import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PySide6.QtMultimediaWidgets import QVideoWidget
from core.player import Player  # 请确保 core.player 路径正确
from core.file import FileHandler  # 导入文件选择逻辑


class PlayerUI(Player):
    """
    媒体播放器 UI，负责界面布局。
    """

    def __init__(self):
        super().__init__()
        self.init_player()  # 确保播放器组件初始化
        self.init_ui()
        self.set_default_size()  # 设置默认窗口大小

    def init_ui(self):
        """
        初始化 UI 界面。
        """
        # 视频组件
        self.video_widget = QVideoWidget()
        self.media_player.setVideoOutput(self.video_widget)

        # 选择文件按钮
        self.select_file_button = QPushButton("选择文件")
        self.select_file_button.clicked.connect(self.open_file)

        # 播放/暂停按钮
        self.play_button = QPushButton("播放/暂停")
        self.play_button.clicked.connect(self.toggle_play)

        # 音量滑块
        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Horizontal)  # 水平滑动
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        # 在初始化时同步播放音量
        self.set_volume(self.volume_slider.value())

        # 状态标签
        self.status_label = QLabel("No file loaded")

        # 布局设置
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.select_file_button)
        controls_layout.addWidget(self.volume_slider)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def set_default_size(self):
        """
        设置默认窗口大小。
        """
        self.resize(800, 600)  # 设置窗口宽 800，高 600

    def toggle_play(self):
        """
        重写/继承逻辑控制播放或暂停。
        """
        super().toggle_play()  # 检查是否在父类中正确实现

    def set_volume(self, value):
        """
        设置播放器音量。
        """
        super().set_volume(value)  # 确保调用父类方法处理

    def open_file(self):
        """
        打开文件选择对话框，选择文件以播放。
        """
        file_handler = FileHandler()  # 使用 file.py 中的逻辑
        selected_file = file_handler.select_file()
        if selected_file:
            self.play_file(selected_file)

    @staticmethod
    def create_app():
        """
        初始化应用实例。
        """
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        player_ui = PlayerUI()
        return app, player_ui
