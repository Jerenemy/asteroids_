from abc import ABC, abstractmethod
import math
from utils import X_SCRNSIZE, Y_SCRNSIZE
from pygame import display


class SpaceEntity(ABC):
    def __init__(self, x, y, size, speed, direction, color):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.direction = direction
        self.color = color

    @abstractmethod
    def move(self):
        """Update the object's position."""
        pass

    @abstractmethod
    def render(self, screen):
        """Render the object on the screen."""
        pass

    @abstractmethod
    def should_despawn(self) -> bool:
        """
        Determine if the object should despawn.
        This must be implemented by all subclasses.
        """
        pass

    def check_collision(self, other):
        """Check if this object collides with another space object."""
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < self.size + other.size
    
    @property
    def is_out_of_bounds(self):
        """Check if the object is outside the screen boundaries."""
        x_scrnsize, y_scrnsize = display.get_window_size()
        return (
            self.x < -self.size or self.x > x_scrnsize + self.size or
            self.y < -self.size or self.y > y_scrnsize + self.size
        )

    
    # def destroy(self): 
    #     """Handle logic if object is destroyed"""
    #     pass
