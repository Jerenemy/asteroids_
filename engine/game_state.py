import pygame as pg
from graphics import Display, AnimationManager, ParticleExplosionAnimation, UserSpaceshipDeathAnimation
from .object_manager import ObjectManager
from entities import UserSpaceship, Asteroid, Bullet
from .high_scores_manager import HighScoresManager
from .level_manager import LevelManager
from utils import AssetManager, is_mouse_pressed, check_quit, choose_color, X_SCRNSIZE, Y_SCRNSIZE, WHITE, BULLET_SPEED, KeysManager, SSHIP_DESTRUCTION_DURATION, SPACEBAR, MAX_X_SCRNSIZE, MAX_Y_SCRNSIZE
from graphics import DisplayElement

class GameState:
    """
    A class to manage the state of the game, including player stats, game progress,
    and transitions between different game states.
    """
    def __init__(self, lives=3, points=0):
        """
        Initialize the GameState with default values.
        """
        self.lives = lives
        self.max_lives = lives
        self.points = points
        self.state = "menu"  # Possible states: 'menu', 'playing', 'paused', 'game_over'
        self.high_scores_manager = HighScoresManager()
        self.asset_manager = AssetManager()
        self.screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))
        self.display = Display(self.screen, self.asset_manager)  # UI manager
        self.object_manager = ObjectManager()  # Manages dynamic game objects
        self.animation_manager = AnimationManager()
        self.keys_manager = KeysManager()
        # self.spacebar_manager = KeyManager(pg.K_SPACE)
        # self.f_key_manager = KeyManager(pg.K_f)
        self.level_manager = None # to be initialized upon game start  
        self.fullscreen = False

    @property
    def current_level(self):
        return self.level_manager.current_level
    
    def get_high_score(self, score_type):
        # if score_type == 'points': # TODO: implement level high scores
        if self.high_scores_manager.is_high_score(self.points):
            self.high_scores_manager.save_high_scores(self.points)
        return self.high_scores_manager.get_top_score()
        # elif score_type == 'level':
       
    @property
    def x_scrnsize(self):
        try:
            x, _ = pg.display.get_window_size()
            return x
        except Exception as e:
            return X_SCRNSIZE
    
    @property
    def y_scrnsize(self):
        try:
            _, y = pg.display.get_window_size()
            return y
        except Exception as e:
            return Y_SCRNSIZE 
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        if self.fullscreen:
            self.screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))  # Windowed mode
            self.fullscreen = False
        else:
            self.screen = pg.display.set_mode((MAX_X_SCRNSIZE, MAX_Y_SCRNSIZE), pg.FULLSCREEN)
            self.fullscreen = True

    def handle_events(self):
        """Process input and update the state accordingly."""
        for event in pg.event.get():
            if check_quit(event):
                self.state = "exit"
                return
        # if self.f_key_manager.is_key_pressed_once():
        if self.keys_manager(pg.K_f).is_key_pressed_once():
            self.toggle_fullscreen()
        if self.state == "menu" and is_mouse_pressed(SPACEBAR):
            self.start_game()
        if self.state == "playing":
            self.handle_bullet_firing()
            # if self.lives <= 0: 
            #     self.state = "game_over"
        if self.state == "game_over" and is_mouse_pressed(SPACEBAR):
            self.reset_game()  

    # NOTE: should add_asteroids be a method in object_manager, if it depends on the level from the game_state?
    def handle_bullet_firing(self):
        # if is_key_pressed(pg.K_SPACE):
        # if self.spacebar_manager.is_key_pressed_once():
        if self.keys_manager(pg.K_SPACE).is_key_pressed_once():
            # need access to spaceship attributes to initialize bullet
            x, y, direction = Bullet.get_bullet_launch_attributes(self.object_manager.get_user_spaceship())
            bullet = Bullet(x, y, 3, BULLET_SPEED, direction, WHITE)
            self.object_manager.add_object(bullet)
            # print(f"added object, len bullet list = {len(self.object_manager.objects['bullets'])}")

    def update_game(self):
        """Update game objects and logic if in 'playing' state."""
        self.object_manager.update_objects()
        self.animation_manager.update_animations()  # Update animations
        self.handle_collisions()  # Handle collisions and update state
        if self.state == "playing":
            self.add_asteroids()
            self.level_manager.update()

    def add_asteroids(self): # TODO: incorporate generation based on level
        """
        Add a new asteroid to the game if the appropriate time has elapsed.
        """
        if not self.level_manager.asteroid_time_manager.check_delta_time_elapsed():
            return
        x, y, direction, size = Asteroid.generate_random_attributes(self.x_scrnsize, self.y_scrnsize)
        color = choose_color()
        asteroid = Asteroid(x, y, size, direction, color)
        self.object_manager.add_object(asteroid)
    
    def handle_collisions(self):
        """Process collision events and update game state."""
        collision_events = self.object_manager.get_collision_events()
        for event in collision_events:
            if event['type'] == 'bullet_hit_asteroid':
                ast = event['asteroid']
                self.add_score(ast.points)
                # Trigger animation
                self.animation_manager.add_animation(
                    ParticleExplosionAnimation(ast.x, ast.y, ast.color, particle_count=ast.size//8, max_lifetime=ast.size//8)
                )
            elif event['type'] == 'user_spaceship_hit':
                sship = event['spaceship']
                if sship.is_destroying or sship.lost_all_lives: # don't allow for destroy if already destroyed
                    continue
                sship.is_destroying = True  # Set the state flag
                sship.delay_game_over_display = True
                self.animation_manager.add_animation(
                    UserSpaceshipDeathAnimation(sship, SSHIP_DESTRUCTION_DURATION)
                )
                self.animation_manager.add_animation(
                    ParticleExplosionAnimation(sship.x, sship.y, sship.color, particle_count=(sship.size//4), max_lifetime=(sship.size))
                )
                self.lose_life()

    def play_sounds(self):
        if self.state == "playing":
            self.level_manager.play_level_sound()
    
    def render_game(self):
        """Render UI and game objects based on the current state."""
        self.display.render() # might need to put this after everything, and just do screen.fill first.
        if self.state == "playing": # render the level behind the objects
            self.display.render_new_level(self.current_level, self.level_manager.display_new_level, self.level_manager.get_level_color_counter())
        self.object_manager.render_objects(self.screen)
        self.animation_manager.render_animations(self.screen)
        if self.state == "menu":
            self.display.render_title_screen(self.get_high_score('points'), self.get_high_score('level'))
        elif self.state == "playing":
            self.display.render_hud(self.points, self.lives)
            # self.display.render_new_level(self.current_level, self.level_manager.display_new_level, self.level_manager.get_level_color_counter())
        elif self.state == "paused":
            self.display.render_paused()
        elif self.state == "game_over":
            # self.object_manager.render_objects(self.screen)
            # self.animation_manager.render_animations(self.screen)
            usship = self.object_manager.get_user_spaceship()
            self.display.render_game_over(
                usship.is_destroying, 
                usship.delay_game_over_display, 
                self.points, 
                self.current_level, 
                self.get_high_score('points'), 
                self.get_high_score('level')
            )
        pg.display.update()    

    def start_game(self):
        """
        Start a new game by resetting the score and lives, and setting the state to 'playing'.
        and initialize game-specific objects and start the game.
        """
        self.state = "playing"
        self.lives = self.max_lives
        self.points = 0
        print("Game started.")
        if not self.object_manager.objects['spaceships']:
            self.object_manager.add_object(UserSpaceship(self.x_scrnsize/2, self.y_scrnsize/2, 20, 0, 0, WHITE, self.screen))
        self.object_manager.get_user_spaceship().lost_all_lives = False
        self.level_manager = LevelManager(self.asset_manager)

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
        self.object_manager.get_user_spaceship().lost_all_lives = True
        print(f"Game over. Final score: { self.points}")
        # Add score to high scores if it's high enough
        self.high_scores_manager.add_score("Player", self.points, self.current_level)

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
        # self.current_level += 1
        print(f"Level {self.current_level} started. Prepare yourself!")

    def add_score(self, points):
        """
        Add points to the player's score.

        Args:
            points (int): The number of points to add.
        """
        self.points += points
        print(f"Score updated: {self.points}")

    def reset_game(self):
        """
        Reset the game state to prepare for a new game.
        """
        if not self.object_manager.get_user_spaceship().is_destroying:
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
            "score": self.points,
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
