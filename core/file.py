import os
import platform
from PySide6.QtWidgets import QFileDialog


class FileHandler:
    """
    文件处理逻辑，包括选择文件。
    """

    @staticmethod
    def get_default_download_folder():
        """
        获取默认的下载文件夹路径，根据不同的操作系统确定路径。
        """
        system = platform.system()
        if system == "Windows":
            return os.path.join(os.environ["USERPROFILE"], "Downloads")
        elif system == "Darwin":  # macOS
            return os.path.join(os.environ["HOME"], "Downloads")
        else:  # Linux 或其他系统
            return os.path.join(os.environ["HOME"], "Downloads")

    def select_file(self):
        """
        打开文件选择对话框，默认打开下载文件夹。
        """
        default_folder = self.get_default_download_folder()
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Select Media File", default_folder, "Media Files (*.mp3 *.wav *.ogg *.mp4 *.avi *.mkv)"
        )
        return file_path
