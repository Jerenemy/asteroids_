import pygame
from math import cos, sin, pi, sqrt
from random import randrange, uniform, choice, randint
from .space_entity import SpaceEntity
from utils import RandomPolygon


class Asteroid(SpaceEntity):
    def __init__(self, x, y, size, direction, color, speed=None, width=3):
        speed = speed or (300 / size + 1 )
        super().__init__(x, y, size, speed, direction, color)
        self.width = width
        self.sides = 8
        self.polygon = RandomPolygon(x, y, size, self.sides, color, 3, self._radii)
        self.points = 10 if size > 30 else 100
        
    def should_despawn(self):
        return self.is_out_of_bounds
    
    @property
    def _radii(self) -> list:
        """Generate random radii for each vertex."""
        min_radius = self.size * 0.5
        max_radius = self.size * 1.5
        return [uniform(min_radius, max_radius) for _ in range(self.sides)]

    def move(self):
        """Move the asteroid."""
        dx = self.speed * cos(self.direction * pi / 180)
        dy = self.speed * sin(self.direction * pi / 180)
        self.x += dx
        self.y += dy
        self.polygon.move(dx, dy)

    def render(self, screen):
        """Render the asteroid using its polygon."""
        self.polygon.render(screen)

    @staticmethod
    def generate_random_attributes(screen_width: int, screen_height: int) -> tuple:
        """
        Generate a random position and direction for an asteroid to spawn along the edges of the screen.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.

        Returns:
            tuple: (x, y, direction, size), where (x, y) is the spawn position, direction is the angle in degrees, and size is the "radius" in pixels.
        """
        size = randint(30, 150) # TODO: change to be fraction of screen
        edge = choice(['top', 'right', 'bottom', 'left'])
        if edge == 'top':  # Spawns at the top edge, moves downward
            x = randint(0, screen_width)
            y = -size
            direction = randint(0, 180)  # Angles to move downward and onto the screen
        elif edge == 'right':  # Spawns at the right edge, moves leftward
            x = screen_width + size
            y = randint(0, screen_height)
            direction = randint(90, 270)  # Angles to move leftward and onto the screen
        elif edge == 'bottom':  # Spawns at the bottom edge, moves upward
            x = randint(0, screen_width)
            y = screen_height + size
            direction = randint(180, 360)  # Angles to move upward and onto the screen
        elif edge == 'left':  # Spawns at the left edge, moves rightward
            x = -size
            y = randint(0, screen_height)
            direction = randint(270, 450)  # Angles to move rightward and onto the screen
        return x, y, direction, size
    
    def check_distance(self, bullet_list):       
        """#Method check_distance in Class Asteroid - check asteroid distance against bullet list"""    
        i = 0
        while i < len(bullet_list):   
            d = sqrt(((bullet_list[i].x_coord - self.x_coord) ** 2) + ((bullet_list[i].y_coord - self.y_coord) ** 2) )
            if d <= bullet_list[i].size + self.size:
                self.hit = 1
                #self.speed = 0
                return(1)
            i = i + 1
        return(0)

    def check_distance_spaceship(self, spaceship):       
        """#not being used"""
        d = sqrt(((spaceship.x_coord - self.x_coord) ** 2) + ((spaceship.y_coord - self.y_coord) ** 2) )
        if d <= spaceship.size + self.size:
            self.hit = 1
            #self.speed = 0
            return(1)
        return(0)
        