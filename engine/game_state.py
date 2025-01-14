import pygame as pg
from graphics import Display, AnimationManager, ParticleExplosionAnimation, UserSpaceshipDeathAnimation, RenderManager, DisplaySpaceshipLives
from .object_manager import ObjectManager
from entities import UserSpaceship, Asteroid, Bullet, UserBullet, EnemyBullet, EnemySpaceship
from .high_scores_manager import HighScoresManager
from .level_manager import LevelManager
from sounds import SoundManager
WAIT_AFTER_ENTERING_INITIALS_TIME = 1000
from utils import AssetManager, is_mouse_pressed, check_quit, choose_color, X_SCRNSIZE, Y_SCRNSIZE, WHITE, BULLET_SPEED, KeysManager, SSHIP_DESTRUCTION_DURATION, LEFT_CLICK, MAX_X_SCRNSIZE, MAX_Y_SCRNSIZE, TimeManager, is_key_pressed, WAIT_AFTER_ENTERING_INITIALS_TIME, INVULNERABLE_TIME, BULLET_SIZE, direction_overlap

# INITIALIZE OBJECTS
high_scores_manager = HighScoresManager()
asset_manager = AssetManager()
object_manager = ObjectManager()
animation_manager = AnimationManager()
keys_manager = KeysManager()
screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))
display = Display(screen, asset_manager)  # UI manager
render_manager = RenderManager()
sound_manager = SoundManager(asset_manager)  


