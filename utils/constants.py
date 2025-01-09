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

# frames per second
FPS = 50

# buttons
LEFT_CLICK = 0

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
ROTATE = 4.5
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
LEVEL_DURATION_INCREASE = 4000
INITIAL_LEVEL_DURATION = 6000

# BULLET SETTINGS
BULLET_SIZE = 3
MAX_BULLETS = 100
BULLET_SPEED = 20
ENEMY_BULLET_SPEED = 5

# ENEMY SPACESHIP SETTINGS
BIG_ENEMY_SSHIP_SIZE = 45
SMALL_ENEMY_SSHIP_SIZE = 25
BIG_ENEMY_SSHIP_SPEED = 3
SMALL_ENEMY_SSHIP_SPEED = 6
SHORTEN_SSHIP_DELTA_TIME = 3
CHANGE_DIRECTION_ENEMY_SSHIP_CHANCE = 100
MIN_SSHIP_DELTA_TIME = 300

# ASTEROID SETTINGS
SHORTEN_AST_DELTA_TIME = 3
MIN_AST_DELTA_TIME = 400

# GAME SETTINGS
INITIAL_SPACESHIP_FIRE_DELTA_TIME = 500  # Increases
INITIAL_ASTEROID_DELTA_TIME = 4000
INITIAL_SPACESHIP_DELTA_TIME = 6000