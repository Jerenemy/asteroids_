from entities import SpaceEntity, Spaceship
from pygame import draw
from math import cos, sin, pi


class Bullet(SpaceEntity):
    def __init__(self, x, y, size, speed, direction, color, lifetime=25):
        super().__init__(x, y, size, speed, direction, color)
        self.lifetime = lifetime
    
    def render(self, screen):
        draw.circle(screen, self.color, [self.x, self.y], self.size)

    def move(self):
        """Move the bullet."""
        dx = self.speed * cos(self.direction * pi / 180)
        dy = self.speed * sin(self.direction * pi / 180)
        self.x += dx
        self.y += dy
        
    def should_despawn(self):
        if self.lifetime <= 0:
            return True
        self.lifetime -= 1
        return False
    
    @staticmethod
    def get_bullet_launch_attributes(sship: Spaceship) -> tuple:
        """gets the attributes needed of a bullet instance shot from a specific spaceship"""
        return (
            sship.x,
            sship.y,
            sship.orientation-90
        )
        