#Defines the Platform class, handling the creation and interaction of platforms.

import pygame

class Footing:
    def __init__(self, x, y):
         # Try loading the platform image, handle error if image is missing
        try:
            self.image = pygame.image.load('assets/images/platform.png')
            print("Footing image loaded successfully")
            # Resize the image to 100x30 pixels
            self.image = pygame.transform.scale(self.image, (100, 30))  # Adjust size
        except pygame.error as e:
            print(f"Error loading footing image: {e}")
            raise SystemExit
        
        self.rect = self.image.get_rect()
        self.rect.x = x  # Set platform's initial horizontal position
        self.rect.y = y  # Set platform's initial vertical position

    def draw(self, screen):
        # Draw the platform on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

