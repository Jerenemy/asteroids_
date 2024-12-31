import pygame as pg
from abc import ABC, abstractmethod
from math import cos, sin, pi
from utils import Line, X_SCRNSIZE, Y_SCRNSIZE
from random import random, uniform

class Animation(ABC):
    def __init__(self, x, y, size, duration):
        self.x = x
        self.y = y
        self.size = size
        self.duration = duration
        self.elapsed = 0  # Frames elapsed
        self.finished = False

    @abstractmethod
    def update(self):
        """Update the animation state."""
        pass

    @abstractmethod
    def render(self, screen):
        """Render the animation on the screen."""
        pass

class ExplosionAnimation(Animation):
    def __init__(self, x, y, size, duration):
        super().__init__(x, y, size, duration)

    def update(self):
        self.elapsed += 1
        if self.elapsed >= self.duration:
            self.finished = True

    def render(self, screen):
        if not self.finished:
            radius = int(self.size * (self.elapsed / self.duration))
            alpha = max(0, 255 - int((self.elapsed / self.duration) * 255))
            color = (255, alpha, 0)  # Fading yellow
            pg.draw.circle(screen, color, (self.x, self.y), radius)

class UserSpaceshipDeathAnimation(Animation):
    def __init__(self, spaceship, duration):
        super().__init__(spaceship.x, spaceship.y, spaceship.size, duration)
        self.spaceship = spaceship
        self.orientation = spaceship.orientation
        self.polygon = spaceship.polygon
        self.lines = []  # Store all destructed lines

    def _calculate_lines(self):
        vertices = self.polygon.vertices
        directions = [-90, 90, 180]  # Angles for line dispersion

        new_lines = []
        for idx, angle in enumerate(directions):
            start = vertices[idx * 2]  # Starting vertex for each line
            end = vertices[(idx * 2 + 1) % len(vertices)]  # Next vertex

            displacement = self.elapsed
            new_start = (
                start[0] + displacement * cos(pi / 180 * (self.orientation - 90 + angle)),
                start[1] + displacement * sin(pi / 180 * (self.orientation - 90 + angle))
            )
            new_end = (
                end[0] + displacement * cos(pi / 180 * (self.orientation - 90 + angle)),
                end[1] + displacement * sin(pi / 180 * (self.orientation - 90 + angle))
            )

            # Calculate color fading
            fade_ratio = self.elapsed / (self.duration)
            color = (
                max(0, 255 - int(fade_ratio * 255)),
                max(0, 255 - int(fade_ratio * 255)),
                max(0, 255 - int(fade_ratio * 255))
            )

            new_lines.append(Line(*new_start, *new_end, color))

        return new_lines

    def update(self):
        self.elapsed += 1
        if self.elapsed == self.duration//2:
            print("here")
            self.spaceship.delay_game_over_display = False
        if self.elapsed >= self.duration:
            self.spaceship.is_destroying = False
            self.finished = True
            self.spaceship.destroy()

        self.lines = self._calculate_lines()

    def render(self, screen):
        for idx, line in enumerate(self.lines):
            
            if not hasattr(self, 'rotation_speed'):
                self.rotation_speed = [
                        (3*uniform(-1,1)*self.spaceship.speed), 
                        (3*uniform(-1,1)*self.spaceship.speed), 
                        (-3*uniform(-1,1)*self.spaceship.speed)
                    ][idx]  # Different rotation speeds for variety
            line.rotate(self.rotation_speed * self.elapsed)
            line.draw(screen)

