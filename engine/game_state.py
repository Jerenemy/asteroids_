import pygame as pg
from graphics import Display, AnimationManager, ParticleExplosionAnimation, UserSpaceshipDeathAnimation
from .object_manager import ObjectManager
from entities import UserSpaceship, Asteroid, Bullet
from .high_scores_manager import HighScoresManager
from .time_manager import TimeManager
from utils import AssetManager, X_SCRNSIZE, Y_SCRNSIZE, is_mouse_pressed, check_quit, choose_color, WHITE, BULLET_SPEED, KeyManager, SSHIP_DESTRUCTION_DURATION, SPACEBAR, MAX_X_SCRNSIZE, MAX_Y_SCRNSIZE

class GameState:
    """
    A class to manage the state of the game, including player stats, game progress,
    and transitions between different game states.
    """
    def __init__(self, lives=3, current_level=1, points=0):
        """
        Initialize the GameState with default values.
        """
        self.lives = lives
        self.max_lives = lives
        self.current_level = current_level
        self.points = points
        self.state = "menu"  # Possible states: 'menu', 'playing', 'paused', 'game_over'
        self.high_scores_manager = HighScoresManager()
        self.asset_manager = AssetManager()
        self.screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))
        self.display = Display(self.screen, self.asset_manager)  # UI manager
        self.object_manager = ObjectManager()  # Manages dynamic game objects
        self.animation_manager = AnimationManager()
        self.spacebar_manager = KeyManager(pg.K_SPACE)
        self.f_key_manager = KeyManager(pg.K_f)
        self.time_manager = None # to be initialized upon game start  
        self.fullscreen = False

    def get_high_score(self, score_type):
        # if score_type == 'points':
        if self.high_scores_manager.is_high_score(self.points):
            self.high_scores_manager.save_high_scores(self.points)
        return self.high_scores_manager.get_top_score()
        # elif score_type == 'level':
            
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        if self.fullscreen:
            self.screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))  # Windowed mode
            self.fullscreen = False
        else:
            self.screen = pg.display.set_mode((MAX_X_SCRNSIZE, MAX_Y_SCRNSIZE), pg.FULLSCREEN)
            self.fullscreen = True
        # self.update_screen_size()

    def handle_events(self):
        """Process input and update the state accordingly."""
        for event in pg.event.get():
            if check_quit(event):
                self.state = "exit"
                return
        if self.f_key_manager.is_key_pressed_once():
            self.toggle_fullscreen()
        if self.state == "menu" and is_mouse_pressed(SPACEBAR):
            self.start_game()
        if self.state == "playing":
            self.handle_bullet_firing()
            # if self.lives <= 0: 
            #     self.state = "game_over"
        if self.state == "game_over" and is_mouse_pressed(SPACEBAR):
            self.reset_game()
        


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
        self.object_manager.update_objects()
        self.animation_manager.update_animations()  # Update animations
        self.handle_collisions()  # Handle collisions and update state
        if self.state == "playing":
            # self.object_manager.add_asteroids(self.time_manager)
            self.add_asteroids()



    def add_asteroids(self): # TODO: incorporate generation based on level
        """
        Add a new asteroid to the game if the appropriate time has elapsed.
        """
        if not self.time_manager.check_delta_time_elapsed():
            return
        x_scrnsize, y_scrnsize = pg.display.get_window_size()
        x, y, direction, size = Asteroid.generate_random_attributes(x_scrnsize, y_scrnsize)
        color = choose_color()
        asteroid = Asteroid(x, y, size, direction, color)
        self.object_manager.add_object(asteroid)


    
    def handle_collisions(self):
        """Process collision events and update game state."""
        collision_events = self.object_manager.get_collision_events()
        for event in collision_events:
            if event['type'] == 'bullet_hit_asteroid':
                ast = event['asteroid']
                # self.object_manager.
                self.add_score(ast.points)
                # Trigger animation
                self.animation_manager.add_animation(
                    ParticleExplosionAnimation(ast.x, ast.y, ast.color, particle_count=ast.size//8, max_lifetime=ast.size//8)
                )
            elif event['type'] == 'user_spaceship_hit':
                sship = event['spaceship']
                sship.is_destroying = True  # Set the state flag
                sship.delay_game_over_display = True
                self.animation_manager.add_animation(
                    UserSpaceshipDeathAnimation(sship, SSHIP_DESTRUCTION_DURATION)
                    # UserSpaceshipDeathAnimation(sship, 200, sship.orientation, sship.polygon)
                )
                self.animation_manager.add_animation(
                    ParticleExplosionAnimation(sship.x, sship.y, sship.color, particle_count=(sship.size//4), max_lifetime=(sship.size))
                )
                self.lose_life()

    def render_game(self):
        """Render UI and game objects based on the current state."""
        self.display.render() # might need to put this after everything, and just do screen.fill first.
        self.object_manager.render_objects(self.screen)
        self.animation_manager.render_animations(self.screen)
        if self.state == "menu":
            self.display.render_title_screen()
        elif self.state == "playing":
            self.display.render_hud( self.points, self.lives)
        elif self.state == "paused":
            self.display.render_paused()
        elif self.state == "game_over":
            # self.animation_manager.render_animations(self.screen)
            usship = self.object_manager.get_user_spaceship()
            # self.object_manager.render_objects(self.screen)
            # print(usship.delay_game_over_display)
            self.display.render_game_over(usship.is_destroying, usship.delay_game_over_display,  self.points, self.lives, self.get_high_score('points'), self.get_high_score('level'))
                
        pg.display.update()

        

    def start_game(self):
        """
        Start a new game by resetting the score and lives, and setting the state to 'playing'.
        and initialize game-specific objects and start the game.
        """
        self.state = "playing"
        self.lives = self.max_lives
        self.current_level = 1
        self.points = 0
        print("Game started.")
        # if len(self.object_manager.objects.values()) != 0:
        if not self.object_manager.objects['spaceships']:
            self.object_manager.add_object(UserSpaceship(X_SCRNSIZE/2, Y_SCRNSIZE/2, 20, 0, 0, WHITE, self.screen))
        self.object_manager.get_user_spaceship().lost_all_lives = False
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
        self.object_manager.get_user_spaceship().lost_all_lives = True
        print(f"Game over. Final score: { self.points}")

        # Add score to high scores if it's high enough
        self.high_scores_manager.add_score("Player",  self.points)

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
