import pygame as pg
from math import cos, sin, pi, sqrt, asin, atan
from entities import SpaceEntity
from utils import WHITE, BLACK, ACCELERATION, DEG2RAD, RAD2DEG, ROTATE, X_SCRNSIZE, Y_SCRNSIZE, DECELERATION, is_key_pressed, UserSpaceshipPolygon, flicker, RocketPolygon, FLICKER_ROCKET_DURATION, FLICKER_INVULNERABLE_DURATION, INVULNERABLE_TIME, TimeManager

class Spaceship(SpaceEntity):
    def __init__(self, x, y, size, speed, direction, color, screen, sound_manager, width=3, orientation=0):
        super().__init__(x, y, size, speed, direction, color)
        self.orientation = orientation
        self.polygon = UserSpaceshipPolygon(x, y, color, width, size, orientation)
        self.rocket_polygon = RocketPolygon(x, y, color, width, size, orientation)
        self.invulnerable = True
        self.rocket_color = WHITE
        self.screen = screen
        self.is_destroying = False
        self.delay_game_over_display = False
        self.lost_all_lives = True
        self.flicker_rocket = flicker(FLICKER_ROCKET_DURATION)
        self.flicker_invulnerable = flicker(FLICKER_INVULNERABLE_DURATION)
        self.sound_manager = sound_manager
        self.invulnerable_time_manager = TimeManager(INVULNERABLE_TIME)

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
    
    def synchronize_polygons(self, polygons: list[UserSpaceshipPolygon]):
        # TODO: potentially move this to utils and use for Asteroid too
        for polygon in polygons:
            # print(f"type(polygon) = {type(polygon)}, ({round(polygon.center_x, 2)}, {round(polygon.center_y, 2)}, {polygon.orientation}")
            polygon.center_x = self.x
            polygon.center_y = self.y
            polygon.orientation = self.orientation
            
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
        if not self.is_destroying and not self.invulnerable: # TODO: also disallow while invulnerable
            if self.flicker_rocket():
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
        if self.invulnerable:
            if self.invulnerable_time_manager.check_delta_time_elapsed():
                self.invulnerable = False
       
    
class UserSpaceship(Spaceship):
    def __init__(self, x, y, size, speed, direction, color, screen, sound_manager, width=3, orientation=0):
        super().__init__(x, y, size, speed, direction, color, screen, sound_manager, width=width, orientation=orientation)


class SpaceshipLives(Spaceship):
    
    pass
    def __init__(self, color, x, y, size, speed, direction, orientation):
        super().__init__(color, x, y, size, speed, direction, orientation)
        self.sship3_x = 140
        self.sship321_y = 60
        self.sship2_x = 100
        self.sship1_x = 60

        self.start_get_new_spaceship_x = 6/8
        self.end_get_new_spaceship_x = 7/8
        self.start_get_new_spaceship_y = 15/16
        self.end_get_new_spaceship_y = 1

        self.new_spaceship_distance3 = X_SCRNSIZE/2 - 140
        self.new_spaceship_distance2 = X_SCRNSIZE/2 - 100
        self.new_spaceship_distance1 = X_SCRNSIZE/2 - 60
        self.new_spaceship_counter = 0
        self.end_new_spaceship_counter = self.end_destroy_counter


    def get_new_spaceship3(self):
        
        #TIME THIS PROPERLY USING RATIOS
        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_x and self.new_spaceship_counter < self.end_new_spaceship_counter * self.end_get_new_spaceship_x:
            if self.x <= X_SCRNSIZE/2 - (X_SCRNSIZE/2 - self.sship3_x) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x)):
                self.x += (X_SCRNSIZE/2 - self.sship3_x) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x))
            else:
                self.x = X_SCRNSIZE/2

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_y:   
            self.x == X_SCRNSIZE/2
            self.y += (Y_SCRNSIZE/2 - self.sship321_y) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_y - self.start_get_new_spaceship_y))
                
        self.new_spaceship_counter += 1
            #self.destroy_counter
            #self.end_destroy_counter
        

    def get_new_spaceship2(self):
        

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_x and self.new_spaceship_counter < self.end_new_spaceship_counter * self.end_get_new_spaceship_x:
            if self.x <= X_SCRNSIZE/2 - (X_SCRNSIZE/2 - self.sship2_x) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x)):
                self.x += (X_SCRNSIZE/2 - self.sship2_x) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x))
            else:
                self.x = X_SCRNSIZE/2

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_y:   
            self.x == X_SCRNSIZE/2
            self.y += (Y_SCRNSIZE/2 - self.sship321_y) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_y - self.start_get_new_spaceship_y))
                
        self.new_spaceship_counter += 1

    
    def get_new_spaceship1(self):
        

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_x and self.new_spaceship_counter < self.end_new_spaceship_counter * self.end_get_new_spaceship_x:
            if self.x <= X_SCRNSIZE/2 - (X_SCRNSIZE/2 - self.sship1_x) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x)):
                self.x += (X_SCRNSIZE/2 - self.sship1_x) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_x - self.start_get_new_spaceship_x))
            else:
                self.x = X_SCRNSIZE/2

        if self.new_spaceship_counter >= self.end_new_spaceship_counter * self.start_get_new_spaceship_y:   
            self.x == X_SCRNSIZE/2
            self.y += (Y_SCRNSIZE/2 - self.sship321_y) / (self.end_new_spaceship_counter * (self.end_get_new_spaceship_y - self.start_get_new_spaceship_y))
                
        if self.paused_true == 0:
            self.new_spaceship_counter += 1

    def revert_spaceship3(self):
        self.x = self.sship3_x
        self.y = self.sship321_y
        self.new_spaceship_counter = 0

    def revert_spaceship2(self):
        self.x = self.sship2_x
        self.y = self.sship321_y
        self.new_spaceship_counter = 0

    def revert_spaceship1(self):
        self.x = self.sship1_x
        self.y = self.sship321_y
        self.new_spaceship_counter = 0


