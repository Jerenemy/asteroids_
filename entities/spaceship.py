import pygame as pg
from math import cos, sin, pi, sqrt, asin, atan
from entities import SpaceEntity
from random import randrange, choice
from utils import WHITE, BLACK, ACCELERATION, DEG2RAD, RAD2DEG, ROTATE, X_SCRNSIZE, Y_SCRNSIZE, DECELERATION, is_key_pressed, UserSpaceshipPolygon, flicker, RocketPolygon, FLICKER_ROCKET_DURATION, FLICKER_INVULNERABLE_DURATION, INVULNERABLE_TIME, TimeManager, EnemySpaceshipPolygon, Polygon, flipcoin, BIG_ENEMY_SSHIP_SIZE, BIG_ENEMY_SSHIP_SPEED, SMALL_ENEMY_SSHIP_SIZE, SMALL_ENEMY_SSHIP_SPEED, CHANGE_DIRECTION_ENEMY_SSHIP_CHANCE


class Spaceship(SpaceEntity):
    def __init__(self, x, y, size, speed, direction, color, width, polygon, screen, sound_manager):
        super().__init__(x, y, size, speed, direction, color)
        self.width = width
        self.polygon = polygon
        self.screen = screen
        self.sound_manager = sound_manager        

    @property
    def x_scrnsize(self):
        try:
            return pg.display.get_window_size()[0]
        except pg.error as e:
            return X_SCRNSIZE
        
    @property
    def y_scrnsize(self):
        try:
            return pg.display.get_window_size()[1]
        except pg.error as e:
            return Y_SCRNSIZE
    
    def synchronize_polygons(self, polygons: list[Polygon]):
        # TODO: potentially move this to utils and use for Asteroid too
        for polygon in polygons:
            # print(f"type(polygon) = {type(polygon)}, ({round(polygon.center_x, 2)}, {round(polygon.center_y, 2)}, {polygon.orientation}")
            polygon.center_x = self.x
            polygon.center_y = self.y
            if hasattr(polygon, 'orientation'):
                polygon.orientation = self.orientation
       
    
class UserSpaceship(Spaceship):
    def __init__(self, x, y, size, speed, direction, color, screen, sound_manager, width=3, orientation=0):
        polygon = UserSpaceshipPolygon(x, y, color, width, size, orientation)
        super().__init__(x, y, size, speed, direction, color, width, polygon, screen, sound_manager)
        self.orientation = orientation
        self.rocket_polygon = RocketPolygon(x, y, color, width, size, orientation)
        self.invulnerable = True
        self.rocket_color = WHITE
        self.is_destroying = False
        self.delay_game_over_display = False
        self.lost_all_lives = True
        self.flicker_rocket = flicker(FLICKER_ROCKET_DURATION)
        self.flicker_invulnerable = flicker(FLICKER_INVULNERABLE_DURATION)
        self.invulnerable_time_manager = TimeManager(INVULNERABLE_TIME)
        
    def should_despawn(self):
        return False
    
    def accelerate(self):
        a = ACCELERATION
        c = self.speed
        B = 180 - (self.orientation - self.direction)
        new_speed = sqrt((a ** 2) + (c ** 2) - (2 * a * c * cos(B * DEG2RAD)))
        #account for division by zero error
        #maybe fixed by using law of sines with angle on bottom, maybe not though
        if new_speed != 0:
            new_direction_radians = asin((a * sin(B*DEG2RAD)) / new_speed)
            new_direction = new_direction_radians * RAD2DEG + self.direction
            # cycle direction when above 360
            if new_direction >= 360:
                new_direction = new_direction - 360
            elif new_direction <= 0:
                new_direction = new_direction + 360 
            self.direction = new_direction
        else: 
            self.speed = 0
        self.speed = new_speed
            
    def decelerate(self):
        if self.speed > DECELERATION:  
            self.speed = self.speed - DECELERATION
        else:
            self.speed = 0


    def move(self): 
        self.x = self.x + (self.speed * cos(pi / 180 * (self.direction - 90) ))
        self.y = self.y + (self.speed * sin(pi / 180 * (self.direction - 90) ))
        if not self.is_destroying:
            if is_key_pressed(pg.K_UP):
                # self.render_rocket(self.screen) # instead render rocket in self.render
                self.accelerate()
                self.sound_manager.play_event_sound('rocket') # play rocket sound here
            else:
                self.decelerate()
            if is_key_pressed(pg.K_LEFT):
                if self.orientation < ROTATE:
                    self.orientation = self.orientation + 360 - ROTATE
                else:
                    self.orientation = self.orientation - ROTATE
            if is_key_pressed(pg.K_RIGHT):
                if self.orientation > 360 - ROTATE:
                    self.orientation = self.orientation - 360 + ROTATE
                else:
                    self.orientation = self.orientation + ROTATE
        if self.x < 0: self.x = self.x + self.x_scrnsize
        if self.x > self.x_scrnsize: self.x = self.x - self.x_scrnsize
        if self.y < 0: self.y = self.y + self.y_scrnsize
        if self.y > self.y_scrnsize: self.y = self.y - self.y_scrnsize
        # synchronize updated coords and orientation with sship's polygon
        self.synchronize_polygons([self.polygon, self.rocket_polygon])
    
    
            
    def render(self, screen):
        if not self.is_destroying and not self.lost_all_lives:
            if is_key_pressed(pg.K_UP):
                self.render_rocket(self.screen) 
            if not TimeManager.paused and self.invulnerable:
                if not self.flicker_invulnerable():
                    self.polygon.render(screen)
            else:
                self.polygon.render(screen)
            self.check_invulnerable_status()
        
    def render_rocket(self, screen):
        if not self.invulnerable and self.flicker_rocket():
            self.rocket_polygon.render(screen)
            # need to have easier way to upgrade all of polygon's coords w/ spaceship. in sship.move, needs to automatically do this, here I just add it to a list of all features of the sship.

    
    def destroy(self):
        if not self.is_destroying:
            self.x = self.x_scrnsize/2
            self.polygon.center_x = self.x_scrnsize/2
            self.y = self.y_scrnsize/2
            self.polygon.center_y = self.y_scrnsize/2
            self.speed = 0
            self.orientation = 0
            self.polygon.orientation = 0
            self.invulnerable = True
            TimeManager.instances.remove(self.invulnerable_time_manager) # remove to avoid overhead by adding too many TimeManager instances
            self.invulnerable_time_manager = TimeManager(INVULNERABLE_TIME)     
                
    def check_invulnerable_status(self):
        if self.invulnerable and self.invulnerable_time_manager.check_delta_time_elapsed():
            self.invulnerable = False




