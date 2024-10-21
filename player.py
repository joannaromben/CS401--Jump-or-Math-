import pygame
from settings import PLAYER_SIZE, GRAVITY, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill((0, 0, 255))  # 蓝色的角色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0  # 垂直速度
        self.velocity_x = 0  # 水平速度
        self.jumping = False
        self.is_alive = True
        self.gravity = GRAVITY

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity_x = -5  # 向左移动
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = 5  # 向右移动
        else:
            self.velocity_x = 0  # 停止移动

    def jump(self):
        if not self.jumping and self.is_alive:
            self.velocity_y = -20  # 设置跳跃的速度
            self.jumping = True

    def apply_gravity(self):
        if self.is_alive:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

            if self.rect.top >= SCREEN_HEIGHT:
                self.is_alive = False
                self.velocity_y = 0
                self.velocity_x = 0

    def update(self, platforms, scroll_speed, ground_platform):
        self.handle_keys()
        self.apply_gravity()

        self.rect.x += self.velocity_x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.velocity_y > 0:  # 只有在下落时检测碰撞
            for platform in platforms:
                if pygame.sprite.collide_rect(self, platform):
                    # 改进碰撞检测，确保玩家底部和跳板顶部对齐
                    if self.rect.bottom <= platform.rect.top + 10 and self.rect.bottom >= platform.rect.top:
                        self.rect.bottom = platform.rect.top  # 精确对齐
                        self.velocity_y = 0  # 停止下落
                        self.jumping = False  # 重置跳跃状态
                        
                        # 如果碰到跳板且不是平地，则移除平地
                        if not platform.is_ground and ground_platform in platforms:
                            platforms.remove(ground_platform)

    def reset_position(self):
        self.rect.x = SCREEN_WIDTH // 2 - 25
        self.rect.y = SCREEN_HEIGHT - 170
        self.velocity_y = 0
        self.velocity_x = 0
        self.jumping = False
        self.is_alive = True
