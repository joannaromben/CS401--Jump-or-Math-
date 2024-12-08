"""
Enemy Class
Handles different types of enemies in the game.
Each enemy type has unique properties and behaviors:
- Whale: Ocean stage enemy with basic movement
- Bird: Sky stage enemy with faster movement
- Fireball: Space stage enemy with wave motion
- Symbol: Math stage enemy with special movement pattern

Includes animation handling, movement patterns, and collision detection.
"""

import pygame
import math
from game.constants import ENEMY_SPEED, SCREEN_WIDTH
from game.resource_manager import ResourceManager
from game.constants import current_background

class Enemy(pygame.sprite.Sprite):
    def __init__(self, y_pos, current_background):
        """
        Initialize enemy sprite with type-specific properties
        Args:
            y_pos (int): Initial vertical position
            current_background (int): Current game stage (0-3)
        """
        pygame.sprite.Sprite.__init__(self)
        # Set enemy properties based on current game stage
        if current_background == 0:  # Ocean stage
            self.enemy_type = 'whale'
            frames = ResourceManager.whale_frames
            self.scale = 1.4
            self.speed = ENEMY_SPEED
            self.animation_speed = 0.1
            self.flip_offset = False
        elif current_background == 1:  # Sky stage
            self.enemy_type = 'bird'
            frames = ResourceManager.bird_frames
            self.scale = 0.6
            self.speed = ENEMY_SPEED * 1.2  # Birds move faster
            self.animation_speed = 0.1
            self.flip_offset = True
        elif current_background == 2:  # Space stage
            self.enemy_type = 'fireball'
            frames = ResourceManager.fireball_frames
            self.scale = 1.2
            self.speed = ENEMY_SPEED * 1.3  # Fireballs move fastest
            self.animation_speed = 0.15
            self.flip_offset = False
        elif current_background == 3:  # Math stage
            self.enemy_type = 'symbol'
            frames = ResourceManager.symbol_frames
            self.scale = 2.0
            self.speed = ENEMY_SPEED * 1.2
            self.animation_speed = 0.15
            self.flip_offset = False

        # Initialize animation frames with proper scaling
        self.original_frames = frames.copy()
        self.original_frames = [pygame.transform.scale(frame, (
            int(frame.get_width() * self.scale),
            int(frame.get_height() * self.scale)
        )) for frame in self.original_frames]
        
        # Set initial frame direction based on enemy type
        if self.flip_offset:
            self.frames = self.original_frames
        else:
            self.frames = [pygame.transform.flip(frame, True, False) 
                          for frame in self.original_frames]

        # Setup animation state
        self.current_frame = 0
        self.counter = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        # Adjust collision box to be smaller than visual size
        collision_shrink = 0.7
        new_width = int(self.rect.width * collision_shrink)
        new_height = int(self.rect.height * collision_shrink)
        self.image_rect = self.rect.copy()  # Save original size for drawing

        # Center the collision box
        x_offset = (self.rect.width - new_width) // 2
        y_offset = (self.rect.height - new_height) // 2
        self.rect = pygame.Rect(
            self.rect.x + x_offset,
            self.rect.y + y_offset,
            new_width,
            new_height
        )

        # Set initial position and movement
        self.direction = 1
        self.rect.x = -self.rect.width
        self.world_y = y_pos
        self.rect.y = y_pos

    def update(self, scroll):
        """
        Update enemy position and animation
        Args:
            scroll (int): Current screen scroll amount
        """
        # Update animation frame
        self.counter += self.animation_speed
        if self.counter >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.counter = 0

        # Update vertical position with screen scroll
        self.world_y += scroll
        self.rect.y = self.world_y

        # Apply special movement patterns for different enemy types
        if self.enemy_type == 'symbol':
            # Math symbols move in sine wave pattern
            self.rect.x += self.speed * self.direction
            self.rect.y += math.sin(pygame.time.get_ticks() * 0.003) * 2
        elif self.enemy_type == 'fireball':
            # Fireballs have smaller wave motion
            self.rect.y += math.sin(pygame.time.get_ticks() * 0.005) * 2

        # Basic horizontal movement
        self.rect.x += self.speed * self.direction

        # Handle screen edge collisions and sprite flipping
        if self.rect.left >= SCREEN_WIDTH:
            self.direction = -1
            self.rect.x = SCREEN_WIDTH
            if self.flip_offset:
                self.frames = [pygame.transform.flip(frame, True, False) 
                              for frame in self.original_frames]
            else:
                self.frames = self.original_frames
        elif self.rect.right <= 0:
            self.direction = 1
            self.rect.x = -self.rect.width
            if self.flip_offset:
                self.frames = self.original_frames
            else:
                self.frames = [pygame.transform.flip(frame, True, False) 
                              for frame in self.original_frames]

        # Remove if enemy moves too far off screen
        if self.rect.top > pygame.display.get_surface().get_height() + 100:
            self.kill() 