class EnemySpaceship(Spaceship):
    def __init__(self, x, y, size, speed, direction, color, screen, sound_manager, width=3, points=200):
        polygon = EnemySpaceshipPolygon(x, y, color, width, size)
        super().__init__(x, y, size, speed, direction, color, width, polygon, screen, sound_manager)
        self.points = points if size<30 else points//2
        
    def render(self, screen):
        self.polygon.render(screen)
        
    def move(self):
        if EnemySpaceship.chance_to_trigger(chance=CHANGE_DIRECTION_ENEMY_SSHIP_CHANCE):
            if flipcoin():
                self.direction += 45
            else:
                self.direction -=45
        self.x = self.x + (self.speed * cos(pi / 180 * (self.direction - 90) ))
        self.y = self.y + (self.speed * sin(pi / 180 * (self.direction - 90) ))    
        self.synchronize_polygons([self.polygon])

    @staticmethod
    def generate_random():
        (size, speed) = (BIG_ENEMY_SSHIP_SIZE, BIG_ENEMY_SSHIP_SPEED) if flipcoin() else (SMALL_ENEMY_SSHIP_SIZE, SMALL_ENEMY_SSHIP_SPEED)
        random_num = randrange(1, 3, 1)
        #random_size = random.randrange(10,50,20)
        #self.speed = 10
        #random_size = random.randrange(30, 50, 5)
        if random_num == 1: 
            # color = (255, round(color_change), round(color_change))
            x = (SpaceEntity.x_scrnsize() + size)
            y = randrange(1, SpaceEntity.y_scrnsize() + size, 1)
            #size = random_size
            #direction = random.randrange(180, 360,1)
            direction = 270
        if random_num == 2: 
            # color = (255, round(color_change), round(color_change))
            x = - size
            y = randrange(1, SpaceEntity.y_scrnsize() + size, 1)
            #size = random_size
            #direction = random.randrange(0, 180,1)
            direction = 90
        color = (255, 0, 0)
        # print('size, speed', size, speed)
        return (color, x, y, size, speed, direction)
    
    def should_despawn(self):
        return self.is_out_of_bounds
    
    @staticmethod
    def chance_to_trigger(level=None, chance=1000):
        '''
        chance that enemy spaceship will fire a bullet depending on level.
        '''
        calcd_chance = int(chance / level) if level else chance
        fire_trigger = randrange(1, calcd_chance, 1)
        if fire_trigger == 1:
            return True # TODO: implement
        return False
        
   
