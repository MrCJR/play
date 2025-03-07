import sys
from gui.ui import PlayerUI
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player_ui = PlayerUI()
    player_ui.show()
    sys.exit(app.exec())