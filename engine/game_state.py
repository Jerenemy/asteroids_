import pygame as pg
from graphics import Display, AnimationManager, ExplosionAnimation, UserSpaceshipDeathAnimation
from .object_manager import ObjectManager
from entities import UserSpaceship, Asteroid, Bullet
from .high_scores_manager import HighScoresManager
from .time_manager import TimeManager
from utils import AssetManager, X_SCRNSIZE, Y_SCRNSIZE, is_key_pressed, is_mouse_pressed, check_quit, choose_color, WHITE, BULLET_SPEED, KeyManager, SSHIP_DESTRUCTION_DURATION

class GameState:
    """
    A class to manage the state of the game, including player stats, game progress,
    and transitions between different game states.
    """
    def __init__(self, lives=3, current_level=1, score=0):
        """
        Initialize the GameState with default values.
        """
        self.lives = lives
        self.current_level = current_level
        self.score = score
        self.state = "menu"  # Possible states: 'menu', 'playing', 'paused', 'game_over'
        self.high_scores_manager = HighScoresManager()
        self.asset_manager = AssetManager()
        self.screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))
        self.display = Display(self.screen, self.asset_manager)  # UI manager
        self.object_manager = ObjectManager()  # Manages dynamic game objects
        self.animation_manager = AnimationManager()
        self.spacebar_manager = KeyManager(pg.K_SPACE)
        self.time_manager = None # to be initialized upon game start  

    def handle_events(self):
        """Process input and update the state accordingly."""
        for event in pg.event.get():
            if check_quit(event):
                self.state = "exit"
                return
        if self.state == "menu" and is_mouse_pressed(0):
            self.start_game()
        if self.state == "playing":
            self.handle_bullet_firing()


    # should add_asteroids be a method in object_manager, if it depends on the level from the game_state?
    # difference between time_manager and level_manager?
    def handle_bullet_firing(self):
        # if is_key_pressed(pg.K_SPACE):
        if self.spacebar_manager.is_key_pressed_once():
            # need access to spaceship attributes to initialize bullet
            x, y, direction = Bullet.get_bullet_launch_attributes(self.object_manager.get_user_spaceship())
            bullet = Bullet(x, y, 3, BULLET_SPEED, direction, WHITE)
            self.object_manager.add_object(bullet)
            # print(f"added object, len bullet list = {len(self.object_manager.objects['bullets'])}")


    def update_game(self):
        """Update game objects and logic if in 'playing' state."""
        if self.state == "playing":
            self.object_manager.update_objects()
            # self.object_manager.add_asteroids(self.time_manager)
            # self.add_asteroids()
            self.handle_collisions()  # Handle collisions and update state
            self.animation_manager.update_animations()  # Update animations



    def add_asteroids(self): # TODO: incorporate generation based on level
        """
        Add a new asteroid to the game if the appropriate time has elapsed.
        """
        if not self.time_manager.check_delta_time_elapsed():
            return
        x, y, direction, size = Asteroid.generate_random_attributes(X_SCRNSIZE, Y_SCRNSIZE)
        color = choose_color()
        asteroid = Asteroid(x, y, size, direction, color)
        self.object_manager.add_object(asteroid)


    
    def handle_collisions(self):
        """Process collision events and update game state."""
        collision_events = self.object_manager.get_collision_events()
        for event in collision_events:
            if event['type'] == 'bullet_hit_asteroid':
                # self.object_manager.
                self.add_score(event['points'])
                # Trigger animation
                self.animation_manager.add_animation(
                    ExplosionAnimation(event['x'], event['y'], event['size'], event['duration'])
                )
            elif event['type'] == 'user_spaceship_hit':
                sship = event['spaceship']
                sship.is_destroying = True  # Set the state flag
                self.animation_manager.add_animation(
                    UserSpaceshipDeathAnimation(sship, SSHIP_DESTRUCTION_DURATION)
                    # UserSpaceshipDeathAnimation(sship, 200, sship.orientation, sship.polygon)
                )
                self.lose_life()

    def render_game(self):
        """Render UI and game objects based on the current state."""
        # self.screen.fill((0, 0, 0))  #  Clear the screen
        self.display.render() # might need to put this after everything, and just do screen.fill first.
        if self.state == "menu":
            self.display.render_title_screen()
        elif self.state == "playing":
            self.animation_manager.render_animations(self.screen)  # Render animations
            self.object_manager.render_objects(self.screen)
            self.display.render_hud(self.score, self.lives)
        elif self.state == "paused":
            self.display.render_paused()
        pg.display.update()

        

    def start_game(self):
        """
        Start a new game by resetting the score and lives, and setting the state to 'playing'.
        and initialize game-specific objects and start the game.
        """
        self.state = "playing"
        self.current_level = 1
        self.score = 0
        self.lives = 3
        print("Game started. Good luck!")
        self.object_manager.add_object(UserSpaceship(X_SCRNSIZE/2, Y_SCRNSIZE/2, 20, 0, 0, WHITE, self.screen))
        self.time_manager = TimeManager()

        # should have time_manager class?
        # self.object_manager.add_object(Asteroid(0, 0, 40, 2, 60, WHITE))


    def pause_game(self):
        """
        Pause the game if it's currently playing.
        """
        if self.state == "playing":
            self.state = "paused"
            print("Game paused.")

    def resume_game(self):
        """
        Resume the game if it's currently paused.
        """
        if self.state == "paused":
            self.state = "playing"
            print("Game resumed.")

    def end_game(self):
        """
        End the game, transitioning to the 'game_over' state.
        """
        self.state = "game_over"
        print(f"Game over. Final score: {self.score}")

        # Add score to high scores if it's high enough
        self.high_scores_manager.add_score("Player", self.score)

    def lose_life(self):
        """
        Decrease the player's lives by one and check for game over.
        """
        self.lives -= 1
        print(f"Lives remaining: {self.lives}")
        if self.lives <= 0:
            self.end_game()

    def advance_level(self):
        """
        Advance to the next level and increase the difficulty.
        """
        self.current_level += 1
        print(f"Level {self.current_level} started. Prepare yourself!")

    def add_score(self, points):
        """
        Add points to the player's score.

        Args:
            points (int): The number of points to add.
        """
        self.score += points
        print(f"Score updated: {self.score}")

    def reset_game(self):
        """
        Reset the game state to prepare for a new game.
        """
        self.start_game()

    def get_game_state(self):
        """
        Retrieve the current game state for debugging or display purposes.

        Returns:
            dict: A dictionary containing the current game state.
        """
        return {
            "state": self.state,
            "current_level": self.current_level,
            "score": self.score,
            "lives": self.lives,
        }



# Example usage
if __name__ == "__main__":
    from engine.high_scores_manager import HighScoresManager

    game_state = GameState()

    game_state.start_game()
    game_state.add_score(100)
    game_state.lose_life()
    game_state.pause_game()
    game_state.resume_game()
    game_state.advance_level()
    game_state.lose_life()
    game_state.lose_life()
    print("Game state:", game_state.get_game_state())
