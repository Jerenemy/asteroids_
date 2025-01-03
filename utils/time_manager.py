import pygame as pg

class TimeManager:
    paused = False
    instances = []
    
    def __init__(self, delta_time):
        self.delta_time = delta_time
        self.start_time = pg.time.get_ticks()
        self.prev_time = 0
        self.already_set_start_paused_time = False
        self.prev_tot_paused_time = 0
        TimeManager.instances.append(self)
        
    @property
    def total_time(self):
        return pg.time.get_ticks()
        
    @property
    def current_time(self):
        return pg.time.get_ticks() - self.paused_time - self.start_time
    
    @property
    def elapsed_time(self):
        return self.current_time - self.prev_time
    
    @property
    def paused_time(self):
        if TimeManager.paused:
            if not self.already_set_start_paused_time:
                self.start_paused_time = self.total_time
                self.already_set_start_paused_time = True
            return self.prev_tot_paused_time + (self.total_time - self.start_paused_time)
        if self.already_set_start_paused_time:
            self.prev_tot_paused_time += (self.total_time - self.start_paused_time)
            self.already_set_start_paused_time = False
        return self.prev_tot_paused_time
        
    def check_delta_time_elapsed(self) -> bool:
        if self.elapsed_time >= self.delta_time:
            self.prev_time = self.current_time
            return True
        return False
    
    def update(self):
        # simply calling the property self.paused_time allows everything to sync and detect properly, 
        # and the self.prev_tot_paused_time to save properly
        _ = self.paused_time

    @classmethod
    def toggle_pause(cls):
        cls.paused = not cls.paused
        TimeManager.update_instances()
        # problem: all time managers never even update during pause, since none of the attributes are called and check_delta_time_elapsed isn't called
        # safest way to do this is to update all instances once when toggling paused.
        
    @classmethod
    def update_instances(cls):
        for instance in cls.instances:
            instance.update()
            
    @classmethod
    def clear_instances(cls):
        cls.instances = []