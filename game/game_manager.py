"""
Game Manager
Core class that manages the entire game state and logic.
Handles game initialization, state transitions, event processing,
rendering, and coordinates all game components.
"""

import pygame
import sys
import random
import os
from components.player import Player
from components.platform import Platform
from components.enemy import Enemy
from components.math_question import MathQuestion
from game.background import Background
from game.sound_manager import SoundManager
from game.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    MENU, PLAYING, MATH_QUESTION, HOW_TO_PLAY,
    SCROLL_THRESH, GRAVITY, MAX_PLATFORMS, PLATFORM_GAP,
    ENEMY_SPEED, PLATFORM_SPEED, ENEMY_DISTANCE, ENEMY_VERTICAL_DISTANCE,
    OCEAN_SCORE, SKY_SCORE, SPACE_SCORE, MATH_SCORE,
    WHITE, BLACK, YELLOW,
    BUTTON_WIDTH, BUTTON_HEIGHT,
    platform_group, enemy_group,
    HIGH_SCORE_FILE
)

class GameManager:
    def __init__(self, screen):
        """
        Initialize game manager and all game components
        Args:
            screen: Pygame surface for the game window
        """
        # Initialize display screen and game settings
        self.screen = screen

        # Initialize game clock
        self.clock = pygame.time.Clock()

        # Game state variables
        self.scroll = 0
        self.bg_scroll = 0
        self.game_over = False
        self.score = 0
        self.score_threshold = OCEAN_SCORE
        self.fade_counter = 0
        self.total_scroll = 0
        self.game_state = MENU
        self.saved_game_state = None
        self.current_background = 0
        self.next_enemy_y = -200

        # Background transition settings
        self.FADE_SPEED = 5
        self.background_alpha = 255
        self.transition_active = False
        self.next_background = 0

        # Initialize components
        self.setup_fonts()
        self.background = Background(self.screen)
        self.sound_manager = SoundManager()
        self.setup_sprites()
        self.load_high_score()

    def setup_fonts(self):
        """Initialize all game fonts with error handling"""
        try:
            self.title_font = pygame.font.SysFont('Lucida Sans', 60)
            self.button_font = pygame.font.SysFont('Lucida Sans', 24)
            self.font_small = pygame.font.SysFont('Lucida Sans', 20)
            self.font_big = pygame.font.SysFont('Lucida Sans', 24)
        except pygame.error as e:
            print(f"Error loading fonts: {e}")
            sys.exit(1)

    def setup_sprites(self):
        """Initialize all game sprites and sprite groups"""
        self.platform_group = platform_group
        self.enemy_group = enemy_group
        self.create_initial_platforms()
        self.jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.math_question = MathQuestion(self.screen, self.font_big)

    def create_initial_platforms(self):
        """Create the initial set of platforms for game start"""
        platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
        self.platform_group.add(platform)
        
        last_platform = platform
        for _ in range(MAX_PLATFORMS - 1):
            p_w = random.randint(50, 100)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = last_platform.rect.y - random.randint(80, 120)
            p_moving = random.random() < 0.3
            platform = Platform(p_x, p_y, p_w, p_moving)
            self.platform_group.add(platform)
            last_platform = platform

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, 'r') as file:
                    self.high_score = int(file.read())
            except ValueError:
                self.high_score = 0
        else:
            self.high_score = 0

    def run(self):
        """
        Main game loop function
        Handles background transitions, event processing,
        state updates, and rendering.
        Returns:
            bool: False if game should exit, True otherwise
        """
        # Check score and background transitions
        if self.score >= self.score_threshold:
            if self.current_background < len(self.background.background_images) - 1:
                self.current_background += 1
                # Sync global current_background to update enemy types
                from game.constants import current_background as global_current_background
                global_current_background = self.current_background
                self.enemy_group.empty()
                self.next_enemy_y = -200
                if self.current_background == 1:
                    self.score_threshold = SKY_SCORE
                elif self.current_background == 2:
                    self.score_threshold = SPACE_SCORE
                elif self.current_background == 3:
                    self.score_threshold = MATH_SCORE

        # Process game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == PLAYING:
                        self.sound_manager.stop_background_music()
                        self.game_state = MENU
                    elif self.game_state == HOW_TO_PLAY:
                        self.game_state = MENU
                    elif self.game_state == MENU:
                        return False
                else:
                    if self.game_state == PLAYING:
                        if event.key in [pygame.K_SPACE, pygame.K_UP]:
                            self.jumpy.jump()
                            self.sound_manager.play_sound('jump')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == MENU:
                    self.handle_menu_click(event.pos)
                elif self.game_state == HOW_TO_PLAY:
                    self.sound_manager.play_sound('click')
                    self.game_state = MENU
                elif self.game_state == MATH_QUESTION:
                    self.handle_math_question_click(event.pos)

        # Update game state and render
        self.update_game_state()
        self.draw()
        
        pygame.display.update()
        self.clock.tick(FPS)
        
        return True

    def handle_menu_click(self, pos):
        """
        Handle clicks on menu buttons
        Args:
            pos: Mouse click position (x, y)
        Returns:
            bool: False if exit button clicked, True otherwise
        """
        mouse_x, mouse_y = pos
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        
        # Start game button
        if self.check_button_click(pos, 300):
            self.sound_manager.play_sound('click')
            self.reset_game()
            self.sound_manager.play_background_music()
        # How to play button
        elif self.check_button_click(pos, 370):
            self.sound_manager.play_sound('click')
            self.game_state = HOW_TO_PLAY
        # Clear high score button
        elif self.check_button_click(pos, 440):
            self.sound_manager.play_sound('click')
            self.clear_high_score()
        # Exit button
        elif self.check_button_click(pos, 510):
            self.sound_manager.play_sound('click')
            return False
        return True

    def handle_math_question_click(self, pos):
        """
        Handle clicks on math question options
        Args:
            pos: Mouse click position (x, y)
        """
        try:
            if hasattr(self.math_question, 'handle_click'):
                result = self.math_question.handle_click(pos)
                if result is not None:
                    self.handle_math_question_result(result)
            else:
                print("Math question object is not properly initialized")
                self.game_state = MENU
        except Exception as e:
            print(f"Error handling math question: {e}")
            self.cleanup_game_state()
            self.game_state = MENU

    def handle_math_question_result(self, result):
        """
        Process the result of answering a math question
        Args:
            result (bool): True if answer correct, False if wrong
        """
        try:
            if result is True:
                if self.restore_game_state():
                    self.game_state = PLAYING
                    self.game_over = False
                    self.sound_manager.play_background_music()
                else:
                    print("Failed to restore game state")
                    self.cleanup_game_state()
                    self.reset_game()
                    self.game_state = MENU
            elif result is False:
                self.cleanup_game_state()
                self.reset_game()
                self.game_state = MENU
        except Exception as e:
            print(f"Error in handle_math_question_result: {e}")
            self.cleanup_game_state()
            self.reset_game()
            self.game_state = MENU

    def update_game_state(self):
        """
        Update game state during gameplay
        Handles player movement, platform generation,
        background transitions, and enemy spawning
        """
        if self.game_state == PLAYING and not self.game_over:
            # Update player position and scrolling
            self.scroll = self.jumpy.move()
            self.bg_scroll = (self.bg_scroll + self.scroll) % SCREEN_HEIGHT
            self.total_scroll += self.scroll
            self.score += self.scroll // 10

            # Update platforms
            self.platform_group.update(self.scroll)
            if len(self.platform_group) < MAX_PLATFORMS:
                p_w = random.randint(50, 100)
                p_x = random.randint(0, SCREEN_WIDTH - p_w)
                p_y = self.platform_group.sprites()[-1].rect.y - PLATFORM_GAP
                p_moving = random.random() < 0.3
                platform = Platform(p_x, p_y, p_w, p_moving)
                self.platform_group.add(platform)

            # Check background transitions
            if not self.transition_active:
                if self.score >= SPACE_SCORE and self.current_background < 3:
                    self.transition_active = True
                    self.next_background = 3
                elif self.score >= SKY_SCORE and self.current_background < 2:
                    self.transition_active = True
                    self.next_background = 2
                elif self.score >= OCEAN_SCORE and self.current_background < 1:
                    self.transition_active = True
                    self.next_background = 1

            # Update background transition
            if self.transition_active:
                self.background_alpha = max(0, self.background_alpha - self.FADE_SPEED)
                if self.background_alpha <= 0:
                    self.current_background = self.next_background
                    self.transition_active = False
                    self.background_alpha = 255
                    # Sync global current_background
                    from game.constants import current_background as global_current_background
                    global_current_background = self.current_background

            # Update enemies
            self.check_spawn_enemy()
            self.enemy_group.update(self.scroll)

            # Check death conditions
            if self.jumpy.rect.top > SCREEN_HEIGHT or any(self.jumpy.rect.colliderect(enemy.rect) for enemy in self.enemy_group):
                if not self.game_over:
                    self.handle_death()

    def check_spawn_enemy(self):
        """
        Check if new enemies should be spawned
        Spawns enemies based on current background and score
        """
        if len(self.enemy_group) == 0 or min(enemy.rect.y for enemy in self.enemy_group) > 0:
            spawn_enemy = False
            if self.current_background == 0 and self.score < OCEAN_SCORE:
                spawn_enemy = True
            elif self.current_background == 1 and OCEAN_SCORE <= self.score < SKY_SCORE:
                spawn_enemy = True
            elif self.current_background == 2 and SKY_SCORE <= self.score < SPACE_SCORE:
                spawn_enemy = True
            elif self.current_background == 3 and self.score >= SPACE_SCORE:
                spawn_enemy = True

            if spawn_enemy:
                enemy = Enemy(self.next_enemy_y, self.current_background)
                self.enemy_group.add(enemy)
                if self.current_background == 0:
                    self.next_enemy_y -= ENEMY_VERTICAL_DISTANCE
                else:
                    self.next_enemy_y -= ENEMY_VERTICAL_DISTANCE * 0.8

    def handle_death(self):
        """
        Handle player death
        Saves game state, updates high score, and shows math question
        """
        self.game_over = True
        self.sound_manager.stop_background_music()
        self.save_game_state()
        if self.score > self.high_score:
            self.high_score = self.score
            with open(HIGH_SCORE_FILE, 'w') as file:
                file.write(str(self.high_score))
        self.sound_manager.play_sound('game_over')
        pygame.time.delay(500)
        self.game_state = MATH_QUESTION
        self.math_question = MathQuestion(self.screen, self.font_big)
        self.math_question.generate_question()
        self.math_question.active = True

    def draw(self):
        """
        Main drawing function
        Handles rendering of all game states (menu, game, etc.)
        """
        self.screen.fill(BLACK)

        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == HOW_TO_PLAY:
            self.draw_how_to_play()
        elif self.game_state == MATH_QUESTION:
            self.draw_game_background()
            self.math_question.draw()
            self.draw_scores()
        elif self.game_state == PLAYING:
            self.draw_game()

    def draw_menu(self):
        """Draw the main menu screen with title and buttons"""
        title_text = self.title_font.render("Jump and Math!", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

        high_score_text = self.font_big.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, 
                        (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 220))

        buttons = [
            ("Start Game", 300),
            ("How to Play", 370),
            ("Clear High Score", 440),
            ("Exit", 510)
        ]

        for text, y in buttons:
            self.draw_button(text, y)

    def draw_how_to_play(self):
        instructions = [
            "How to Play",
            "- Use LEFT and RIGHT arrows to move",
            "- Press SPACE to jump",
            "- Collect points by going higher",
            "- Avoid enemies",
            "- Answer math questions to continue",
            "",
            "Click anywhere or press ESC to return to menu"
        ]

        for i, line in enumerate(instructions):
            # Use big font for title, small font for instructions
            font = self.font_big if i == 0 else self.font_small
            text = font.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 35))

    def draw_game(self):
        """Draw the main gameplay screen"""
        self.draw_game_background()
        self.platform_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.jumpy.draw(self.screen)
        self.draw_scores()

    def draw_game_background(self):
        """Draw the game background with transition effects if active"""
        if self.transition_active:
            self.background.draw_transition(self.current_background, self.next_background, 
                                         self.background_alpha, self.bg_scroll)
        else:
            self.background.draw(self.current_background, self.bg_scroll)

    def draw_scores(self):
        """Draw current score and high score"""
        self.draw_text(f"Score: {self.score}", self.font_big, WHITE, 10, 10)
        self.draw_text(f"High Score: {self.high_score}", self.font_big, WHITE, 10, 40)

    def draw_text(self, text, font, color, x, y):
        """
        Draw text on screen
        Args:
            text (str): Text to draw
            font: Pygame font to use
            color: RGB color tuple
            x (int): X position
            y (int): Y position
        """
        img = font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def draw_button(self, text, y, hover=False):
        """
        Draw a menu button
        Args:
            text (str): Button text
            y (int): Y position
            hover (bool): Whether mouse is hovering over button
        """
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        color = (90, 90, 255) if hover else (70, 70, 255)
        pygame.draw.rect(self.screen, color, (button_x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, (button_x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 3)

        text_surface = self.button_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(button_x + BUTTON_WIDTH // 2, 
                                                 y + BUTTON_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def check_button_click(self, pos, button_y):
        mouse_x, mouse_y = pos
        button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        return (button_x <= mouse_x <= button_x + BUTTON_WIDTH and
                button_y <= mouse_y <= button_y + BUTTON_HEIGHT)

    def clear_high_score(self):
        self.high_score = 0
        try:
            with open(HIGH_SCORE_FILE, 'w') as file:
                file.write('0')
        except Exception as e:
            print(f"Error clearing high score: {e}")

    def save_game_state(self):
        """
        Save current game state when player dies
        Includes platform positions, enemy positions, score,
        and finds appropriate spawn point for revival
        """
        try:
            # Find lowest platform for spawn point
            lowest_platform = None
            lowest_y = -float('inf')
            for platform in self.platform_group:
                if platform.rect.y > lowest_y:
                    lowest_y = platform.rect.y
                    lowest_platform = platform
            
            if lowest_platform:
                spawn_x = lowest_platform.rect.centerx
                spawn_y = lowest_platform.rect.top - 60
            else:
                spawn_x = SCREEN_WIDTH // 2
                spawn_y = SCREEN_HEIGHT - 150

            self.saved_game_state = {
                'score': self.score,
                'bg_scroll': self.bg_scroll,
                'current_background': self.current_background,
                'total_scroll': self.total_scroll,
                'platform_positions': [(p.rect.x, p.rect.y, p.width, p.moving) 
                                     for p in self.platform_group],
                'enemy_positions': [(e.rect.x, e.world_y, e.enemy_type) 
                                   for e in self.enemy_group],
                'player_pos': (spawn_x, spawn_y),
                'transition_active': self.transition_active,
                'background_alpha': self.background_alpha,
                'next_background': self.next_background if self.transition_active else self.current_background
            }
        except Exception as e:
            print(f"Error saving game state: {e}")
            self.saved_game_state = None

    def restore_game_state(self):
        """
        Restore saved game state after correctly answering math question
        Returns:
            bool: True if state restored successfully, False otherwise
        """
        if not self.saved_game_state:
            self.reset_game()
            return False

        try:
            # Restore basic state
            self.score = self.saved_game_state['score']
            self.bg_scroll = self.saved_game_state['bg_scroll']
            self.current_background = self.saved_game_state['current_background']
            self.total_scroll = self.saved_game_state['total_scroll']
            self.transition_active = self.saved_game_state.get('transition_active', False)
            self.background_alpha = self.saved_game_state.get('background_alpha', 255)
            self.next_background = self.saved_game_state.get('next_background', self.current_background)

            # Rebuild platforms
            self.platform_group.empty()
            platform_positions = self.saved_game_state.get('platform_positions', [])
            if not platform_positions:
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                self.platform_group.add(platform)
            else:
                for x, y, width, moving in platform_positions:
                    platform = Platform(x, y, width, moving)
                    self.platform_group.add(platform)

            # Rebuild enemies
            self.enemy_group.empty()
            for x, world_y, enemy_type in self.saved_game_state.get('enemy_positions', []):
                if 0 <= x <= SCREEN_WIDTH:
                    enemy = Enemy(world_y, self.current_background)
                    enemy.rect.x = x
                    enemy.enemy_type = enemy_type
                    self.enemy_group.add(enemy)

            # Restore player position
            player_x, player_y = self.saved_game_state['player_pos']
            self.jumpy = Player(player_x, player_y)
            self.jumpy.vel_y = 0
            self.jumpy.jumping = False

            self.saved_game_state = None
            return True

        except Exception as e:
            print(f"Error in restore_game_state: {e}")
            self.reset_game()
            return False

    def cleanup_game_state(self):
        """Clean up game state by resetting all variables and clearing sprite groups"""
        self.platform_group.empty()
        self.enemy_group.empty()
        self.saved_game_state = None
        self.score = 0
        self.bg_scroll = 0
        self.current_background = 0
        self.total_scroll = 0
        self.transition_active = False
        self.background_alpha = 255
        self.next_background = 0
        self.game_over = False
        self.math_question = MathQuestion(self.screen, self.font_big)

    def reset_game(self):
        """Reset game to initial state for new game start"""
        self.game_over = False
        self.score = 0
        self.bg_scroll = 0
        self.total_scroll = 0
        self.score_threshold = OCEAN_SCORE
        self.next_enemy_y = -200
        self.saved_game_state = None
        
        self.platform_group.empty()
        self.enemy_group.empty()
        self.create_initial_platforms()
        self.jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        
        self.current_background = 0
        self.transition_active = False
        self.background_alpha = 255
        self.sound_manager.play_background_music()
        
        self.game_state = PLAYING