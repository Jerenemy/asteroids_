import pygame as pg
from .time_manager import TimeManager  # Assuming TimeManager is in a separate file

class LevelManager:
    def __init__(self, initial_level=1, level_duration=5000, asteroid_delta_time=1000):
        """
        Initialize the LevelManager.

        Args:
            initial_level (int): Starting level.
            level_duration (int): Duration of each level in milliseconds.
        """
        self.current_level = initial_level
        self.level_time_manager = TimeManager(delta_time=level_duration)
        self.level_duration = level_duration  # Keep this for reference or UI purposes.
        # self.asteroid_delta_time = 1000
        self.asteroid_time_manager = TimeManager(delta_time=asteroid_delta_time)

    def update(self):
        """
        Check if the current level's time has elapsed and advance the level if necessary.
        """
        if self.level_time_manager.check_delta_time_elapsed():
            self.current_level += 1
            self.adjust_level_settings()

    def adjust_level_settings(self):
        """
        Adjust game settings based on the current level.
        """
        print(f"Advancing to Level {self.current_level}")
        # Modify difficulty settings here
        self.level_time_manager.delta_time = self.level_duration + 2000
        self.asteroid_time_manager.delta_time = max(300, self.asteroid_time_manager.delta_time - 200)

    def reset(self):
        """
        Reset the level manager for a new game.
        """
        self.current_level = 1
        self.time_manager = TimeManager(level_duration=self.level_duration)
