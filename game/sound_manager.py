"""
Sound Manager
Handles loading and playback of all game audio.
Manages sound effects and background music with volume control.

Provides centralized control over game audio, including:
- Sound effect loading and playback
- Background music control
- Volume management for different sound types
"""

import pygame

class SoundManager:
    def __init__(self):
        """
        Initialize sound manager and load all audio resources.
        Sets up sound effects and their respective volumes.
        """
        self.background_music_playing = False
        self.load_sounds()
        self.setup_volumes()

    def load_sounds(self):
        """
        Load all game sound effects into a dictionary.
        Each sound is loaded with error handling to prevent crashes.
        """
        self.sounds = {
            'background': self.load_sound('assets/sounds/background_music.wav'),
            'jump': self.load_sound('assets/sounds/jump.wav'),
            'collision': self.load_sound('assets/sounds/collision.wav'),
            'game_over': self.load_sound('assets/sounds/game_over.wav'),
            'correct': self.load_sound('assets/sounds/correct.wav'),
            'wrong': self.load_sound('assets/sounds/wrong.wav'),
            'click': self.load_sound('assets/sounds/click.wav')
        }

    def load_sound(self, filename):
        """
        Load a single sound file with error handling
        Args:
            filename (str): Path to sound file
        Returns:
            Sound: Loaded sound object or None if loading fails
        """
        try:
            sound = pygame.mixer.Sound(filename)
            return sound
        except pygame.error as e:
            print(f"Error loading sound {filename}: {e}")
            return None

    def setup_volumes(self):
        """
        Set up volume levels for different sound effects.
        Each sound type has a predefined volume level for balance.
        """
        volumes = {
            'background': 0.3,  # Background music volume
            'jump': 0.4,       # Jump sound effect volume
            'collision': 0.8,  # Collision sound volume
            'game_over': 0.5,  # Game over sound volume
            'correct': 0.4,    # Correct answer sound volume
            'wrong': 0.4,      # Wrong answer sound volume
            'click': 0.3       # Button click sound volume
        }
        
        for sound_name, volume in volumes.items():
            if sound := self.sounds.get(sound_name):
                sound.set_volume(volume)

    def play_sound(self, sound_name):
        """
        Play a sound effect by name
        Args:
            sound_name (str): Name of the sound to play from the sounds dictionary
        """
        if sound := self.sounds.get(sound_name):
            sound.play()

    def play_background_music(self):
        """
        Start playing background music in a loop.
        Stops any currently playing sounds before starting.
        """
        if not self.background_music_playing:
            pygame.mixer.stop()  # Stop all playing sounds
            pygame.mixer.music.load('assets/sounds/background_music.wav')
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            pygame.mixer.music.set_volume(0.3)
            self.background_music_playing = True

    def stop_background_music(self):
        """
        Stop the currently playing background music.
        Also unloads the music to free up resources.
        """
        if self.background_music_playing:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            self.background_music_playing = False 