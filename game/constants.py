"""
Game Constants
Defines all constant values used throughout the game.
This includes game states, dimensions, physics settings,
score thresholds, colors, and shared sprite groups.

These constants are imported and used by various game components
to maintain consistent behavior across the game.
"""

import pygame

# Game states - Different screens/modes in the game
MENU = "menu"          # Main menu screen
PLAYING = "playing"    # Active gameplay
MATH_QUESTION = "math_question"  # Math question screen after death
HOW_TO_PLAY = "how_to_play"     # Instructions screen

# Window dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

# Game physics and mechanics settings
SCROLL_THRESH = 200    # Screen scrolling threshold
GRAVITY = 1           # Gravity force applied to player
MAX_PLATFORMS = 10    # Maximum number of platforms on screen
PLATFORM_GAP = 100    # Vertical gap between platforms

# Speed settings for game entities
ENEMY_SPEED = 2.0     # Base enemy movement speed
PLATFORM_SPEED = 1.5  # Moving platform speed
ENEMY_DISTANCE = 400  # Horizontal distance between enemies
ENEMY_VERTICAL_DISTANCE = 600  # Vertical distance between enemies

# Background transition settings
FADE_SPEED = 5  # Speed of background fade transitions

# Score thresholds for background changes
OCEAN_SCORE = 200   # Score needed for ocean to sky transition
SKY_SCORE = 400    # Score needed for sky to space transition
SPACE_SCORE = 600  # Score needed for space to math transition
MATH_SCORE = 800   # Final background threshold

# Button dimensions for menu interface
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Color definitions (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Frame rate setting
FPS = 60

# File paths
HIGH_SCORE_FILE = 'high_score.txt'

# Sprite groups shared across the game
platform_group = pygame.sprite.Group()  # Group for all platforms
enemy_group = pygame.sprite.Group()     # Group for all enemies

# Current background tracker
current_background = 0  # Tracks current background stage (0-3)