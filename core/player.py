import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QMessageBox
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon


def load_icon(icon_name):
    """
    加载图标函数。
    参数:
        icon_name (str): 图标文件名称。
    返回:
        QIcon: 如果文件存在，返回QIcon；否则返回空图标，并打印通知。
    """
    icon_path = os.path.join(os.path.dirname(__file__), "static", "icons", icon_name)
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    else:
        print(f"Icon not found: {icon_path}")
        return QIcon()  # 返回空的 QIcon，避免程序崩溃。


class Player(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化音频播放和输出组件
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # 播放/暂停按钮
        self.play_button = QPushButton()
        self.play_button.setIcon(load_icon("play.png"))
        self.play_button.clicked.connect(self.toggle_play)

        # 音量滑块
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)  # 音量范围 0 - 100
        self.volume_slider.setValue(50)  # 初始设置为 50%
        self.set_volume(50)  # 保证实际音量与滑块同步
        self.volume_slider.valueChanged.connect(self.set_volume)

        # 控件布局
        controls_layout = QHBoxLayout()  # 播放按钮和音量滑块的水平布局
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.volume_slider)

        main_layout = QVBoxLayout()  # 总布局，包含控件布局
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)

        # 初始化播放器状态变量
        self.is_playing = False  # 当前是否正在播放
        self.current_file = None  # 当前加载的音频文件路径

    def play_file(self, file_path):
        """
        加载并播放指定的音频文件。
        参数:
            file_path (str): 音频文件路径。
        """
        if not os.path.exists(file_path):  # 检查文件是否存在
            print(f"File not found: {file_path}")
            QMessageBox.warning(self, "Error", f"File not found: {file_path}")
            return

        try:
            # 配置 QMediaPlayer 的播放源
            url = QUrl.fromLocalFile(file_path)
            self.media_player.setSource(url)
            self.media_player.play()

            # 更新按钮图标和状态变量
            self.is_playing = True
            self.current_file = file_path
            self.play_button.setIcon(load_icon("pause.png"))
        except Exception as e:
            print(f"Error playing file: {e}")
            QMessageBox.critical(self, "Error", f"Error playing file: {e}")

    def toggle_play(self):
        """
        切换播放/暂停状态。
        """
        if self.current_file is None:  # 未加载文件时，提示用户
            print("No audio file loaded.")
            QMessageBox.information(self, "Info", "No audio file loaded.")
            return

        if self.is_playing:
            # 暂停播放
            self.media_player.pause()
            self.play_button.setIcon(load_icon("play.png"))
            self.is_playing = False
        else:
            # 开始播放
            self.media_player.play()
            self.play_button.setIcon(load_icon("pause.png"))
            self.is_playing = True

    def set_volume(self, value):
        """
        设置播放音量。
        参数:
            value (int): 音量值，范围为 0 - 100。
        """
        self.audio_output.setVolume(value / 100)  # QAudioOutput 的音量范围为 0.0 - 1.0
        print(f"Volume set to {value}%")  # 调试信息，可改为在界面中显示音量值

    def closeEvent(self, event):
        """
        关闭窗口时释放资源，避免内存泄漏。
        """
        self.media_player.stop()  # 停止播放
        self.media_player.deleteLater()  # 删除播放器对象
        self.audio_output.deleteLater()  # 删除音频输出对象
        super().closeEvent(event)  # 调用基类的关闭事件


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建播放器窗口
    player = Player()
    player.setWindowTitle("Audio Player")
    player.resize(300, 100)
    player.show()

    # 播放指定文件（测试用）
    # player.play_file("example_audio.mp3")  # 替换为实际存在的音频文件路径

    sys.exit(app.exec())
