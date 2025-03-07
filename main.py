import sys
from gui.ui import PlayerUI


if __name__ == "__main__":
    app, player_ui = PlayerUI.create_app()

    # 如果传入文件路径,直接加载播放
    if len(sys.argv) > 1:
        player_ui.play_file(sys.argv[1])

    player_ui.show()
    sys.exit(app.exec())
