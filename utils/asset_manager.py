import os
import pygame
from utils.helpers import load_from_file, save_to_file

class AssetManager:
    """
    A modular and object-oriented asset manager for handling all game assets such as images,
    sounds, and fonts. This class centralizes asset loading and retrieval.
    """

    def __init__(self, base_path="assets"):
        """
        Initialize the AssetManager with a base path for assets.

        Args:
            base_path (str): The base directory where assets are stored.
        """
        self.base_path = base_path
        self.images = {}
        self.sounds = {}
        self.fonts = {}

        # Initialize pygame's mixer and font systems if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.font.get_init():
            pygame.font.init()

    def init_assets(self):
        # init fonts
        self.load_font('signature', 'signature_font', )
    
    def load_image(self, key, relative_path, colorkey=None):
        """
        Load an image and store it in the images dictionary.

        Args:
            key (str): The identifier for the image.
            relative_path (str): The relative path to the image file.
            colorkey (tuple or None): Optional color key for transparency.
        """
        full_path = os.path.join(self.base_path, "images", relative_path)
        try:
            image = pygame.image.load(full_path)
            if colorkey is not None:
                image.set_colorkey(colorkey)
            self.images[key] = image
        except pygame.error as e:
            print(f"Failed to load image {relative_path}: {e}")

    def get_image(self, key):
        """
        Retrieve a loaded image by its key.

        Args:
            key (str): The identifier for the image.

        Returns:
            pygame.Surface: The requested image.
        """
        return self.images.get(key)

    def load_sound(self, key, relative_path):
        """
        Load a sound effect and store it in the sounds dictionary.

        Args:
            key (str): The identifier for the sound.
            relative_path (str): The relative path to the sound file.
        """
        full_path = os.path.join(self.base_path, "sounds", relative_path)
        try:
            sound = pygame.mixer.Sound(full_path)
            self.sounds[key] = sound
        except pygame.error as e:
            print(f"Failed to load sound {relative_path}: {e}")

    def get_sound(self, key):
        """
        Retrieve a loaded sound effect by its key.

        Args:
            key (str): The identifier for the sound.

        Returns:
            pygame.mixer.Sound: The requested sound.
        """
        return self.sounds.get(key)

    def load_font(self, key, relative_path, size):
        """
        Load a font and store it in the fonts dictionary.
        If relative_path=None, load the built-in font of 'key'.

        Args:
            key (str): The identifier for the font.
            relative_path (str): The relative path to the font file.
            size (int): The font size.
        """
        if relative_path:
            full_path = os.path.join(self.base_path, "fonts", relative_path)
            try:
                font = pygame.font.Font(full_path, size)
                self.fonts[f"{key}_{size}"] = font
            except pygame.error as e:
                print(f"Failed to load font {relative_path}: {e}")
        else: 
            font = pygame.font.SysFont(key, size)
            self.fonts[f"{key}_{size}"] = font

    def get_font(self, key, size):
        """
        Retrieve a loaded font by its key.

        Args:
            key (str): The identifier for the font.

        Returns:
            pygame.font.Font: The requested font.
        """
        return self.fonts.get(f"{key}_{size}")

    def load_high_scores(self, relative_path):
        """
        Load high scores from a file using the helpers function.

        Args:
            relative_path (str): The relative path to the high scores file.

        Returns:
            list: High scores as a list of tuples.
        """
        full_path = os.path.join(self.base_path, "data", relative_path)
        content = load_from_file(full_path)
        if content is None:
            return []
        high_scores = []
        for line in content.strip().split("\n"):
            try:
                name, score = line.split(":")
                high_scores.append((name, int(score)))
            except ValueError:
                pass
        return high_scores

    def save_high_scores(self, relative_path, high_scores):
        """
        Save high scores to a file using the helpers function.

        Args:
            relative_path (str): The relative path to the high scores file.
            high_scores (list): List of tuples with player names and scores.
        """
        full_path = os.path.join(self.base_path, "data", relative_path)
        content = "\n".join(f"{name}:{score}" for name, score in high_scores)
        save_to_file(full_path, content)
