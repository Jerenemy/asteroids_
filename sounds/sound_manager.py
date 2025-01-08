from utils import TimeManager, AssetManager


class SoundManager:
    def __init__(self, asset_manager: AssetManager):
        self.asset_manager = asset_manager
        self.rocket_sound_time_manager = TimeManager(285) # rocket sound delta time
    
    def get_sound(self, sound_name: str, custom_sound_path=None):
        sound = self.asset_manager.get_sound(sound_name)
        if sound:
            return sound
        self.asset_manager.load_sound(sound_name, custom_sound_path)
        return self.asset_manager.get_sound(sound_name)
       
    def play_event_sound(self, event_type: str):
        if event_type == 'rocket':
            if self.rocket_sound_time_manager.check_delta_time_elapsed():
                self.get_sound('rocket', 'thrust1.wav').play()
        elif event_type == 'bullet_hit_asteroid':
            self.get_sound('asteroid_explosion', 'bangLarge.wav').play()
        elif event_type == 'user_spaceship_hit':
            self.get_sound('explosion', 'bangMedium.wav').play()
        elif event_type == 'enemy_spaceship_hit':
            self.get_sound('explosion', 'bangSmall.wav').play()
        elif event_type == 'shoot':
            self.get_sound('shoot', 'fire.wav').play()

    
class LevelSoundManager(SoundManager):
    def __init__(self, asset_manager, level_duration):
        super().__init__(asset_manager)
        self.level_sound_time_manager = TimeManager(delta_time=level_duration)
        self.last_level_sound_played = 2

    def play_sounds(self, current_level_time: int, level_duration: int):
        self.play_level_sound(current_level_time, level_duration)
        
    def play_level_sound(self, current_level_time: int, level_duration: int, level_sound_delay=1000):
        if current_level_time <= (1/3) * level_duration:
            self.level_sound_time_manager.delta_time = level_sound_delay
        elif current_level_time <= (2/3) * level_duration:
            self.level_sound_time_manager.delta_time = level_sound_delay/2
        elif current_level_time <= level_duration:
            self.level_sound_time_manager.delta_time = level_sound_delay/4
        if self.level_sound_time_manager.check_delta_time_elapsed():
            if self.last_level_sound_played == 2:
                self.get_sound('bip1', 'beat1.wav').play()
                self.last_level_sound_played = 1
            else:
                self.get_sound('bip2', 'beat2.wav').play()
                self.last_level_sound_played = 2