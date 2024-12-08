"""
Player Class
Handles the player character's movement, jumping mechanics,
collision detection with platforms, and sprite rendering.
"""

import pygame
from game.constants import GRAVITY, SCREEN_WIDTH, SCROLL_THRESH, platform_group
from game.resource_manager import ResourceManager

class Player:
    def __init__(self, x, y):
        """
        Initialize player sprite
        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        self.image = pygame.transform.scale(ResourceManager.jumpy_image, (80, 80))
        self.width = 45
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.jumping = False
        self.flip = False

    def jump(self):
        """
        Make the player jump if not already jumping
        Returns:
            bool: True if jump initiated, False if already jumping
        """
        if not self.jumping:
            self.vel_y = -20
            self.jumping = True
            return True
        return False

    def move(self):
        """
        Handle player movement, including keyboard input,
        gravity, collisions, and screen scrolling.
        Returns:
            int: Amount of screen scroll
        """
        dx = 0
        dy = 0
        scroll = 0

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -10
            self.flip = True
        if keys[pygame.K_RIGHT]:
            dx = 10
            self.flip = False

        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Check screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # Platform collision detection
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < platform.rect.centery and self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = 0
                    self.jumping = False

        # Screen scrolling
        if self.rect.top <= SCROLL_THRESH and self.vel_y < 0:
            scroll = -dy

        # Update position
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll

    def draw(self, screen):
        """
        Draw the player sprite
        Args:
            screen: Pygame surface to draw on
        """
        screen.blit(pygame.transform.flip(self.image, self.flip, False), 
                   (self.rect.x - 12, self.rect.y - 5))