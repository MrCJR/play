from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import os
import logging
# 导入 FileHandler 类
from core.file import FileHandler


# 设置日志基础配置
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)


class Player(QWidget):
    """
    媒体播放器组件,负责播放逻辑和信号处理。
    """

    def __init__(self):
        super().__init__()
        self.init_player()
        # 初始化 FileHandler 实例
        self.file_handler = FileHandler()

    def init_player(self):
        """
        初始化播放器逻辑和状态。
        """
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)

        # 播放器状态
        self.is_playing = False
        self.current_file = None

        # 信号绑定
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)
        self.media_player.playbackStateChanged.connect(self.update_play_state)

    def handle_media_status(self, status):
        """
        处理媒体状态事件。
        """
        if status == QMediaPlayer.MediaStatus.InvalidMedia:
            QMessageBox.critical(self, "错误", "加载媒体失败.")
            logging.error(f"无效的媒体资源: {self.current_file}")

    def update_play_state(self, state):
        """
        更新播放状态。
        """
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.is_playing = False
        elif state == QMediaPlayer.PlaybackState.PlayingState:
            self.is_playing = True

    def play_file(self, file_path):
        """
        加载并播放媒体文件。
        """
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "错误", f"未找到文件: {file_path}")
            return

        try:
            url = QUrl.fromLocalFile(file_path)
            self.media_player.setSource(url)
            self.media_player.play()
            self.current_file = file_path
            self.is_playing = True
        except Exception as e:
            QMessageBox.critical(self, "错误", f"播放文件时出错: {e}")
            logging.error(str(e))

    def toggle_play(self):
        """
        切换播放/暂停状态。
        """
        if self.is_playing:
            self.media_player.pause()
            self.is_playing = False
        else:
            self.media_player.play()
            self.is_playing = True

    def set_volume(self, value):
        """
        设置播放音量。
        """
        self.audio_output.setVolume(value / 100)

    def open_file(self):
        """
        打开文件选择对话框。
        """
        # 使用 FileHandler 的 select_file 方法获取文件路径
        file_path = self.file_handler.select_file()
        if file_path:
            self.play_file(file_path)