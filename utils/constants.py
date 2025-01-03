from pygame import display, init
import math
from os import path

# Initialize pygame to fetch display information
init()

# SCREEN SETTINGS
scrnsize_scale_factor = .8
screen_info = display.Info()
X_SCRNSIZE = int(screen_info.current_w * scrnsize_scale_factor) # Width of the display
Y_SCRNSIZE = int(screen_info.current_h * scrnsize_scale_factor) # Height of the display
MAX_X_SCRNSIZE = screen_info.current_w
MAX_Y_SCRNSIZE = screen_info.current_h

FPS = 50

# buttons
SPACEBAR = 0

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (211, 3, 252)
YELLOW = (255, 241, 0)
ORANGE = (255, 140, 0)

# SPACESHIP MOVEMENT
ACCELERATION = 0.3
DECELERATION = 0.02
ROTATE = 5
SPACESHIP_STARTING_LIVES = 3 #reset to 3

# ANGLE CONVERSIONS
RAD2DEG = 180 / math.pi
DEG2RAD = math.pi / 180

# PATHS
HIGH_SCORES_FILE = path.join("assets", "data", "high_scores.json")

# STATES
MENU = 'menu'
PLAYING = 'playing'
PAUSED = 'paused'
GAME_OVER = 'game_over'

# DURATIONS
SSHIP_DESTRUCTION_DURATION = 200
FLICKER_ROCKET_DURATION = 2
WAIT_AFTER_ENTERING_INITIALS_TIME = 1000
INVULNERABLE_TIME = 5000
FLICKER_INVULNERABLE_DURATION = 20

# BULLET SETTINGS
MAX_BULLETS = 100
BULLET_SPEED = 20
AUTO_BULLET_SPEED = 5

# GAME SETTINGS
INITIAL_SPACESHIP_FIRE_DELTA_TIME = 500  # Increases
INITIAL_ASTEROID_DELTA_TIME = 1200
INITIAL_SPACESHIP_DELTA_TIME = 6000

MIN_ASTEROID_DELTA_TIME = 450
MIN_SPACESHIP_DELTA_TIME = 2500
MAX_SPACESHIP_FIRE_DELTA_TIME = 1500

# DELTA TIMES (STATIC)
BULLET_DELTA_TIME = 150
ROCKET_SOUND_DELTA_TIME = 285
PAUSE_DELTA_TIME = 500

