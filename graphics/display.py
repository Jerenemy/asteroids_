from abc import ABC, abstractmethod
import pygame as pg
from utils import BLACK, WHITE, X_SCRNSIZE, Y_SCRNSIZE, translate_to_ratio
import re
from utils import UserSpaceshipPolygon, SPACESHIP_STARTING_LIVES


class DisplayElement(ABC):
    """Abstract base class for all display elements."""

    @abstractmethod
    def render(self, screen):
        """Render the element on the screen."""
        pass
    
    @staticmethod
    def x_scrnsize() -> int:
        try:
            x, _ = pg.display.get_window_size()
            return int(x)
        except Exception as e:
            return X_SCRNSIZE
    
    @staticmethod
    def y_scrnsize() -> int:
        try:
            _, y = pg.display.get_window_size()
            return int(y)
        except Exception as e:
            return Y_SCRNSIZE
        
    @staticmethod
    def _center_position(rendered_text):
        return (
            DisplayElement.x_scrnsize() / 2 - rendered_text.get_width() / 2,
            DisplayElement.y_scrnsize() / 2 - rendered_text.get_height() / 2
        )
        
    @staticmethod
    def _upper_left_position():
        return (0, 0)
        
    @staticmethod
    def _upper_right_position(rendered_text):
        return (
            DisplayElement.x_scrnsize() - rendered_text.get_width(),
            0
        )
     
    @staticmethod   
    def _lower_left_position(rendered_text):
        return (
            0,
            DisplayElement.y_scrnsize() - rendered_text.get_height()
        )
        
    @staticmethod
    def _lower_right_position(rendered_text):
        return (
            DisplayElement.x_scrnsize() - rendered_text.get_width(),
            DisplayElement.y_scrnsize() - rendered_text.get_height()
        )

    @staticmethod
    def _default_position(position_type: str, rendered_text):
        if position_type == "center":
            return DisplayElement._center_position(rendered_text)
        elif position_type == "upper_left":
            return DisplayElement._upper_left_position()
        elif position_type == "lower_left":
            return DisplayElement._lower_left_position(rendered_text)
        elif position_type == "upper_right":
            return DisplayElement._upper_right_position(rendered_text)
        elif position_type == "lower_right":
            return DisplayElement._lower_right_position(rendered_text)
    
    @staticmethod
    def parse_position(position, offset, rendered_text):
        """
        Parses a position string and calculates the position.
        Supports 'center' with optional offsets in the format: "center:(+x,+y)".
        """
        if not isinstance(position, str):
            # if isinstance(position, Tuple):
            if position is None:
                return offset
            else:
                raise ValueError("Position must be a string or None.")
        if  re.match(r"center|upper_left|upper_right|lower_left|lower_right", position):
            # Extract offsets
            delta_x, delta_y = offset
            # Calculate position with offsets
            default_position_x, default_position_y = DisplayElement._default_position(position, rendered_text)
            parsed_position = (default_position_x + delta_x, default_position_y + delta_y)
        else:
            raise ValueError(f"Invalid position format: {position}")
        return parsed_position

