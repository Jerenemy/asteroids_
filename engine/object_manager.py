from entities import Asteroid, Spaceship, UserSpaceship, UserBullet, EnemyBullet, Bullet, EnemySpaceship
from utils import get_list_item_by_type, BULLET_SIZE, AUTO_BULLET_SPEED, WHITE, get_direction_to
from random import choice


class ObjectManager:
    def __init__(self):
        self.objects = {
            "asteroids": [],
            "user_bullets": [],
            "enemy_bullets": [],
            "user_spaceship": [],
            "enemy_spaceships": []
        }
        self.type_mapping = {
            Asteroid: "asteroids",
            UserBullet: "user_bullets",
            EnemyBullet: "enemy_bullets",
            # Spaceship: "spaceships",
            UserSpaceship: "user_spaceship",
            EnemySpaceship: "enemy_spaceships"
        }
        self.collision_pairs = [
            ("user_spaceship", "asteroids"),
            ('user_spaceship', 'enemy_spaceships'),
            ('user_spaceship', 'enemy_bullets'),
            ('enemy_spaceships', 'asteroids'), 
            ('enemy_spaceships', 'user_bullets'),
            ('enemy_spaceships', 'enemy_bullets'),
            ("asteroids", "user_bullets"),
            ('asteroids', 'enemy_bullets')
        ]
    
    def get_user_spaceship(self):
        return get_list_item_by_type(self.objects["user_spaceship"], UserSpaceship) # TODO: have friendly and enemy spaceships stored in sub-dictionary, 
    
    def get_object_type_key(self, obj) -> str:
        """Get the object type key for a given object."""
        return self.type_mapping.get(type(obj), None)

    def get_object_list(self, obj) -> list:
        """Get the list corresponding to an object's type."""
        obj_type = self.get_object_type_key(obj)
        if obj_type:
            return self.objects[obj_type]
        return None
    
    def get_object_list2(self, object_list: str) -> list:
        return self.objects[object_list]

    def remove_object(self, obj):
        """Remove an object from its list."""
        obj_list = self.get_object_list(obj)
        if obj_list and obj in obj_list:
            obj_list.remove(obj)

    def wipe_obj_lists(self):
        for obj_type in self.objects.keys():
            self.objects[obj_type] = []

    def add_object(self, obj):
        self.get_object_list(obj).append(obj)

    def update_objects(self):
        """Update all space objects."""
        for obj_list in self.objects.values():
            for obj in obj_list[:]:
                obj.move()
                if obj.should_despawn():
                    self.remove_object(obj)

    def render_objects(self, screen):
        """Render all space objects."""
        for obj_list in self.objects.values():
            for obj in obj_list:
                obj.render(screen)

    def get_collision_events(self):
        collision_events = []
        """Check collisions based on predefined type pairs."""
        for type1, type2 in self.collision_pairs:
            for obj1 in self.objects[type1][:]:
                for obj2 in self.objects[type2][:]:
                    if obj1.check_collision(obj2):
                        event = self.handle_collision(obj1, obj2)
                        if event:
                            collision_events.append(event)
        return collision_events

    def handle_collision(self, obj1, obj2):
        """Handle logic for when objects collide."""
        if isinstance(obj1, UserSpaceship):
            return self.get_user_spaceship_collision_event(obj1, obj2)
        elif isinstance(obj1, EnemySpaceship):
            return self.get_enemy_spaceship_collision_event(obj1, obj2)
        elif isinstance(obj1, Asteroid):
            return self.get_asteroid_collision_event(obj1, obj2)
    
    
    def get_user_spaceship_collision_event(self, user_sship, obj2):
        if not user_sship.is_destroying and not user_sship.lost_all_lives and not user_sship.invulnerable:
            self.remove_object(obj2)
            if isinstance(obj2, Asteroid):
                self.split_asteroid(obj2)
            # elif isinstance(obj2, EnemySpaceship):
            # elif isinstance(obj2, EnemyBullet):
            return {
                    'type': 'user_spaceship_hit', 
                    'spaceship': user_sship, 
                    'collided_with': obj2
                }
        
    def get_enemy_spaceship_collision_event(self, enemy_sship, obj2):
        # TODO: add collisions with other enemy spaceships
        self.remove_object(enemy_sship)
        if not isinstance(obj2, UserSpaceship):
            self.remove_object(obj2)
        # if isinstance(obj2, UserBullet):
        #     return {
        #     'type': 'enemy_spaceship_hit_by_user',
        #     'spaceship': enemy_sship,
        #     'collided_with': obj2
        #     }
        if isinstance(obj2, Asteroid):
            self.split_asteroid(obj2)
        # elif isinstance(obj2, EnemyBullet):
        return {
            'type': 'enemy_spaceship_hit',
            'spaceship': enemy_sship,
            'collided_with': obj2
        }

    def get_asteroid_collision_event(self, ast, obj2):
        if isinstance(obj2, Bullet):
            self.split_asteroid(ast)
            self.remove_object(obj2)
            self.remove_object(ast)
            return {
                'type': 'bullet_hit_asteroid',
                'asteroid': ast,
                'collided_with': obj2
            }
            

    def split_asteroid(self, ast: Asteroid):
        # self.remove_object(ast)
        ast1, ast2 = ast.split()
        if ast1 and ast2:
            self.add_object(ast1)
            self.add_object(ast2)
           

    def fire_enemy_sship_bullets(self, level):
        enemy_sships = self.get_object_list2('enemy_spaceships')
        for enemy_sship in enemy_sships:
            # fire bullet every so often at nearby object
            nearest_target = self.get_nearest_target(enemy_sship.x, enemy_sship.y)
            user_target = self.get_user_spaceship()
            target = choice([nearest_target, user_target]) if nearest_target else user_target
            # target = nearest_target
            dir = get_direction_to(enemy_sship, target)
            if EnemySpaceship.chance_to_trigger(level):
                x, y, direction, sship_speed = Bullet.get_bullet_launch_attributes(enemy_sship.x, enemy_sship.y, enemy_sship.size+10, dir, enemy_sship.speed)
                blt = EnemyBullet(x, y, BULLET_SIZE, AUTO_BULLET_SPEED, direction, WHITE, lifetime=200)
                self.add_object(blt)
            
    
    def get_nearest_target(self, x, y):
        asts = self.get_object_list2('asteroids')
        min_x = float('inf')
        min_y = float('inf')
        nearest_target = None
        for ast in asts:
            if abs(x - ast.x) + abs(y-ast.y) < min_x + min_y :
                min_x = ast.x
                min_y = ast.y
                nearest_target = ast
        return nearest_target