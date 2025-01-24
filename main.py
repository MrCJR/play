# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import VideoPlayerWindow

# 程序入口
if __name__ == "__main__":
    # 创建 PyQt5 应用程序实例
    app = QApplication(sys.argv)
    # 创建视频播放器窗口实例
    window = VideoPlayerWindow()
    # 显示窗口
    window.show()
    # 进入应用程序的主循环，直到窗口关闭
    sys.exit(app.exec_())