import os
import platform
from PySide6.QtMultimedia import QMediaFormat
from PySide6.QtWidgets import QFileDialog

# 媒体格式对应文件扩展名映射表
FORMAT_TO_EXTENSION_MAP = {
    # 视频格式
    "MPEG-4": ["mp4"],
    "MPEG-4 audio": ["mp3", "m4a", "aac"],
    "Matroska": ["mkv"],
    "QuickTime": ["mov"],
    "Wave": ["wav"],
    "FLAC": ["flac"],
    "Windows Media": ["wmv"],
    "Ogg": ["ogg", "ogv", "oga", "ogx"],
    "AVI": ["avi"],
    "MPEG": ["mpeg", "mpg", "mpe"],
    "WebM": ["webm"],
    "3GPP": ["3gp", "3g2"],
    "Flash Video": ["flv"],
    "RealMedia": ["rm", "rmvb"],
    "HEIF": ["heif", "heic"],

    # 音频格式
    "MP3": ["mp3"],
    "AAC": ["aac"],
    "WMA": ["wma"],
    "WAV": ["wav"],
    "AIFF": ["aiff", "aif", "aifc"],
    "ALAC": ["m4a"],
    "MIDI": ["midi", "mid"],
    "AMR": ["amr"],
    "RealAudio": ["ra"],

    # 工程文件或流媒体
    "Playlist": ["m3u", "m3u8", "pls", "xspf"],
    "Streaming": ["ts"],
    "ISO Base Media": ["isml"],

    # 其他可能用到的格式
    "DV": ["dv"],
    "DivX": ["divx"],
    "MK3D": ["mk3d"],

    # 可进一步扩展...
}



class FileHandler:
    """
    文件处理逻辑,包括选择文件。
    """

    def __init__(self):
        # 初始化时创建 QMediaFormat 对象
        self.media_format = QMediaFormat()

    @staticmethod
    def get_default_download_folder():
        """
        获取默认的下载文件夹路径。
        """
        try:
            if platform.system() == "Windows":
                return os.path.join(os.environ.get("USERPROFILE", ""), "Downloads")
            else:
                return os.path.join(os.environ.get("HOME", ""), "Downloads")
        except Exception as e:
            print(f"Error retrieving download folder: {e}")
            return os.getcwd()


    def get_playable_formats(self):
        """
        获取系统支持的可播放文件格式
        :return: 支持的文件格式名称列表
        """
        try:
            # 获取系统支持解码的文件格式列表
            formats = self.media_format.supportedFileFormats(QMediaFormat.ConversionMode.Decode)
            extensions = []

            for fmt in formats:
                # 获取每个支持格式的名称
                format_name = QMediaFormat.fileFormatName(fmt)

                # 根据名称获取对应的文件扩展名，比较时忽略大小写
                format_name_lower = format_name.lower()
                if any(key.lower() == format_name_lower for key in FORMAT_TO_EXTENSION_MAP):
                    # 获取正确的key
                    matching_key = next(key for key in FORMAT_TO_EXTENSION_MAP if key.lower() == format_name_lower)
                    extensions.extend(FORMAT_TO_EXTENSION_MAP[matching_key])
            return list(set(extensions))  # 返回去重的扩展名列表
        except Exception as e:
            print(f"获取可播放格式时出错: {e}")
            return []

    def select_file(self):
        """
        打开文件选择对话框,默认打开下载文件夹。
        """
        default_folder = self.get_default_download_folder()
        playable_extensions = self.get_playable_formats()

        if not playable_extensions:  # 如果支持的格式为空
            playable_extensions = ["mp4", "mp3"]  # 默认为一些常见格式


        # 使用文件扩展名生成过滤器
        file_types = " ".join([f"*.{ext.lower()}" for ext in playable_extensions])
        filter_str = f"媒体文件类型 ({file_types})"

        print(filter_str)

        try:
            file_path, _ = QFileDialog.getOpenFileName(
                None, "查看媒体文件", default_folder, filter_str
            )
            return file_path if file_path else None
        except Exception as e:
            print(f"文件选择时出错: {e}")
            return None
