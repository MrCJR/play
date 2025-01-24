import sys
from gui.ui import create_app

if __name__ == "__main__":
    app,player = create_app()
    player.show()
    if len(sys.argv) > 1:
        player.play_file(sys.argv[1])
    sys.exit(app.exec())