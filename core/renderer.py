import pygame
import cv2


class VideoRenderer:
    def __init__(self, screen):
        self.screen = screen

    def render(self, frame):
        # 将 OpenCV 图像转换为 Pygame 表面
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        # 在屏幕上绘制帧
        self.screen.blit(frame, (0, 0))