from entities import SpaceEntity, Asteroid, Spaceship, UserSpaceship, Bullet
from .time_manager import TimeManager
# from utils import choose_color, WHITE, X_SCRNSIZE, Y_SCRNSIZE
from random import randint
from utils import get_list_item_by_type


class ObjectManager:
    def __init__(self):
        self.objects = {
            "asteroids": [],
            "bullets": [],
            "spaceships": []
        }
        self.type_mapping = {
            Asteroid: "asteroids",
            Bullet: "bullets",
            Spaceship: "spaceships",
            UserSpaceship: "spaceships"
        }
        self.collision_pairs = [
            ("bullets", "asteroids"),
            ("spaceships", "asteroids")
        ]
    
    def get_user_spaceship(self):
        return get_list_item_by_type(self.objects["spaceships"], UserSpaceship) # TODO: have friendly and enemy spaceships stored in sub-dictionary, 
    
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
        if isinstance(obj1, Bullet) and isinstance(obj2, Asteroid):
            self.remove_object(obj1)
            self.remove_object(obj2)
            ast1, ast2 = obj2.split()
            if ast1 and ast2:
                self.add_object(ast1)
                self.add_object(ast2)
            return {
                'type': 'bullet_hit_asteroid',
                'x': obj2.x,
                'y': obj2.y,
                'size': obj2.size,
                'points': obj2.points,
                'duration': 30  # Example duration
            }
        elif isinstance(obj1, Spaceship) and isinstance(obj2, Asteroid):
            # obj1.destroy()
            if not obj1.is_destroying:
                self.remove_object(obj2)
                if isinstance(obj1, UserSpaceship):
                    return {
                        'type': 'user_spaceship_hit', 
                        'spaceship': obj1, 
                        'asteroid': obj2
                    }
            # elif isinstance(obj1, EnemySpaceship):
        return None  # No significant event
