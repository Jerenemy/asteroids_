from utils import TimeManager, AssetManager
from sounds import LevelSoundManager

class LevelManager:
    def __init__(self, asset_manager: AssetManager, initial_level=1, level_duration=5000, asteroid_delta_time=1000):
        """
        Initialize the LevelManager.

        Args:
            initial_level (int): Starting level.
            level_duration (int): Duration of each level in milliseconds.
        """
        self.current_level = initial_level
        self.asset_manager = asset_manager
        # self.prev_display_new_level = self.display_new_level # debugging
        TimeManager.clear_instances()
        self.level_time_manager = TimeManager(delta_time=level_duration)
        self.sound_manager = LevelSoundManager(self.asset_manager, level_duration)
        
        self.display_new_level = True
        self.display_new_level_time_manager = TimeManager(delta_time=2000)
        
        # self.asteroid_delta_time = 1000
        self.asteroid_time_manager = TimeManager(delta_time=asteroid_delta_time)
        self.level_sound_time_manager = TimeManager(delta_time=2000)

    @property
    def level_duration(self):
        return self.level_time_manager.delta_time

    # @property
    # def current_level_time(self):
    #     return self.level_time_manager.current_time
    @property
    def elapsed_level_time(self):
        return self.level_time_manager.elapsed_time
    
    def play_level_sound(self):
        self.sound_manager.play_level_sound(self.elapsed_level_time, self.level_duration)
        
    def check_display_new_level_allowed(self):
        if self.display_new_level:
            return not self.display_new_level_time_manager.check_delta_time_elapsed()
        return False
    
    def get_level_color_counter(self) -> int:
        # want it to equal 255 when it equals the delta time
        dim = 0.5
        white = 255
        if self.display_new_level_time_manager.elapsed_time < self.display_new_level_time_manager.delta_time/2:
            rgb = int(
                white 
                * (dim*2 
                   - (self.display_new_level_time_manager.elapsed_time/self.display_new_level_time_manager.delta_time)*dim
                )
            ) 
        else:
            rgb = int(
                white 
                * ((self.display_new_level_time_manager.current_time/self.display_new_level_time_manager.delta_time)
                   + dim*2
                   )
                * dim
            ) 
        # print('elaps', self.display_new_level_time_manager.elapsed_time)
        # print('curr', self.display_new_level_time_manager.current_time)
        # print('prev', self.display_new_level_time_manager.prev_time)
        # print(self.display_new_level_time_manager.paused)
        # print('rgb', rgb)
        return rgb

    def update(self):
        """
        Check if the current level's time has elapsed and advance the level if necessary.
        """
        self.display_new_level = self.check_display_new_level_allowed()
        # if self.display_new_level != self.prev_display_new_level:
        #     print(self.display_new_level)
            # self.prev_display_new_level = self.display_new_level
        # print(self.display_new_level)
        # print(f"level time manager curr time: {self.level_time_manager.current_time}, prev time: {self.level_time_manager.prev_time}")
        print(
            f"\ncurr = {self.level_time_manager.current_time}\n, paus time = {self.level_time_manager.paused_time}\n, prev tot paused = {self.level_time_manager.prev_tot_paused_time}\n, elapsed = {self.level_time_manager.elapsed_time}\n, delta = {self.level_time_manager.delta_time}"
        )
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
