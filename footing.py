import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height=50, is_ground=False):
        super().__init__()
        try:
            # 加载跳板图片并调整大小，包括自定义高度
            self.image = pygame.image.load('assets/images/platform.png')
            self.image = pygame.transform.scale(self.image, (width, height))  # 宽度和高度可变
        except pygame.error as e:
            print(f"Error loading platform image: {e}")
            # 如果图片加载失败，则使用颜色作为备用
            self.image = pygame.Surface((width, height))
            self.image.fill((0, 255, 0))  # 使用绿色填充作为跳板颜色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_ground = is_ground  # 判断是否是地面

    def update(self, scroll_speed):
        """跳板随着背景一起滚动"""
        if not self.is_ground:
            self.rect.y += scroll_speed

def generate_footings(num_footings, min_y=SCREEN_HEIGHT):
    """生成跳板，确保跳板的y坐标在屏幕上方"""
    footings = pygame.sprite.Group()
    y = min_y - 100  # 从指定的最小y坐标开始生成跳板
    for _ in range(num_footings):
        width = random.randint(100, 200)  # 跳板的宽度范围
        height = 50  # 设置跳板的高度
        x = random.randint(0, SCREEN_WIDTH - width)  # 随机生成 x 坐标
        y -= random.randint(60, 100)  # 跳板之间的垂直间距调整为 60 到 100 像素
        platform = Platform(x, y, width, height)  # 生成自定义高度的跳板
        footings.add(platform)
    return footings