# CLASS SpaceshipAutomated ******************************************************************************************************    
class SpaceshipAutomated(Spaceship):
    def __init__(self, color, x, y, size, speed, direction, orientation):
        super().__init__(color, x, y, size, speed, direction, orientation)

        
        
        #self.color_change = bullet_collection.bullet_accuracy / (24/17)
        self.color_change = 0
        self.color = (255, self.color_change, self.color_change)
        self.width = 3
        self.destroy_spaceship = 0
        
        
        
        
        self.score = 0
        self.game_over_true = 0
        self.high_score = 0
        self.start_game = 0
        self.restart_tick_time = 0

        self.automated = 1
        
        self.points = 500


        #super().__init__()"""

    
   



    def move(self):
        self.x = self.x + (self.speed * cos(pi / 180 * (self.direction - 90) ))
        self.y = self.y + (self.speed * sin(pi / 180 * (self.direction - 90) ))    

    @staticmethod
    def x_scrnsize():
        try:
            return pg.display.get_window_size()[0]
        except pg.error as e:
            return X_SCRNSIZE
        
    @staticmethod
    def y_scrnsize():
        try:
            return pg.display.get_window_size()[1]
        except pg.error as e:
            return X_SCRNSIZE
        

    @staticmethod
    def generate_random():
        random_num = randrange(1, 3, 1)
        #random_size = random.randrange(10,50,20)
        
        #self.speed = 10
        #random_size = random.randrange(30, 50, 5)

        
        
        if random_num == 1: 
            # color = (255, round(color_change), round(color_change))
            x = X_SCRNSIZE + 40
            y = randrange(1, Y_SCRNSIZE, 1)
            #size = random_size
            #direction = random.randrange(180, 360,1)
            direction = 270
 
        
        if random_num == 2: 
            # color = (255, round(color_change), round(color_change))
            x = -40
            y = randrange(1, Y_SCRNSIZE, 1)
            #size = random_size
            #direction = random.randrange(0, 180,1)
            direction = 90
        color = (255, 0, 0)
        return (color, x, y, direction)
            

class SpaceshipAutomatedList( list ):
    def __init__(self):
        self.spaceship_auto_destroy_sound_play = 0
        self.change_direction_amount = 0
        self.random_direction_amount = 0

    #Method change spaceships direction in Class SpaceshipAutomatedList:
    def change_directions(self, manned_sship):       
        i = 0
        
        while i < len(self):   
            """if self.change_direction_amount != 0:
                self.random_direction_amount = random.randrange(round(-self.change_direction_amount),round(self.change_direction_amount),1)
            else:
                self.random_direction_amount = 0
            """

            xx = manned_sship.x - self[i].x
            yy = manned_sship.y - self[i].y

            if xx < 0:
                self.change_direction_amount = (atan(yy/xx) - 90 * DEG2RAD) * RAD2DEG
            if xx > 0:
                self.change_direction_amount = (atan(yy/xx) + 90 * DEG2RAD) * RAD2DEG
            if xx == 0:
                if yy >= 0: 
                    self.change_direction_amount = 180
                if yy < 0:
                    self.change_direction_amount = 0

            self.change_direction_amount = self.change_direction_amount + self.random_direction_amount
            #self[i].direction = self[i].direction - self.change_direction_amount
            self[i].direction = self.change_direction_amount

            i = i + 1

    #Method move_asteroids in Class SpaceshipAutomatedList:
    def move_spaceships(self):       
        i = 0
        while i < len(self):   
            self[i].move()
            if self[i].x < (0 - self[i].size) or self[i].x > (X_SCRNSIZE + self[i].size) or self[i].y < (0 - self[i].size) or  self[i].y > (Y_SCRNSIZE + self[i].size): 
                self.pop(i)            
            i = i + 1

    #Method check_spaceships in Class SpaceshipAutomatedList:
    def check_if_spaceships_hit(self, bullet_list):       
        i = 0
        while i < len(self):   
            hit = self[i].check_distance(bullet_list)
            self[i].hit = hit
            i = i + 1
            

    #Method display_spaceships in Class SpaceshipAutomatedList:
    def display_spaceships(self):        
        i = 0
        while i < len(self):   
            self[i].display()
            i = i + 1


    def delete_hit_spaceships(self):       
        i = 0
        while i < len(self):   
            if self[i].hit == 1:
                #bang_sship_auto_destroy.play()
                self.spaceship_auto_destroy_sound_play = 1
                self.pop(i)            
            i = i + 1


