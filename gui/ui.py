import os
from PySide6.QtWidgets import QApplication
from core.player import Player
from PySide6.QtCore import QFile, QTextStream

def load_stylesheet(qss_file):
    """加载 QSS 样式表"""
    qss_path = os.path.join(os.path.dirname(__file__), "static", "qss", qss_file)

    try:
        with open(qss_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"QSS file not found: {qss_path}")
        return ""

def create_app():
    app = QApplication([])
    app.setStyleSheet(load_stylesheet("style.qss")) #加载样式表
    player = Player()
    return app,player