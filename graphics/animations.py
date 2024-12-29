import pygame as pg

class ExplosionAnimation:
    def __init__(self, x, y, size, duration):
        self.x = x
        self.y = y
        self.size = size
        self.duration = duration  # Duration in frames
        self.elapsed = 0  # Frames elapsed
        self.finished = False

    def update(self):
        """Update the animation frame."""
        self.elapsed += 1
        if self.elapsed >= self.duration:
            self.finished = True

    def render(self, screen):
        """Render the explosion animation."""
        if not self.finished:
            radius = int(self.size * (self.elapsed / self.duration))
            alpha = max(0, 255 - int((self.elapsed / self.duration) * 255))
            color = (255, alpha, 0)  # Fading yellow
            pg.draw.circle(screen, color, (self.x, self.y), radius)
