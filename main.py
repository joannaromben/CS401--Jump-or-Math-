import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from player import Player
from footing import Footing  # Platform renamed as Footing

pygame.init()

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump or Math")


clock = pygame.time.Clock()

# Create player object (ball) at starting position
player = Player(100, 500)

# Create footing object (platform) at position
footing = Footing(200, 400)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()  # Make the player jump when spacebar is pressed

    # Update player state
    player.update()

    # Fill the screen with a light blue background
    screen.fill((135, 206, 235))

    # Draw footing (platform) and player (ball)
    footing.draw(screen)
    player.draw(screen)

    # Update the display
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

