from utils import TimeManager, AssetManager, SHORTEN_AST_DELTA_TIME, SHORTEN_SSHIP_DELTA_TIME, LEVEL_DURATION_INCREASE, INITIAL_LEVEL_DURATION, INITIAL_ASTEROID_DELTA_TIME, INITIAL_SPACESHIP_DELTA_TIME, MIN_AST_DELTA_TIME, MIN_SSHIP_DELTA_TIME
from sounds import LevelSoundManager

class LevelManager:
    def __init__(self, asset_manager: AssetManager, initial_level=1, level_duration=INITIAL_LEVEL_DURATION, asteroid_delta_time=INITIAL_ASTEROID_DELTA_TIME, enemy_sship_delta_time=INITIAL_SPACESHIP_DELTA_TIME):
        """
        Initialize the LevelManager.

        Args:
            initial_level (int): Starting level.
            level_duration (int): Duration of each level in milliseconds.
        """
        self.current_level = initial_level
        self.new_level_approaching = None
        self.asset_manager = asset_manager
        TimeManager.clear_instances()
        self.level_time_manager = TimeManager(delta_time=level_duration)
        self.sound_manager = LevelSoundManager(self.asset_manager, level_duration)
        # new level
        self.display_new_level = True
        self.display_new_level_time_manager = TimeManager(delta_time=2000)
        # asteroids
        self.longest_asteroid_delta_time = asteroid_delta_time
        self.asteroid_time_manager = TimeManager(delta_time=asteroid_delta_time)
        # enemy sship
        self.longest_enemy_sship_delta_time = enemy_sship_delta_time
        self.enemy_sship_time_manager = TimeManager(delta_time=enemy_sship_delta_time)
        # sounds
        self.level_sound_time_manager = TimeManager(delta_time=2000)


    @property
    def level_duration(self):
        return self.level_time_manager.delta_time

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
        return rgb

    def update(self, len_enemies):
        """
        Check if the current level's time has elapsed and advance the level if necessary.
        TODO: need to let everything exit the screen before the new level starts
        """
        self.increase_difficulty_during_level()
        self.display_new_level = self.check_display_new_level_allowed()
        if self.level_time_manager.check_delta_time_elapsed():
            self.new_level_approaching = True
        if self.new_level_approaching and len_enemies == 0:
            # print('spawn allowed now')
            self.new_level_approaching = False
            self.display_new_level_time_manager = TimeManager(delta_time=2000)
            self.display_new_level = True
            self.current_level += 1
            # print(self.current_level)
            self.adjust_level_settings_for_new_level()

    def increase_difficulty_during_level(self):
        '''
        increase the difficulty during each level by shortening the asteroid delta time and the spaceship delta time
        '''
        self.asteroid_time_manager.delta_time = max(MIN_AST_DELTA_TIME, self.asteroid_time_manager.delta_time - SHORTEN_AST_DELTA_TIME)
        self.enemy_sship_time_manager.delta_time = max(MIN_SSHIP_DELTA_TIME, self.enemy_sship_time_manager.delta_time - SHORTEN_SSHIP_DELTA_TIME)
    
    def adjust_level_settings_for_new_level(self):
        """
        Adjust game settings based on the current level.
        """
        print(f"Advancing to Level {self.current_level}")
        # Modify difficulty settings here
        self.level_time_manager.delta_time = self.level_duration + LEVEL_DURATION_INCREASE
        self.asteroid_time_manager.delta_time = self.longest_asteroid_delta_time
        self.enemy_sship_time_manager.delta_time = self.longest_enemy_sship_delta_time
        # self.longest_asteroid_delta_time = max(300, self.longest_asteroid_delta_time - 200)
        # self.asteroid_time_manager.delta_time = max(300, self.asteroid_time_manager.delta_time - 200)

    def reset(self):
        """
        Reset the level manager for a new game.
        """
        self.current_level = 1
        self.time_manager = TimeManager(level_duration=self.level_duration)
