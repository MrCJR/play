import os
from tkinter import filedialog

# 文件管理类，用于打开文件对话框并记录上次打开的目录
class FileManager:
    def __init__(self):
        # 初始化上次打开的目录为当前目录
        self.last_opened_dir = "."

    def open_file(self):
        # 根据操作系统设置默认的初始目录为下载文件夹
        if os.name == 'nt':
            self.last_opened_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads')
        elif os.name == 'posix':
            self.last_opened_dir = os.path.join(os.environ['HOME'], 'Downloads')
        # 弹出文件选择对话框
        filename = filedialog.askopenfilename(
            title="打开文件",
            filetypes=(("视频文件", "*.mp4 *.avi *.mkv *.mov"), ("所有文件", "*.*")),
            initialdir=self.last_opened_dir
        )
        if filename:
            # 若用户选择了文件，更新上次打开的目录
            self.last_opened_dir = os.path.dirname(filename)
        return filename