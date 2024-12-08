"""
Platform Class
Handles the platforms that the player can jump on.
Includes both static and moving platforms with collision detection.

Features:
- Static platforms for basic gameplay
- Moving platforms that travel horizontally
- Automatic removal when platforms move off screen
- Platform width variation for gameplay variety
"""

import pygame
from game.resource_manager import ResourceManager
from game.constants import PLATFORM_SPEED, SCREEN_WIDTH

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        """
        Initialize platform sprite
        Args:
            x (int): Initial x position
            y (int): Initial y position
            width (int): Platform width in pixels
            moving (bool): Whether platform moves horizontally
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ResourceManager.platform_image, (width, 12))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.moving = moving
        self.direction = 1 if moving else 0  # Direction for moving platforms
        self.speed = PLATFORM_SPEED if moving else 0  # Speed for moving platforms

    def update(self, scroll):
        """
        Update platform position
        Args:
            scroll (int): Amount to scroll vertically
        
        Handles:
        - Horizontal movement for moving platforms
        - Screen boundary checks
        - Vertical scrolling
        - Off-screen removal
        """
        # Handle platform movement for moving platforms
        if self.moving:
            next_x = self.rect.x + (self.direction * self.speed)
            # Reverse direction at screen edges
            if next_x <= 0:
                self.direction = 1
                self.rect.x = 0
            elif next_x + self.width >= SCREEN_WIDTH:
                self.direction = -1
                self.rect.x = SCREEN_WIDTH - self.width
            else:
                self.rect.x = next_x

        # Update vertical position with screen scroll
        self.rect.y += scroll

        # Remove platform if it moves off the top of the screen
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()