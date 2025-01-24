import os
import tkinter as tk
from tkinter import filedialog


class FileManager:
    def __init__(self):
        pass

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        # 根据不同操作系统获取默认下载文件夹
        if os.name == 'nt':  # Windows
            default_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        elif os.name == 'posix':  # Linux 或 macOS
            default_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        else:
            default_dir = os.getcwd()
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(
            initialdir=default_dir,
            filetypes=[("媒体文件", "*.mp3;*.mp4;*.avi;*.mkv")]
        )
        return file_path