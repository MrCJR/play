import sys
from gui.main_window import MainWindow

if __name__ == '__main__':
    # 创建主窗口实例
    window = MainWindow()
    # 进入主循环
    window.run()
    sys.exit()