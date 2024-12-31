from random import choice
from .constants import WHITE, YELLOW, ORANGE, RED, GREEN, BLUE, PURPLE, Y_SCRNSIZE
from pygame import display

def load_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

def save_to_file(filepath, content):
    # Code for saving files
    pass

def clamp(value, min_value, max_value):
    # Code for clamping values
    pass

def choose_color():
    return choice([YELLOW, ORANGE, RED, GREEN, BLUE, PURPLE])

def get_list_item_by_type(lst, typ):
    """Gets the first instance of the item of 'typ' from 'lst'."""
    return next((item for item in lst if isinstance(item, typ)), None)

class flicker:
    def __init__(self, duration: int):
        self.duration = duration
        self.counter = 0
    
    def __call__(self):
        if self.counter < self.duration:
            result = True
        else:
            result = False
        self.counter += 1
        if self.counter >= 2 * self.duration:  # Reset counter after a full cycle
            self.counter = 0
        return result
    
     
def translate_to_ratio(raw_val: int, scale_val=800, screen_size=Y_SCRNSIZE) -> int:
    _, screen_size = display.get_window_size()
    return int((raw_val/scale_val) * screen_size)