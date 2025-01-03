from pygame import quit, key, mouse, QUIT, K_q, K_z, time, display
from sys import exit


def cleanup():
    exit()
    quit()
    
def is_key_pressed(key_input):
    """
    Detect if a key is pressed
    example call:
    is_key_pressed(pg.K_q)
    """
    kp = key.get_pressed()
    return kp[key_input]

def is_mouse_pressed(mouse_input: int):
    """
    Detect if a mouse button is pressed
    0: left mouse button
    1: middle mouse button
    2: right mouse button
    """
    mp = mouse.get_pressed()
    return mp[mouse_input]

def check_quit(event):
    if event.type == QUIT or is_key_pressed(K_q):
        return True


class KeyManager:
    """manages whether or not we are allowed to return a true event when detecting that a key has been pressed"""
    def __init__(self, key):
        self.key = key
        self.recently_allowed = False # store bool as attribute in class, check for if this specific key has been unpressed

    def is_key_pressed_once(self) -> bool:
        # if key is pressed, need to return true, and also restrict a new press until the key is unpressed
        kp = key.get_pressed()
        if kp[self.key]:
            if not self.recently_allowed:
                self.recently_allowed = True
                return True
            else: return False # redundant else
        else: # redundant else
            # detect key unpress when kp[self.key] == False
            self.recently_allowed = False
            return False

class KeysManager:
    def __init__(self):
        self.key_obj_list = KeysManager.init_key_obj_list()
     
    @staticmethod   
    def init_key_obj_list():
        r = []
        # instantiate object for each key in list (eg K_SPACE, K_a, K_b, ...)
        for i in range(K_z):
            r += [KeyManager(i)]
        return r

    def __call__(self, k: int):
        return self.key_obj_list[k].is_key_pressed_once()