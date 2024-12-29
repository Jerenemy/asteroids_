class AnimationManager:
    def __init__(self):
        self.animations = []  # A list of active animations

    def add_animation(self, animation):
        """Add a new animation."""
        self.animations.append(animation)

    def update_animations(self):
        """Update all active animations."""
        for animation in self.animations[:]:  # Iterate over a copy to allow safe removal
            animation.update()
            if animation.finished:
                self.animations.remove(animation)

    def render_animations(self, screen):
        """Render all active animations."""
        for animation in self.animations:
            animation.render(screen)
