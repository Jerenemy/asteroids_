from random import choice
from .constants import WHITE, YELLOW, ORANGE, RED, GREEN, BLUE, PURPLE
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