class Display:
    def __init__(self, screen, asset_manager):
        self.screen = screen
        self.asset_manager = asset_manager
        self.color = BLACK
        self.caption = "Asteroids"
        self.title_elements = []
        self.hud_elements = []
        self.elements = []  # Holds all DisplayElement instances
        self.title_elements_added = False  # Track if title elements are added
        self.last_displayed_score = 0

    def add_element(self, element):
        """Add a new display element."""
        if isinstance(element, DisplayElement):
            self.elements.append(element)
        else:
            raise TypeError("Element must be a subclass of DisplayElement.")

    def craft_element(
            self, 
            value, 
            font_size: int, 
            generic_placement: str, 
            coords: tuple, 
            font_name='keyboard', 
            custom_font_path=None,
            color=WHITE
        ):
        coords = (translate_to_ratio(coords[0]), translate_to_ratio(coords[1]))
        font_obj = self.get_font(font_name, translate_to_ratio(font_size), custom_font_path=custom_font_path)
        disp_el = DisplayText(
            str(value),
            font_obj,
            color, 
            generic_placement,
            coords
        )
        return disp_el
    
    def render(self):
        """Render the display and all elements."""
        self.screen.fill(self.color)
        pg.display.set_caption(self.caption)
        
    def get_font(self, font_name: str, size: int, custom_font_path=None):
        font = self.asset_manager.get_font(font_name, size)
        if font:
            return font
        self.asset_manager.load_font(font_name, custom_font_path, size)
        return self.asset_manager.get_font(font_name, size)
       
    def render_game_over(self, is_destroying: bool, delay: bool, score: int, lives: int, points_high_score: int, level_high_score: int):
        game_over_elements_list = self.game_over_elements(is_destroying, delay, score, lives, points_high_score, level_high_score)
        for element in game_over_elements_list:
            element.render(self.screen)
    
    def score_high_score_elements(self, points: int, level: int, points_high_score_tup: tuple, level_high_score_tup: tuple) -> list:
        # print(points_high_score_tup, 'brea', level_high_score_tup)
        points_name, points_high_score = points_high_score_tup
        level_name, level_high_score = level_high_score_tup
        element_size = 50
        game_over_hud = [
            self.craft_element(points, element_size, 'upper_right', (-10, 10)),
            self.craft_element(level, element_size, 'upper_left', (10, 10))
        ]
        high_score_text_height = -Y_SCRNSIZE/2+40
        high_score_text_size = 15
        points_level_text_height = high_score_text_height + translate_to_ratio(high_score_text_size+7)
        high_score_size = 30
        high_score_height = points_level_text_height + translate_to_ratio(high_score_size)
        initials_text_size = translate_to_ratio(high_score_size/2)
        initials_text_height = high_score_height + initials_text_size + translate_to_ratio(8)
        stats = [
            self.craft_element("HIGH SCORE", 20, "center", (0, high_score_text_height)),
            self.craft_element("LEVEL", high_score_text_size, "center", (-50, points_level_text_height)),
            self.craft_element("POINTS", high_score_text_size, "center", (50, points_level_text_height)),
            self.craft_element(level_high_score, high_score_size, 'center', (-45, high_score_height)),
            self.craft_element(points_high_score, high_score_size, 'center', (45, high_score_height)),
            self.craft_element(points_name, initials_text_size, 'center', ((-45, initials_text_height))),
            self.craft_element(level_name, initials_text_size, 'center', ((45, initials_text_height)))
        ]
        return game_over_hud + stats 

    def game_over_elements(self, is_destroying: bool, delay: bool, points: int, level: int, points_high_score_tup: tuple, level_high_score_tup: tuple) -> list: 
        if not delay:
            element_size = 50
            game_over_text = [
                self.craft_element('GAME OVER', 100, 'center', (0, -10))
            ]
            game_over_hud = [self.craft_element(points, element_size, 'upper_right', (-10, 10))]
            if not is_destroying:
                game_over_hud = self.score_high_score_elements(points, level, points_high_score_tup, level_high_score_tup)
                game_over_text.append(self.craft_element('CLICK TO PLAY', 30, 'center', (0, 65)))
        else:
            game_over_text = []
            game_over_hud = []
        return game_over_text + game_over_hud
            
    def set_title_elements(self, points_high_score_tup: tuple, level_high_score_tup: tuple, points=0, level=1):
        self.title_elements = [
            self.craft_element('ASTEROIDS', (150), 'center', (0, -40)),
            self.craft_element('Lucas Wiedmann', (50), 'center', (0, (DisplayElement.y_scrnsize()/2)-translate_to_ratio(120)), font_name='signature', custom_font_path='signature.otf'),
            self.craft_element('CLICK TO PLAY', (30), 'center', (0, 65)),
            # self.craft_element('Named best game of all time by Obama', (40), 'lower_left', (50,-50), font_name='minecraft', custom_font_path='minecraft_font.ttf')
        ]
        self.title_elements += self.score_high_score_elements(points, level, points_high_score_tup, level_high_score_tup)
        
    def render_title_screen(self, points_high_score_tup: tuple, level_high_score_tup: tuple):
        self.set_title_elements(points_high_score_tup, level_high_score_tup)
        for element in self.title_elements:
            element.render(self.screen)
        
    def init_hud_elements(self, score: int, lives: int):
        self.hud_elements = [
            self.craft_element(score, 45, 'upper_right', (-10, 10)),
            # self.craft_element(lives, 45, 'upper_left', (10, 10))
            DisplaySpaceshipLives
        ]
        
        
    def render_hud(self, score: int, lives: int):
        self.init_hud_elements(score, lives)
        for element in self.hud_elements:
            element.render(self.screen)
        
    def render_paused(self):
        pause_element = self.craft_element('P A U S E D', 40, 'center', (0, -X_SCRNSIZE/2+20))
        pause_element.render(self.screen)
        
    def clear_elements(self):
        """Remove all elements from the display."""
        self.elements = []

    def remove_elements_of_class(self, class_type):
        """Remove elements of a specific class type."""
        new_elements = []
        for el_group in self.elements:
            for el in el_group:
                if isinstance(el, class_type):
                    break
                else:
                    new_elements += [el_group]
                    break
        self.elements = new_elements        
        # self.elements = [el for el in self.elements if not isinstance(el, class_type)]

    def render_new_level(self, level: int, display_new_level: bool, color_counter: int):
        self.new_level_element = []
        if display_new_level:
            color = (
                255 - color_counter,
                255 - color_counter,
                255 - color_counter
            )
            self.new_level_element = [
                self.craft_element(f'LEVEL {level}', 150, 'center', (0,0), color=color)
            ]
        for element in self.new_level_element:
            element.render(self.screen)
        

