"""
Resource Manager
Centralizes the loading and management of all game resources.
Provides static access to game assets including enemy animations,
player sprites, platform textures, and background images.

This manager ensures resources are loaded only once and shared
across all game components that need them.
"""

import pygame

class ResourceManager:
    # Static resource variables for game assets
    whale_frames = None     # Ocean enemy animation frames
    bird_frames = None      # Sky enemy animation frames
    fireball_frames = None  # Space enemy animation frames
    symbol_frames = None    # Math enemy animation frames
    
    jumpy_image = None      # Player character sprite
    platform_image = None   # Platform texture
    background_images = []  # List of background images for different stages

    @classmethod
    def initialize(cls):
        """
        Initialize and load all game resources.
        Must be called before any game objects are created.
        """
        # Load enemy animation frames
        cls.whale_frames = cls.load_enemy_frames('whale', 6)
        cls.bird_frames = cls.load_enemy_frames('bird', 4)
        cls.fireball_frames = cls.load_enemy_frames('fireball', 9)
        cls.symbol_frames = cls.create_symbol_frames()
        
        # Load player and platform images
        cls.jumpy_image = cls.load_image('assets/images/player.png')
        cls.platform_image = cls.load_image('assets/images/wood.png')
        
        # Load background images
        cls.load_backgrounds()

    @staticmethod
    def load_enemy_frames(prefix, count):
        """
        Load animation frames for an enemy type
        Args:
            prefix (str): Enemy type prefix for filename (whale/bird/fireball)
            count (int): Number of frames to load
        Returns:
            list: List of loaded frame images with fallback on error
        """
        frames = []
        for i in range(1, count + 1):
            try:
                frame = pygame.image.load(f'assets/images/{prefix}_frame_{i}.png').convert_alpha()
                frames.append(frame)
            except pygame.error as e:
                print(f"Error loading enemy frame {i}: {e}")
                # Create fallback frame on error
                fallback = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(fallback, (255, 0, 0), (25, 25), 25)
                frames.append(fallback)
        return frames

    @staticmethod
    def create_symbol_frames():
        """
        Create frames for math symbol enemies
        Returns:
            list: List of surfaces with rendered math symbols
        """
        frames = []
        symbols = ['+', '-', '×', '÷', '=']
        size = 60
        for symbol in symbols:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            font = pygame.font.SysFont('Arial', 40, bold=True)
            symbol_text = font.render(symbol, True, (255, 255, 255))
            text_rect = symbol_text.get_rect(center=(size // 2, size // 2))
            surface.blit(symbol_text, text_rect)
            frames.append(surface)
        return frames

    @staticmethod
    def load_image(filename, convert_alpha=True):
        """
        Load a single image file with error handling
        Args:
            filename (str): Path to image file
            convert_alpha (bool): Whether to convert alpha channel
        Returns:
            Surface: Loaded image surface or red square fallback
        """
        try:
            if convert_alpha:
                return pygame.image.load(filename).convert_alpha()
            return pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")
            surface = pygame.Surface((50, 50))
            surface.fill((255, 0, 0))
            return surface

    @classmethod
    def load_backgrounds(cls):
        """
        Load and scale background images for all game stages.
        Backgrounds are loaded in sequence and scaled to screen size.
        """
        from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        for i in range(1, 5):
            try:
                img = pygame.image.load(f'assets/images/bk{i}.png')
                img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                cls.background_images.append(img)
            except pygame.error as e:
                print(f"Error loading background {i}: {e}")
                # Create colored fallback background
                fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fallback.fill((i * 50, i * 50, i * 50))
                cls.background_images.append(fallback) 