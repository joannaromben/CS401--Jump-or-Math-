import pygame
import sys
from player import Player
from footing import Platform, generate_footings
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump and Platform Game")

# Load and resize background images to fit the screen size
background_images = [
    pygame.transform.scale(pygame.image.load('assets/images/bk1.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/bk2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/bk3.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    pygame.transform.scale(pygame.image.load('assets/images/bk4.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
]

# Create the ground platform as the starting point of the game
ground = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, is_ground=True)

# Initialize the player object
player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 170)

# Initialize platforms (footings)
platforms = generate_footings(10)  # Initially generate 10 platforms
platforms.add(ground)  # Add the ground platform to the platform group

# Main game loop
running = True
scroll_speed = 0  # Scrolling speed
background_y_positions = [0, -SCREEN_HEIGHT, -2 * SCREEN_HEIGHT, -3 * SCREEN_HEIGHT]  # Y positions for each background image

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.is_alive:
                player.jump()

    # If the player is dead, show "You are dead" message and reset the game
    if not player.is_alive:
        font = pygame.font.SysFont(None, 55)
        text = font.render("You are dead!!", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds
        player.reset_position()  # Reset the player's position
        platforms = generate_footings(10)  # Reset platforms
        platforms.add(ground)  # Re-add the ground
        background_y_positions = [0, -SCREEN_HEIGHT, -2 * SCREEN_HEIGHT, -3 * SCREEN_HEIGHT]  # Reset background positions
        continue  # Skip rendering and move to the next frame

    # Scroll the background and platforms when the player jumps above the middle of the screen
    if player.rect.y < SCREEN_HEIGHT // 2:
        scroll_speed = abs(player.velocity_y)  # Scroll speed is proportional to the player's velocity
        player.rect.y = SCREEN_HEIGHT // 2  # Keep the player locked in the middle of the screen

        # Update each background's Y position
        for i in range(len(background_y_positions)):
            background_y_positions[i] += scroll_speed

            # When the background scrolls out of the screen, loop it back to the top to create a seamless transition
            if background_y_positions[i] >= SCREEN_HEIGHT:
                background_y_positions[i] = background_y_positions[(i - 1) % len(background_y_positions)] - SCREEN_HEIGHT

        # Remove platforms that are off the screen
        for platform in platforms:
            if platform.rect.top > SCREEN_HEIGHT:
                platforms.remove(platform)

        # Check if new platforms need to be generated when scrolling
        if len(platforms) < 10:  # Ensure enough platforms are present on the screen
            new_platforms = generate_footings(5, min_y=min([p.rect.y for p in platforms]))  # Generate new platforms above the current ones
            platforms.add(new_platforms)
    else:
        scroll_speed = 0

    # Draw the current background images in sequence
    for i, background_image in enumerate(background_images):
        screen.blit(background_image, (0, background_y_positions[i]))

    # Update and draw platforms
    platforms.update(scroll_speed)
    platforms.draw(screen)

    # Update and draw the player
    player.update(platforms, scroll_speed, ground)
    screen.blit(player.image, player.rect)

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit the frame rate to 60 FPS
