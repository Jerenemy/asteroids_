import pygame as pg
# import math
from math import cos, sin, pi, hypot, atan2
from abc import ABC, abstractmethod

class Line: 
    def __init__(self, x0, y0, x1, y1, color):
        self.color = color
        self.width = 3
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.center_x = (x1 + x0) / 2
        self.center_y = (y1 + y0) / 2

        self.half_length = hypot(x1 - x0, y1 - y0) / 2
        self.angle = atan2(0 - y1, x1 - x0)

    def rotate(self, angle):
        #rotates line by given angle in degrees
        angle *= pi / 180
        self.angle += angle
        dx = self.half_length * cos(self.angle)
        dy = -self.half_length * sin(self.angle)
        self.x0 = self.center_x - dx
        self.y0 = self.center_y - dy
        self.x1 = self.center_x + dx
        self.y1 = self.center_y + dy

    def draw(self, surface):
        pg.draw.line(
            surface,
            self.color,
            (self.x0, self.y0),
            (self.x1, self.y1),
            self.width
        )



class Polygon(ABC):
    def __init__(self, center_x, center_y, color, width):
        self.center_x = center_x
        self.center_y = center_y
        self.color = color
        self.width = width
    
    @property
    @abstractmethod
    def vertices(self):
        """Calculate vertices of the polygon."""
        pass
    
    def render(self, screen):
        """Draw the polygon on the given screen."""
        pg.draw.polygon(screen, self.color, self.vertices, self.width)
    
    def move(self, dx, dy):
        """Move the polygon by a certain offset."""
        self.center_x += dx
        self.center_y += dy
        
class RandomPolygon(Polygon):
    def __init__(self, center_x, center_y, base_radius, sides, color, width, radii=None):
        super().__init__(center_x, center_y, color, width)
        """
        Initialize a polygon with potentially varying radii for each vertex.
        
        Args:
            center_x (float): X-coordinate of the polygon's center.
            center_y (float): Y-coordinate of the polygon's center.
            base_radius (float): Base radius of the polygon.
            sides (int): Number of sides.
            color (tuple): RGB color of the polygon.
            width (int): Line width for drawing the polygon.
            radii (list, optional): List of radii for each vertex. If None, uses base_radius for all vertices.
        """
        self.sides = sides
        self.base_radius = base_radius
        self.radii = radii or [base_radius] * sides

    @property
    def vertices(self):
        """Calculate vertices of the polygon with varying radii."""
        angle_increment = 2 * pi / self.sides
        vertices = []
        for i in range(self.sides):
            angle = i * angle_increment
            radius = self.radii[i]
            x = self.center_x + radius * cos(angle)
            y = self.center_y + radius * sin(angle)
            vertices.append((x, y))
        return vertices



class UserSpaceshipPolygon(Polygon):
    def __init__(self, center_x, center_y, color, width, size, orientation):
        super().__init__(center_x, center_y, color, width)
        self.size = size
        self.orientation = orientation

class UserSpaceshipPolygon(UserSpaceshipPolygon):
    def __init__(self, center_x, center_y, color, width, size, orientation):
        super().__init__(center_x, center_y, color, width, size, orientation)
        
    @property
    def vertices(self):
        """Calculate vertices of the polygon with specific radii to form the spaceship 'A' shape."""
        #define coordinate for front of spacecraft
        x_front = self.center_x + (self.size * cos(pi / 180 * (self.orientation - 90) ))
        y_front = self.center_y + (self.size * sin(pi / 180 * (self.orientation - 90) ))

        #define coordinate for back right of spacecraft
        x_backright = self.center_x + ((self.size * .8) * cos(pi / 180 * (140 + 15 + self.orientation - 90) ))
        y_backright = self.center_y + ((self.size * .8) * sin(pi / 180 * (140 + 15 + self.orientation - 90) ))
  
        #define coordinate for back left of spacecraft
        x_backleft = self.center_x + ((self.size * .8) * cos(pi / 180 * (220 - 15 + self.orientation - 90) ))
        y_backleft = self.center_y + ((self.size * .8) * sin(pi / 180 * (220 - 15 + self.orientation - 90) ))
        
        #define coordinate for back right of spacecraft
        x_endright = self.center_x + ((self.size * 1.4) * cos(pi / 180 * (140 + 20 + self.orientation - 90) ))
        y_endright = self.center_y + ((self.size * 1.4) * sin(pi / 180 * (140 + 20 + self.orientation - 90) ))
  
        #define coordinate for back left of spacecraft
        x_endleft = self.center_x + ((self.size * 1.4) * cos(pi / 180 * (220 - 20 + self.orientation - 90) ))
        y_endleft = self.center_y + ((self.size * 1.4) * sin(pi / 180 * (220 - 20 + self.orientation - 90) ))    
        
        return [(x_front, y_front), (x_endright, y_endright), (x_backright, y_backright), (x_backleft, y_backleft), (x_endleft, y_endleft)] 
        

class RocketPolygon(UserSpaceshipPolygon):
    def __init__(self, center_x, center_y, color, width, size, orientation):
        super().__init__(center_x, center_y, color, width, size, orientation)
    
    @property
    def vertices(self):
        # tip
        x_rocket = self.center_x + ((self.size * 1.4) * cos(pi / 180 * (180 + self.orientation - 90) ))
        y_rocket = self.center_y + ((self.size * 1.4) * sin(pi / 180 * (180 + self.orientation - 90) ))
        # 
        x_rocketleft = self.center_x + ((self.size * .8) * cos(pi / 180 * (180 + 20 + self.orientation - 90) ))
        y_rocketleft = self.center_y + ((self.size * .8) * sin(pi / 180 * (180 + 20 + self.orientation - 90) ))    
        # 
        x_rocketright = self.center_x + ((self.size * .8) * cos(pi / 180 * (180 - 20 + self.orientation - 90) ))
        y_rocketright = self.center_y + ((self.size * .8) * sin(pi / 180 * (180 - 20 + self.orientation - 90) ))
        return [(x_rocket, y_rocket), (x_rocketleft, y_rocketleft), (x_rocketright, y_rocketright)]

    