from entities import SpaceEntity
from pygame import draw
from math import cos, sin, pi


class Bullet(SpaceEntity):
    def __init__(self, x, y, size, speed, direction, color, lifetime=40):
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
    def get_bullet_launch_attributes(x, y, size, fire_direction, speed) -> tuple: # TODO: calculate speed compared to direction spaceship is moving (otherwise incorrect)
        """gets the attributes needed of a bullet instance shot from a specific spaceship"""
        # orientation = sship.orientation-90
        corrected_fire_direction = fire_direction - 90
        dx = size * cos(corrected_fire_direction * pi / 180)
        dy = size * sin(corrected_fire_direction * pi / 180)
        new_x = x + dx
        new_y = y + dy
        return (
            new_x,
            new_y,
            corrected_fire_direction,
            speed
        )
    
class UserBullet(Bullet):
    pass

class EnemyBullet(Bullet):
    def __init__(self, x, y, size, speed, direction, color, lifetime=100):
        super().__init__(x, y, size, speed, direction, color, lifetime)
        
    
        