class DisplayText(DisplayElement):
    def __init__(self, text: str, font, color: tuple, position, offset: tuple):
        super().__init__()
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.offset = offset
        
    def render(self, screen):
        rendered_text = self.font.render(self.text, True, self.color)
        screen.blit(rendered_text, DisplayElement.parse_position(self.position, self.offset, rendered_text))


class DisplayTitleText(DisplayText):
    def __init__(self, text, font, color, position, offset):
        super().__init__(text, font, color, position, offset)


class DebugValue(DisplayElement):
    def __init__(self, label, value, font_size, color, position):
        self.label = label
        self.value = value
        self.font_size = font_size
        self.color = color
        self.position = position

    def render(self, screen):
        font = pg.font.SysFont("arial", self.font_size)
        text = f"{self.label}: {self.value}"
        rendered_text = font.render(text, True, self.color)
        screen.blit(rendered_text, self.position)
        
class DisplaySpaceshipLives:
    lives = 0
    instances = []
    screen = None
    edge_offset = 40
    
    def __init__(self, lives=None, screen=None):
        self.instances.append(self)
        center_y = DisplaySpaceshipLives.edge_offset
        self.life_polygon = UserSpaceshipPolygon(self.center_x, center_y, WHITE, 3, 20, 0)
        if lives is not None: DisplaySpaceshipLives.lives = lives 
        if screen is not None: DisplaySpaceshipLives.screen = screen

    @property
    def center_x(self):
        return DisplaySpaceshipLives.edge_offset * (DisplaySpaceshipLives.instances.index(self) + 1) # account for zero index
     
    def render_instance(self, screen):
        self.life_polygon.render(screen)
        
    @classmethod
    def add_life(cls, screen):
        _ = cls(lives=(cls.lives+1))
        cls.screen = screen
    
    @classmethod
    def remove_life(cls):
        try:
            cls.instances.pop()
        except IndexError as e:
            pass
    
    @classmethod
    def render(cls, screen):
        # print(len(cls.instances))
        for instance in cls.instances:
            instance.render_instance(screen)
