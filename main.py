import pygame
import sys
from player import Player
from footing import Platform, generate_footings
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# 初始化 Pygame
pygame.init()

# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump and Platform Game")

# 加载并调整背景图片的尺寸，使其与屏幕宽高一致
background_images = [
    pygame.transform.scale(pygame.image.load('assets/images/bk1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/bk2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/bk3.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/bk4.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
]

# 创建平地作为游戏开始时的起点
ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, is_ground=True)

# 初始化玩家对象
player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 170)

# 初始化跳板
platforms = generate_footings(10)  # 初始生成10个跳板
platforms.add(ground)  # 将平地添加到平台组

# 游戏主循环
running = True
scroll_speed = 0  # 滚动速度
background_y_positions = [0, -SCREEN_HEIGHT, -2 * SCREEN_HEIGHT, -3 * SCREEN_HEIGHT]  # 每张背景图片的 y 位置

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.is_alive:
                player.jump()

    # 如果玩家死亡，显示 "死亡提示" 并重置游戏
    if not player.is_alive:
        font = pygame.font.SysFont(None, 55)
        text = font.render("You are dead!!", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # 等待2秒
        player.reset_position()  # 重置玩家
        platforms = generate_footings(10)  # 重置跳板
        platforms.add(ground)  # 重新添加地面
        background_y_positions = [0, -SCREEN_HEIGHT, -2 * SCREEN_HEIGHT, -3 * SCREEN_HEIGHT]  # 重置背景位置
        continue  # 跳过下面的渲染，进入下一帧

    # 滚动背景和跳板，当玩家跳跃到屏幕中间以上时
    if player.rect.y < SCREEN_HEIGHT // 2:
        scroll_speed = abs(player.velocity_y)  # 滚动速度与玩家的速度成比例
        player.rect.y = SCREEN_HEIGHT // 2  # 锁定玩家在屏幕中间位置

        # 更新每个背景的 y 位置
        for i in range(len(background_y_positions)):
            background_y_positions[i] += scroll_speed

            # 当背景滚出屏幕时，循环将其移到最顶部，形成无缝衔接
            if background_y_positions[i] >= SCREEN_HEIGHT:
                background_y_positions[i] = background_y_positions[(i - 1) % len(background_y_positions)] - SCREEN_HEIGHT

        # 删除已经超出屏幕的跳板
        for platform in platforms:
            if platform.rect.top > SCREEN_HEIGHT:
                platforms.remove(platform)

        # 当背景滚动时，检查是否需要生成新的跳板
        if len(platforms) < 10:  # 保持屏幕上始终有足够的跳板
            new_platforms = generate_footings(5, min_y=min([p.rect.y for p in platforms]))  # 在现有跳板之上生成新的跳板
            platforms.add(new_platforms)
    else:
        scroll_speed = 0

    # 画当前的背景图片，顺序绘制
    for i, background_image in enumerate(background_images):
        screen.blit(background_image, (0, background_y_positions[i]))

    # 更新跳板位置并画跳板
    platforms.update(scroll_speed)
    platforms.draw(screen)

    # 更新并画玩家
    player.update(platforms, scroll_speed, ground)
    screen.blit(player.image, player.rect)

    # 更新显示
    pygame.display.flip()
    pygame.time.Clock().tick(60)
