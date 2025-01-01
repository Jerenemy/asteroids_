import pygame as pg
from .time_manager import TimeManager  # Assuming TimeManager is in a separate file
from utils import AssetManager

class LevelManager:
    def __init__(self, asset_manager: AssetManager, initial_level=1, level_duration=5000, asteroid_delta_time=1000):
        """
        Initialize the LevelManager.

        Args:
            initial_level (int): Starting level.
            level_duration (int): Duration of each level in milliseconds.
        """
        self.current_level = initial_level
        self.level_time_manager = TimeManager(delta_time=level_duration)
        # self.level_duration = level_duration  # Keep this for reference or UI purposes.
        self.asset_manager = asset_manager
        self.display_new_level = True
        # self.prev_display_new_level = self.display_new_level # debugging
        self.display_new_level_time_manager = TimeManager(delta_time=2000)
        self.last_level_sound_played = 2
        # self.asteroid_delta_time = 1000
        self.asteroid_time_manager = TimeManager(delta_time=asteroid_delta_time)
        self.level_sound_time_manager = TimeManager(delta_time=2000)

    @property
    def level_duration(self):
        return self.level_time_manager.delta_time

    @property
    def current_level_time(self):
        return self.level_time_manager.current_time
    
    def play_level_sound(self):
        delta_time = 1000
        if self.current_level_time <= (1/3) * self.level_duration:
            self.level_sound_time_manager.delta_time = delta_time
        elif self.current_level_time <= (2/3) * self.level_duration:
            self.level_sound_time_manager.delta_time = delta_time/2
        elif self.current_level_time <= self.level_duration:
            self.level_sound_time_manager.delta_time = delta_time/4
        if self.level_sound_time_manager.check_delta_time_elapsed():
            if self.last_level_sound_played == 2:
                self.get_sound('bip1', 'beat1.wav').play()
                self.last_level_sound_played = 1
            else:
                self.get_sound('bip2', 'beat2.wav').play()
                self.last_level_sound_played = 2

    def get_sound(self, sound_name: str, custom_sound_path=None):
        sound = self.asset_manager.get_sound(sound_name)
        if sound:
            return sound
        self.asset_manager.load_sound(sound_name, custom_sound_path)
        return self.asset_manager.get_sound(sound_name)
       
    
    def check_display_new_level_allowed(self):
        if self.display_new_level:
            return not self.display_new_level_time_manager.check_delta_time_elapsed()
        return False
    
    def get_level_color_counter(self) -> int:
        # want it to equal 255 when it equals the delta time
        dim = 0.5
        white = 255
        if self.display_new_level_time_manager.current_time < self.display_new_level_time_manager.delta_time/2:
            return int(
                white 
                * (dim*2 
                   - (self.display_new_level_time_manager.current_time/self.display_new_level_time_manager.delta_time)*dim
                )
            ) 
        else:
            return int(
                white 
                * ((self.display_new_level_time_manager.current_time/self.display_new_level_time_manager.delta_time)
                   + dim*2
                   )
                * dim
            ) 

    def update(self):
        """
        Check if the current level's time has elapsed and advance the level if necessary.
        """
        self.display_new_level = self.check_display_new_level_allowed()
        # if self.display_new_level != self.prev_display_new_level:
        #     print(self.display_new_level)
            # self.prev_display_new_level = self.display_new_level
        # print(self.display_new_level)
        if self.level_time_manager.check_delta_time_elapsed():
            self.display_new_level_time_manager = TimeManager(delta_time=2000)
            self.display_new_level = True
            self.current_level += 1
            print(self.current_level)
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
