"""
Background Manager
Handles the game's background rendering and transitions.
Manages loading, scaling, and smooth transitions between different background images
as the player progresses through different game stages.
"""

import pygame
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game.resource_manager import ResourceManager

class Background:
    def __init__(self, screen):
        """
        Initialize background manager
        Args:
            screen: Pygame surface to draw backgrounds on
        """
        self.screen = screen
        self.background_images = ResourceManager.background_images
        self.current_background = 0
        self.transition_active = False
        self.background_alpha = 255
        self.next_background = 0

    def draw(self, current_background, bg_scroll):
        """
        Draw the current background with scrolling effect
        Args:
            current_background (int): Index of current background
            bg_scroll (int): Current scroll position for parallax effect
        """
        try:
            # Draw two copies of the background for seamless scrolling
            self.screen.blit(self.background_images[current_background], 
                           (0, 0 + bg_scroll))
            self.screen.blit(self.background_images[current_background], 
                           (0, -SCREEN_HEIGHT + bg_scroll))
        except Exception as e:
            print(f"Error drawing background: {e}")

    def draw_transition(self, current_bg, next_bg, alpha, bg_scroll):
        """
        Draw transition between two backgrounds with fade effect
        Args:
            current_bg (int): Index of current background
            next_bg (int): Index of next background
            alpha (int): Transparency value for transition effect
            bg_scroll (int): Current scroll position for parallax effect
        """
        # Draw current background first
        self.draw(current_bg, bg_scroll)

        # Create temporary surface for alpha blending
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        temp_surface.blit(self.background_images[next_bg], (0, 0 + bg_scroll))
        temp_surface.blit(self.background_images[next_bg], (0, -SCREEN_HEIGHT + bg_scroll))
        temp_surface.set_alpha(alpha)
        self.screen.blit(temp_surface, (0, 0))