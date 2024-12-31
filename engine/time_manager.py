import pygame as pg

class TimeManager:
    def __init__(self, delta_time):
        self.delta_time = delta_time
        self.start_time = pg.time.get_ticks()
        # self.current_level = 1
        self.next_time = self.delta_time
        self.prev_time = 0
        # self.level_scale_factor = 0.8
        
    # @property
    # def delta_time(self):
    #     return 1000 * (self.level_scale_factor * self.current_level)
    
    @property
    def current_time(self):
        return pg.time.get_ticks() - self.start_time
    
    def check_delta_time_elapsed(self):
        # print(f"current_time = {self.current_time}, prev_time = {self.prev_time}")
        if self.current_time - self.prev_time >= self.delta_time:
            self.prev_time = self.current_time
            return True
        return False
            