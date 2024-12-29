import pygame as pg

class TimeManager:
    def __init__(self):
        self.start_time = pg.time.get_ticks()
        self.level = 1
        self.delta_time = self.get_delta_time()
        self.next_time = self.delta_time
        self.prev_time = 0
        
    def get_delta_time(self):
        return 1000 / self.level
    
    @property
    def current_time(self):
        return pg.time.get_ticks() - self.start_time
    
    def check_delta_time_elapsed(self):
        # print(f"current_time = {self.current_time}, prev_time = {self.prev_time}")
        if self.current_time - self.prev_time >= self.delta_time:
            self.prev_time = self.current_time
            return True
        return False
            