# bullet_collection = BulletList()

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

    
    def display(self):
        
        #LEFT
        #1,2,3,4
        xL1 = self.x + (self.size * .9 * cos(pi / 180 * (350 + self.orientation - 90) ))
        yL1 = self.y + (self.size * .9 * sin(pi / 180 * (350 + self.orientation - 90) ))


        xL2 = self.x + (self.size * .6 * cos(pi / 180 * (360 - 45 + self.orientation - 90) ))
        yL2 = self.y + (self.size * .6 * sin(pi / 180 * (360 - 45 + self.orientation - 90) ))

        xL3 = self.x + (self.size * 1 * cos(pi / 180 * (270 + self.orientation - 90) ))
        yL3 = self.y + (self.size * 1 * sin(pi / 180 * (270 + self.orientation - 90) ))

        xL4 = self.x + (self.size * .8 * cos(pi / 180 * (225 + self.orientation - 90) ))
        yL4 = self.y + (self.size * .8 * sin(pi / 180 * (225 + self.orientation - 90) ))

        #RIGHT
        xR1 = self.x + (self.size * .9 * cos(pi / 180 * (10 + self.orientation - 90) ))
        yR1 = self.y + (self.size * .9 * sin(pi / 180 * (10 + self.orientation - 90) ))


        xR2 = self.x + (self.size * .6 * cos(pi / 180 * (45 + self.orientation - 90) ))
        yR2 = self.y + (self.size * .6 * sin(pi / 180 * (45 + self.orientation - 90) ))

        xR3 = self.x + (self.size * 1 * cos(pi / 180 * (90 + self.orientation - 90) ))
        yR3 = self.y + (self.size * 1 * sin(pi / 180 * (90 + self.orientation - 90) ))

        xR4 = self.x + (self.size * .8 * cos(pi / 180 * (135 + self.orientation - 90) ))
        yR4 = self.y + (self.size * .8 * sin(pi / 180 * (135 + self.orientation - 90) ))

        pg.draw.polygon(SCREEN, self.color, [(xL1,yL1), (xL2,yL2), (xR2,yR2), (xL2,yL2), (xL3,yL3), (xR3,yR3), (xL3,yL3), (xL4,yL4), (xR4,yR4), (xR3,yR3), (xR2,yR2), (xR1,yR1)], self.width)




    def move(self):
        self.x = self.x + (self.speed * cos(pi / 180 * (self.direction - 90) ))
        self.y = self.y + (self.speed * sin(pi / 180 * (self.direction - 90) ))    

    def generate_random(self):
        random_num = random.randrange(1, 3, 1)
        #random_size = random.randrange(10,50,20)
        
        #self.speed = 10
        #random_size = random.randrange(30, 50, 5)

        
        
        if random_num == 1: 
            self.color = (255, round(self.color_change), round(self.color_change))
            self.x = X_SCRNSIZE + 40
            self.y = random.randrange(1, Y_SCRNSIZE, 1)
            #self.size = random_size
            #self.direction = random.randrange(180, 360,1)
            self.direction = 270
 
        
        if random_num == 2: 
            self.color = (255, round(self.color_change), round(self.color_change))
            self.x = -40
            self.y = random.randrange(1, Y_SCRNSIZE, 1)
            #self.size = random_size
            #self.direction = random.randrange(0, 180,1)
            self.direction = 90
            

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