class GameState:
    """
    A class to manage the state of the game, including player stats, game progress,
    and transitions between different game states.
    """
    def __init__(self, lives, points=0):
        """
        Initialize the GameState with default values.
        """
        self.lives = lives
        self.max_lives = lives
        self.points = points
        self.state = "title_menu"  # Possible states: 'title_menu', 'playing', 'paused', 'game_over', 'new_high_score', 'game_over_menu'
        self.level_manager = LevelManager(asset_manager) # to be re-initialized upon game start  
        self.fullscreen = False
        self.name = None
        self.initials = []
        self.last_high_score_initials = None
        self.delay_trans_tm = None # will be init'ed to be a TimeManager that delays the transition away from the new_high_score state so you can see the initials you entered for a sec
        self.allow_lose_life = False


    @property
    def current_level(self):
        return self.level_manager.current_level
    
    def get_high_score(self, score_type: str) -> tuple:
        if self.state != "game_over_menu":
            return high_scores_manager.get_top_score(score_type)
        if score_type == 'points':
            if high_scores_manager.is_high_score(self.points, score_type):
                print(self.last_high_score_initials)
                high_scores_manager.save_new_high_score(self.last_high_score_initials, self.points, score_type)
        elif score_type == 'level':
            if high_scores_manager.is_high_score(self.current_level, score_type):
                high_scores_manager.save_new_high_score(self.last_high_score_initials, self.current_level, score_type)
        return high_scores_manager.get_top_score(score_type)
       
    
    @property
    def x_scrnsize(self):
        try:
            x, _ = pg.display.get_window_size()
            return x
        except pg.error as e:
            return X_SCRNSIZE
    
    @property
    def y_scrnsize(self):
        try:
            _, y = pg.display.get_window_size()
            return y
        except pg.error as e:
            return Y_SCRNSIZE 
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        if self.fullscreen:
            screen = pg.display.set_mode((X_SCRNSIZE, Y_SCRNSIZE))  # Windowed mode
            self.fullscreen = False
        else:
            screen = pg.display.set_mode((MAX_X_SCRNSIZE, MAX_Y_SCRNSIZE), pg.FULLSCREEN)
            self.fullscreen = True

    def hide_cursor_while_playing(self):
        if self.state == "playing":
            pg.mouse.set_visible(0)
        else:
            pg.mouse.set_visible(1)

    def handle_events(self):
        """Process input and update the state accordingly."""
        for event in pg.event.get():
            if check_quit(event):
                self.state = "exit"
                return
        if self.state != "new_high_score":
            if keys_manager.is_key_pressed(pg.K_f):
                self.toggle_fullscreen()
            if is_key_pressed(pg.K_q):
                self.state = "exit"
                return
        if self.state == "title_menu":
            if is_mouse_pressed(LEFT_CLICK) or is_key_pressed(pg.K_SPACE):
                self.start_game()
        elif self.state == "game_over_menu":
            if is_mouse_pressed(LEFT_CLICK) or is_key_pressed(pg.K_SPACE):
                self.start_game()
        elif self.state == "playing":
            self.handle_user_bullet_firing()
            if keys_manager.is_key_pressed(pg.K_p):
                self.pause_game()
        elif self.state == "game_over":
            sship = object_manager.get_user_spaceship()
            if not sship.is_destroying:
                if self.is_high_score():  
                    self.state = "new_high_score"
                else: self.state = "game_over_menu"
        elif self.state == "new_high_score":
            initial = keys_manager.get_key_pressed_once()
            if initial is not None and len(self.initials) < 3:
                self.initials += [initial.upper()]
            if self.delay_trans_tm is None and len(self.initials) == 3:
                self.delay_trans_tm = TimeManager(WAIT_AFTER_ENTERING_INITIALS_TIME)
            if self.delay_trans_tm is not None and self.delay_trans_tm.check_delta_time_elapsed():
                self.last_high_score_initials = ''.join(self.initials) # if i wipe the initials now, is that fine? i need to pass the initials into the init_layers_to_render
                self.delay_trans_tm = None
                self.state = "game_over_menu"
        elif self.state == "paused":
            if keys_manager.is_key_pressed(pg.K_p):
                self.resume_game()
            if keys_manager.is_key_pressed(pg.K_r):
                self.reset_game()
                # self.end_game()
                # TimeManager.paused = False
                # DisplaySpaceshipLives.wipe_lives()
                # self.lives = 0
                # self.state = "title_menu"
            
    def handle_user_bullet_firing(self):
        if not object_manager.get_user_spaceship().is_destroying and keys_manager.is_key_pressed(pg.K_SPACE):
            # need access to spaceship attributes to initialize bullet
            user_sship = object_manager.get_user_spaceship()
            x, y, direction, sship_speed = Bullet.get_bullet_launch_attributes(user_sship.x, user_sship.y, user_sship.size, user_sship.orientation, user_sship.speed)
            bullet_speed = BULLET_SPEED + sship_speed * direction_overlap(user_sship.direction, user_sship.orientation)
            bullet = UserBullet(x, y, BULLET_SIZE, bullet_speed, direction, WHITE)
            object_manager.add_object(bullet)
            sound_manager.play_event_sound('shoot') 

        
    def update_game(self):
        """Update game objects and logic if in 'playing' state."""
        if self.state != "paused":
            object_manager.update_objects()
            animation_manager.update_animations()  # Update animations
            self.handle_collisions()  # Handle collisions and update state
            self.add_enemies()
            if self.state == "playing":
                object_manager.fire_enemy_sship_bullets(self.current_level)
                self.level_manager.update(
                    len(object_manager.get_object_list2('asteroids'))
                    + len(object_manager.get_object_list2('enemy_spaceships'))
                )
                self.lose_life_after_destruction()

    def add_enemies(self): # TODO: incorporate generation based on level
        """
        Add a new asteroid to the game if the appropriate time has elapsed.
        """
        if not self.level_manager.new_level_approaching:
            self.add_asteroids()
            self.add_enemy_sships()
    
    def add_asteroids(self):
        if not self.level_manager.asteroid_time_manager.check_delta_time_elapsed():
            # print(self.level_manager.asteroid_time_manager.elapsed_time, self.level_manager.asteroid_time_manager.delta_time)
            return
        # add asteroids
        x, y, direction, size = Asteroid.generate_random_attributes(self.x_scrnsize, self.y_scrnsize)
        color = choose_color()
        asteroid = Asteroid(x, y, size, direction, color)
        object_manager.add_object(asteroid)
        
    def add_enemy_sships(self):
        if not self.level_manager.enemy_sship_time_manager.check_delta_time_elapsed():
            return
        color, x, y, size, speed, direction = EnemySpaceship.generate_random()
        # print(color, x, y, direction)
        enemy_sship = EnemySpaceship(x, y, size, speed, direction, color, screen, sound_manager)
        object_manager.add_object(enemy_sship)
        # print('added')
    
        
    def handle_collisions(self):
        """Process collision events and update game state."""
        collision_events = object_manager.get_collision_events()
        for event in collision_events:
            if event['type'] == 'bullet_hit_asteroid':
                ast = event['asteroid']
                if isinstance(event['collided_with'], UserBullet):
                    self.add_score(ast.points)
                # Trigger animation
                animation_manager.add_animation(
                    ParticleExplosionAnimation(ast.x, ast.y, ast.color, particle_count=ast.size//8, max_lifetime=ast.size//8)
                )
            elif event['type'] == 'user_spaceship_hit':
                # continue
                sship = event['spaceship']
                if sship.is_destroying or sship.lost_all_lives: # don't allow for destroy if already destroyed
                    continue
                sship.is_destroying = True 
                sship.delay_game_over_display = True
                animation_manager.add_animation(
                    UserSpaceshipDeathAnimation(sship, SSHIP_DESTRUCTION_DURATION)
                )
                animation_manager.add_animation(
                    ParticleExplosionAnimation(sship.x, sship.y, sship.color, particle_count=(sship.size//4), max_lifetime=(sship.size))
                )
                self.allow_lose_life = True
                # self.lose_life()
            elif event['type'] == 'enemy_spaceship_hit':
                enemy_sship = event['spaceship']
                if isinstance(event['collided_with'], UserBullet):
                    self.add_score(enemy_sship.points)
                animation_manager.add_animation(
                    ParticleExplosionAnimation(enemy_sship.x, enemy_sship.y, enemy_sship.color, particle_count=enemy_sship.size//8, max_lifetime=enemy_sship.size//8)
                )
            sound_manager.play_event_sound(event['type'])

    def play_sounds(self): # TODO: fix this
        if self.state == "playing":
            self.level_manager.play_level_sound()
    
    def render_game(self):
        self.init_layers_to_render()
        render_manager.render(screen, self.state)  # Pass the current game state
        pg.display.update()

    def init_layers_to_render(self):
        render_manager.layers = []
        # Add a background layer (visible in all states)
        render_manager.add_layer(
            lambda screen: display.render(),
            z_index=0
        )
        # Add the next LEVEL indicator (displays the 'LEVEL <1>' text at start of each new level)
        render_manager.add_layer(
            lambda screen: display.render_new_level(self.current_level, self.level_manager.display_new_level, self.level_manager.get_level_color_counter()),
            z_index=1,
            states=["playing", "paused"]
        )
        # Add a game objects layer (only in 'playing' state)
        render_manager.add_layer(
            lambda screen: object_manager.render_objects(screen),
            z_index=2,
            # states=["playing"]
        )
        # Add an animation layer (only in 'playing' state)
        render_manager.add_layer(
            lambda screen: animation_manager.render_animations(screen),
            z_index=3,
            # states=["playing"]
        )
        # Add a HUD layer (only in 'playing' state)
        render_manager.add_layer(
            lambda screen: display.render_hud(self.points, self.lives),
            z_index=4,
            states=["playing", "paused"]
        )
        usship = object_manager.get_user_spaceship()
        # Add a menu layer (only in 'menu' state)
        render_manager.add_layer(
            lambda screen: display.render_title_screen(
                self.get_high_score('points'), 
                self.get_high_score('level')),
            z_index=4,
            states=["title_menu"]
        )
        # Add a paused layer (only in 'paused' state)
        render_manager.add_layer(
            lambda screen: display.render_paused(),
            z_index=4,
            states=["paused"]
        )
        sship = object_manager.get_user_spaceship()
        render_manager.add_layer(
            lambda screen: display.render_game_over(
                sship.delay_game_over_display,
                self.points
                ),
            z_index=4,
            states=["game_over"]
        ) # where to handle exiting this phase if timer runs out?
        render_manager.add_layer(
            lambda screen: display.render_game_over_menu(
                self.points,
                self.current_level,
                self.get_high_score('points'), 
                self.get_high_score('level'),
            ), 
            z_index=4,
            states=["game_over_menu"]
        )
        render_manager.add_layer(
            lambda screen: display.render_new_high_score(
                self.points,
                self.current_level,
                self.initials
            ),
            z_index=4,
            states=["new_high_score"]
        )
    
    def is_high_score(self):
        b = high_scores_manager.is_high_score(self.points, 'points') or high_scores_manager.is_high_score(self.current_level, 'level')
        return b
    

    def start_game(self):
        """
        Start a new game by resetting the score and lives, and setting the state to 'playing'.
        and initialize game-specific objects and start the game.
        """
        self.state = "playing"
        self.lives = self.max_lives
        self.points = 0
        print("Game started.")
        object_manager.wipe_obj_lists()
        object_manager.add_object(UserSpaceship(
            self.x_scrnsize/2, 
            self.y_scrnsize/2, 
            20, 
            0, 
            0, 
            WHITE, 
            screen, 
            sound_manager
        ))
        for _ in range(self.max_lives-1):
            DisplaySpaceshipLives.add_life(screen)
        sship = object_manager.get_user_spaceship()
        sship.lost_all_lives = False
        sship.invulnerable = True
        self.level_manager = LevelManager(asset_manager)
        sship.invulnerable_time_manager = TimeManager(INVULNERABLE_TIME) # add it back cause instantiating the level_manager wipes all the instances from TimeManager

    def pause_game(self):
        """
        Pause the game if it's currently playing.
        """
        if self.state == "playing": # redundant check
            self.state = "paused"
            TimeManager.toggle_pause()
            print("Game paused.")

    def resume_game(self):
        """
        Resume the game if it's currently paused.
        """
        if self.state == "paused":
            self.state = "playing"
            TimeManager.toggle_pause()
            print("Game resumed.")

    def end_game(self):
        """
        End the game, transitioning to the 'game_over' state.
        """
        self.state = "game_over"
        object_manager.get_user_spaceship().lost_all_lives = True
        print(f"Game over. Final score: { self.points}")
        # Add score to high scores if it's high enough
        # high_scores_manager.add_score("Player", self.points, self.current_level)

    def reset_game(self):
        self.end_game()
        TimeManager.paused = False
        DisplaySpaceshipLives.wipe_lives()
        self.lives = 0
        self.state = "title_menu"
        
    def lose_life(self):
        """
        Decrease the player's lives by one and check for game over.
        """
        self.lives -= 1
        print(f"Lives remaining: {self.lives}")
        DisplaySpaceshipLives.remove_life() # only want to remove a life after the sship death animation completes and the sship respawns
        # 2 ways: either don't call lose_life until death animation complete, or detect when death animation complete and call remove_life then. 
        # problem with second way: couldn't just call lose_life once, would need to be checking every time
        # problem with first way: if call lose life after delay, does the delay_game_over timer get messed up? maybe it simplifies it
        # quick fix: just add another life while sship is destroying
        self.allow_lose_life = False
        if self.lives <= 0:
            # object_manager.get_user_spaceship().delay_game_over_display = True
            self.end_game()

    def lose_life_after_destruction(self):
        if self.allow_lose_life:
            if self.lives == 1 or not object_manager.get_user_spaceship().is_destroying: # for last life, forget about the delay
                self.lose_life()
                
            
    def add_score(self, points):
        """
        Add points to the player's score.

        Args:
            points (int): The number of points to add.
        """
        self.points += points
        # print(f"Score updated: {self.points}")

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