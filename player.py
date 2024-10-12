#Defines the Player class, handling player attributes, movement, and animations.

import pygame

class Player:
    def __init__(self, x, y):
        # Load the player image (ball-shaped image)
        try:
            self.original_image = pygame.image.load('assets/images/character.png')
            self.original_image = pygame.transform.scale(self.original_image, (50, 50))  # Scale the ball to 50x50
            self.image = self.original_image  # Keep a copy of the original image for rotation
            print("Player (ball) image loaded and scaled successfully")

        except pygame.error as e:
            print(f"Error loading player image: {e}")
            raise SystemExit

        self.rect = self.image.get_rect()
        self.rect.x = x  # Initial horizontal position
        self.rect.y = y  # Initial vertical position
        self.velocity_y = 0  # Vertical velocity for jumping
        self.jumping = False  # Whether the player is jumping
        self.angle = 0  # Angle of rotation for rolling effect
        self.rotation_speed = 5  # Speed at which the ball rotates when moving

    def handle_keys(self):
        # Handle left and right movement with ball rolling effect
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5  # Move the player to the left
            self.angle += self.rotation_speed  # Increase the angle for rotation (counter-clockwise)
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5  # Move the player to the right
            self.angle -= self.rotation_speed  # Decrease the angle for rotation (clockwise)

    def jump(self):
        # Handle jump when the player presses spacebar
        if not self.jumping:  # Player can jump only when not already jumping
            self.jumping = True  # Set jumping to True
            self.velocity_y = -10  # Set an initial upward velocity for jump

    def apply_gravity(self):
        # Apply gravity to make the player fall downwards after jumping
        self.velocity_y += 0.5  # Gradually increase the vertical speed to simulate gravity
        self.rect.y += self.velocity_y  # Update player's vertical position

        # Prevent the player from falling off the screen (stop at ground level)
        if self.rect.y >= 500:  # If the player hits the ground (y = 500)
            self.rect.y = 500  # Reset the player position to ground
            self.jumping = False  # Allow the player to jump again

    def update(self):
        self.handle_keys()  # Check for key input for left and right movement
        self.apply_gravity()  # Apply gravity to update player's vertical position

        # Rotate the ball image based on the current angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)  # Rotate image
        self.rect = self.image.get_rect(center=self.rect.center)  # Recenter the ball's position

    def draw(self, screen):
        # Draw the player (ball) on the screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        