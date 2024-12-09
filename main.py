"""
Jump and Math - Main Entry Point
A platformer game that combines jumping mechanics with math challenges.
Players must solve math questions to continue after dying.
"""

import pygame
import sys
from game.game_manager import GameManager
from game.resource_manager import ResourceManager

def main():
    # Initialize Pygame engine and mixer with error handling
    try:
        pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    except pygame.error as e:
        print(f"Error initializing Pygame: {e}")
        sys.exit(1)

    # Initialize display screen
    try:
        screen = pygame.display.set_mode((500, 800))
        pygame.display.set_caption("Jump and Math")
    except pygame.error as e:
        print(f"Error setting up display: {e}")
        sys.exit(1)

    try:
        # Initialize resource manager
        ResourceManager.initialize()
        
        # Create game manager instance and run game
        game = GameManager(screen)
        
        # Main game loop
        running = True
        while running:
            running = game.run()

    except Exception as e:
        print(f"Error in main: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main() 