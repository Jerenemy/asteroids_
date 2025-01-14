from random import choice
from .constants import WHITE, YELLOW, ORANGE, RED, GREEN, BLUE, PURPLE, Y_SCRNSIZE, DEG2RAD, RAD2DEG
from pygame import display
from math import atan, radians, cos, sin

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
    return choice([YELLOW, ORANGE, GREEN, BLUE, PURPLE])

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


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else: return 0
    
    
def get_direction_to(origin_object, target_object):    
    try: 
        xx = target_object.x - origin_object.x
        yy = target_object.y - origin_object.y

        if xx < 0:
            fire_direction = (atan(yy/xx) - 90 * DEG2RAD) * RAD2DEG
        if xx > 0:
            fire_direction = (atan(yy/xx) + 90 * DEG2RAD) * RAD2DEG
        if xx == 0:
            if yy >= 0: 
                fire_direction = 180
            if yy < 0:
                fire_direction = 0 
        return fire_direction
    except AttributeError:
        return 0
    
    
def flipcoin():
    return choice([True, False])




def direction_overlap(angle1, angle2):
    """
    Takes two angles in degrees and returns a factor based on their alignment:
    - Returns 1 if they are in the same direction.
    - Returns -1 if they are in opposite directions.
    - Returns 0 if they are perpendicular.

    Args:
        angle1 (float): The first angle in degrees (0 to 360).
        angle2 (float): The second angle in degrees (0 to 360).

    Returns:
        float: A factor between -1 and 1.
    """
    # Convert angles to radians
    angle1_rad = radians(angle1)
    angle2_rad = radians(angle2)

    # Convert angles to unit vectors
    vector1 = (cos(angle1_rad), sin(angle1_rad))
    vector2 = (cos(angle2_rad), sin(angle2_rad))

    # Calculate dot product
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    return dot_product
