# This __init__.py file makes this directory a Python package.
# It can also group imports for convenience.

# Import specific modules or classes from the package
from .space_entity import SpaceEntity
from .spaceship import Spaceship, UserSpaceship
from .asteroid import Asteroid
from .bullet import Bullet
# from .level import Level

# Optionally, define an __all__ list to control imports with 'from entities import *'
__all__ = [
    "SpaceObject"
    "Spaceship",
    "Asteroid",
    "Bullet",
    # "Level",
]
