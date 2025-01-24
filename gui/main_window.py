import pygame
import pygame_menu
from core.decoder import VideoDecoder
from core.renderer import VideoRenderer
from core.av_sync import AVSync
from core.add_file import FileManager


class MainWindow:
    def __init__(self):
        pygame.init()
        # 设置窗口标题
        pygame.display.set_caption("媒体播放器")
        # 设置窗口大小
        self.screen = pygame.display.set_mode((800, 600))
        # 创建视频解码器实例
        self.decoder = None
        # 创建视频渲染器实例
        self.renderer = VideoRenderer(self.screen)
        # 创建音视频同步器实例
        self.av_sync = AVSync()
        # 初始化播放状态
        self.playing = False
        # 初始化当前文件路径
        self.current_file = None

        # 定义支持中文的字体
        font_path = pygame_menu.font.FONT_NEVIS
        # 创建自定义主题
        my_theme = pygame_menu.themes.THEME_BLUE.copy()
        my_theme.title_font = font_path
        my_theme.widget_font = font_path

        # 创建 pygame_menu 菜单
        self.menu = pygame_menu.Menu('媒体播放器', 800, 600,
                                     theme=my_theme)
        self.menu.add.button('打开文件', self.open_file)
        self.menu.add.button('退出', pygame_menu.events.EXIT)

        self.files = []


    def play_file(self, file_path):
        self.current_file = file_path
        # 创建视频解码器实例
        self.decoder = VideoDecoder(file_path)
        self.playing = True
        self.menu.disable()

    def open_file(self):
        self.menu.enable()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if self.menu.is_enabled():
                self.menu.update(events)
                self.menu.draw(self.screen)
            elif self.playing and self.decoder:
                # 解码视频帧
                frame = self.decoder.decode_frame()
                if frame:
                    # 同步音视频
                    self.av_sync.sync(frame)
                    # 渲染视频帧
                    self.renderer.render(frame)
            else:
                # 如果菜单未启用且未播放视频，清空屏幕
                self.screen.fill((0, 0, 0))

            pygame.display.flip()