"""
Math Question Class
Handles the math question minigame that appears when the player dies.
Generates random arithmetic questions and validates player answers.

Features:
- Random question generation with multiple choice answers
- Visual feedback for selected answers
- Sound effects for correct/wrong answers
- Circular question display with button-style answers
"""

import pygame
import random
from game.constants import SCREEN_WIDTH, BLACK, WHITE, YELLOW

class MathQuestion:
    def __init__(self, screen, font):
        """
        Initialize math question interface
        Args:
            screen: Pygame surface to draw on
            font: Font to use for text rendering
        """
        self.screen = screen
        self.font = font
        self.question = ""
        self.correct_answer = 0
        self.options = []
        self.active = False
        self.selected_option = None
        self.option_rects = []

    def generate_question(self):
        """
        Generate a random arithmetic question.
        Creates a question using numbers 1-10 and basic operators (+, -, *).
        Generates four answer options, including the correct one.
        """
        # Generate random numbers and operator
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operator = random.choice(["+", "-", "*"])

        # Calculate correct answer based on operator
        if operator == "+":
            self.correct_answer = num1 + num2
        elif operator == "-":
            self.correct_answer = num1 - num2
        else:  # multiplication
            self.correct_answer = num1 * num2

        self.question = f"{num1} {operator} {num2} = ?"

        # Generate answer options including correct answer
        self.options = [self.correct_answer]
        while len(self.options) < 4:
            # Generate wrong answers within reasonable range
            wrong_answer = random.randint(max(0, self.correct_answer - 20), 
                                       self.correct_answer + 20)
            if wrong_answer not in self.options:
                self.options.append(wrong_answer)
        random.shuffle(self.options)

        self.active = True
        self.selected_option = None
        self.option_rects = []

    def handle_click(self, pos):
        """
        Handle mouse click on answer options
        Args:
            pos: Mouse click position (x, y)
        Returns:
            bool: True if correct answer clicked
            bool: False if wrong answer clicked
            None: If no option clicked or question not active
        """
        if not self.active:
            return None

        for i, rect in enumerate(self.option_rects):
            if rect.collidepoint(pos):
                self.selected_option = i
                if self.options[i] == self.correct_answer:
                    if pygame.mixer.get_init():
                        correct_sound = pygame.mixer.Sound('assets/sounds/correct.wav')
                        correct_sound.play()
                    return True
                else:
                    if pygame.mixer.get_init():
                        wrong_sound = pygame.mixer.Sound('assets/sounds/wrong.wav')
                        wrong_sound.play()
                    return False
        return None

    def draw(self):
        """
        Draw the math question interface.
        Includes:
        - Yellow circle with question text
        - Four answer option buttons
        - Visual feedback for selected option
        
        Returns:
            bool: Always returns False (historical behavior)
        """
        if not self.active:
            return False

        # Draw question circle
        circle_center = (SCREEN_WIDTH // 2, 200)
        circle_radius = 150
        pygame.draw.circle(self.screen, YELLOW, circle_center, circle_radius)

        # Draw question text
        question_text = self.font.render(self.question, True, BLACK)
        text_rect = question_text.get_rect(center=circle_center)
        self.screen.blit(question_text, text_rect)

        # Draw answer options as buttons
        self.option_rects = []
        for i, option in enumerate(self.options):
            rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 100,  # Center horizontally
                350 + i * 60,             # Stack vertically with spacing
                200,                      # Button width
                40                        # Button height
            )
            self.option_rects.append(rect)

            # Highlight selected option in brighter red
            color = (200, 0, 0) if self.selected_option != i else (255, 0, 0)
            pygame.draw.rect(self.screen, color, rect)

            # Draw option text
            option_text = self.font.render(str(option), True, WHITE)
            text_rect = option_text.get_rect(center=rect.center)
            self.screen.blit(option_text, text_rect)

        return False 