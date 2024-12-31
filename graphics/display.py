from abc import ABC, abstractmethod
import pygame as pg
from utils import BLACK, WHITE, X_SCRNSIZE, Y_SCRNSIZE, translate_to_ratio
import re
from typing import Tuple


class DisplayElement(ABC):
    """Abstract base class for all display elements."""

    @abstractmethod
    def render(self, screen):
        """Render the element on the screen."""
        pass
    
    @staticmethod
    def _center_position(rendered_text):
        return (
            X_SCRNSIZE / 2 - rendered_text.get_width() / 2,
            Y_SCRNSIZE / 2 - rendered_text.get_height() / 2
        )
        
    @staticmethod
    def _upper_left_position():
        return (0, 0)
        
    @staticmethod
    def _upper_right_position(rendered_text):
        return (
            X_SCRNSIZE - rendered_text.get_width(),
            0
        )
        
    @staticmethod
    def _lower_left_position(rendered_text):
        return (
            0,
            Y_SCRNSIZE - rendered_text.get_height()
        )
        
    @staticmethod
    def _lower_right_position(rendered_text):
        return (
            X_SCRNSIZE - rendered_text.get_width(),
            Y_SCRNSIZE - rendered_text.get_height()
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
        self.init_title_elements()
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

    def init_title_elements(self):
        """Add title elements only"""
        title_font = self.get_font('keyboard', 150)
        title_disp_el = DisplayTitleText(
            'ASTEROIDS', 
            title_font, 
            WHITE, 
            "center",
            (0, -40)
        )
        self.title_elements.append(title_disp_el)
        signature_font = self.get_font('signature', 50, custom_font_path='signature.otf')
        signature_disp_el = DisplayTitleText(
            'Jeremy Zay', 
            signature_font,
            WHITE,
            "center",
            (0, 120)
        )
        self.title_elements.append(signature_disp_el)

    def render_title_screen(self):
        for element in self.title_elements:
            element.render(self.screen)
       
    def render_game_over(self, is_destroying, delay, score, lives, points_high_score, level_high_score):
        game_over_elements_list = self.game_over_elements(is_destroying, delay, score, lives, points_high_score, level_high_score)
        for element in game_over_elements_list:
            element.render(self.screen)
    

    def game_over_elements(self, is_destroying: bool, delay: bool, points: int, level: int, points_high_score: int, level_high_score: int) -> list: 
        if not delay:
            element_size = translate_to_ratio(50)
            game_over_text = [
                self.craft_element('GAME OVER', 'keyboard', translate_to_ratio(100), WHITE, 'center', (0, translate_to_ratio(-10)))
            ]
            game_over_hud = [self.craft_element(points, 'keyboard', element_size, WHITE, 'upper_right', (translate_to_ratio(-10), translate_to_ratio(10)))]
            if not is_destroying:
                game_over_hud.append(
                    self.craft_element(level, 'keyboard', element_size, WHITE, 'upper_left', (translate_to_ratio(10), translate_to_ratio(10)))
                )
                high_score_text_height = translate_to_ratio(-Y_SCRNSIZE/2+40)
                high_score_text_size = translate_to_ratio(15)
                points_level_text_height = high_score_text_height + translate_to_ratio(high_score_text_size+7) 
                high_score_size = translate_to_ratio(30)
                high_score_height = points_level_text_height + high_score_size
                stats = [
                    self.craft_element("HIGH SCORE", 'keyboard', translate_to_ratio(20), WHITE, "center", (0, high_score_text_height)),
                    self.craft_element("LEVEL", 'keyboard', high_score_text_size, WHITE, "center", (translate_to_ratio(-50), points_level_text_height)),
                    self.craft_element("POINTS", 'keyboard', high_score_text_size, WHITE, "center", (translate_to_ratio(50), points_level_text_height)),
                    self.craft_element(level_high_score, 'keyboard', high_score_size, WHITE, 'center', (translate_to_ratio(-45), high_score_height)),
                    self.craft_element(points_high_score, 'keyboard', high_score_size, WHITE, 'center', (translate_to_ratio(45), high_score_height))
                ]
                game_over_text.append(self.craft_element('CLICK TO PLAY', 'keyboard', translate_to_ratio(30), WHITE, 'center', (0, translate_to_ratio(65))))
            else: 
                stats = []
        else:
            game_over_text = []
            game_over_hud = []
            stats = []
        return game_over_text + game_over_hud + stats
            
        game_over_text = [
            self.craft_element("HIGH SCORE", 'keyboard', 20, WHITE, "center", (0, -40)),
            self.craft_element("LEVEL", 'keyboard', 15, WHITE, "center", (-50, 10)),
            self.craft_element("POINTS", 'keyboard', 15, WHITE, "center", (50, 10)),
            self.craft_element(str(level_high_score), 'keyboard', translate_to_ratio(30), WHITE, "center", (translate_to_ratio(-50), translate_to_ratio(50))),
            self.craft_element(str(points_high_score), 'keyboard', 30, WHITE, "center", (50, 50)),
            # self.craft_element(f"Score: {points}", 'keyboard', 20, WHITE, "center", (0, 100))
        ]
        
            
       
    def craft_element(
            self, value, font_name: str, font_size: int, 
            color: tuple, generic_placement: str, coords: tuple
            ):
        font_obj = self.get_font(font_name, font_size)
        disp_el = DisplayText(
            str(value),
            font_obj,
            color, 
            generic_placement,
            coords
        )
        return disp_el
            

        
    
    def add_lives_element(self, lives: int):
        # if lives != self.last_displayed_lives:
        lives_font = self.get_font('keyboard', 50)
        lives_disp_el = DisplayText(
            str(lives),
            lives_font,
            WHITE,
            'upper_left',
            (10, 10)
        )
        self.hud_elements.append(lives_disp_el)
        # self.last_displayed_lives = lives
    
    def add_score_element(self, score: int):
        # if score != self.last_displayed_score:
        self.hud_elements = []
        score_font = self.get_font('keyboard', 50)
        score_disp_el = DisplayText(
            str(score),
            score_font,
            WHITE,
            'upper_right',
            (-10, 10)
        )
        self.hud_elements.append(score_disp_el)
    
    def init_hud_elements(self, score: int, lives: int):
        self.hud_elements = [
            self.craft_element(score, 'keyboard', 50, WHITE, 'upper_right', (-10, 10)),
            self.craft_element(lives, 'keyboard', 50, WHITE, 'upper_left', (10, 10))
        ]
        
    
        
    def render_hud(self, score: int, lives: int):
        self.init_hud_elements(score, lives)
        for element in self.hud_elements:
            element.render(self.screen)
        
    # def display_render_game_over(self, score: int, level: int, high_score: int): #TODO: add level
    #     pass
        
        
    # ***** hud elements ***** #
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

        


class DisplayText(DisplayElement):
    def __init__(self, text: str, font, color: tuple, position, offset: tuple):
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

######################################
class GameOver:
    def game_over(self):
        WINNER_FONT = pg.font.SysFont('keyboard', 100)
        WINNER_TEXT = "GAME OVER"
        
        draw_text = WINNER_FONT.render(WINNER_TEXT, 1, WHITE)
        SCREEN.blit(draw_text, (X_SCRNSIZE/2 - draw_text.get_width() / 2, Y_SCRNSIZE/2 - draw_text.get_height() / 2 - 10))
    
    def restart(self, event):
        RESTART_FONT = pg.font.SysFont('keyboard', 30)
        RESTART_TEXT = "CLICK TO PLAY"
        draw_text1 = RESTART_FONT.render(RESTART_TEXT, 1, WHITE)
        SCREEN.blit(draw_text1, (X_SCRNSIZE/2 - draw_text1.get_width() / 2, Y_SCRNSIZE/2 - draw_text1.get_height()/2 + 65))
        
    
    def score_display(self):

        SCORE_FONT = pg.font.SysFont('keyboard', 50)

        score_text = SCORE_FONT.render( str(self.score), 1, WHITE)
        SCREEN.blit(score_text, ((X_SCRNSIZE - score_text.get_width() - 40), (score_text.get_height() - 30)))


    def display_high_score(self):
        
        if self.high_score < self.score:
            self.high_score = self.score
        HIGH_SCORE_FONT = pg.font.SysFont('keyboard', 20)
        HIGH_SCORE_FONT1 = pg.font.SysFont('keyboard', 30)

        HIGH_SCORE_TEXT1 = "HIGH SCORE" 
        HIGH_SCORE_TEXT2 = str(self.high_score)
        h1 = HIGH_SCORE_FONT.render(HIGH_SCORE_TEXT1, 1, WHITE)
        h2 = HIGH_SCORE_FONT1.render(HIGH_SCORE_TEXT2, 1, WHITE)
        SCREEN.blit(h1, ( X_SCRNSIZE/2 - h1.get_width()/2 , 40 + 0 ))
        SCREEN.blit(h2, ( X_SCRNSIZE/2 - h2.get_width()/2 , 40 + h1.get_height()))

    def display_high_score(self, high_score, score):
        """
        sig: int, int --> int
        displays high score (points and waves completed) during title screen and game over
        must pass sship.high_score and sship.score, must set function = sship.high_score
        """
        if high_score < score:
            high_score = score
            self.init_new_high_score = 1
        if self.max_waves_completed < self.waves_completed:
            self.max_waves_completed = self.waves_completed
        HIGH_SCORE_FONT = pygame.font.SysFont('keyboard', 20)
        HIGH_SCORE_FONT1 = pygame.font.SysFont('keyboard', 15)
        HIGH_SCORE_FONT2 = pygame.font.SysFont('keyboard', 30)


        HIGH_SCORE_TEXT = "HIGH SCORE" 
        HIGH_SCORE_TEXT1 = "LEVEL"
        HIGH_SCORE_TEXT1a = "POINTS"
        HIGH_SCORE_TEXT2 = str(self.max_waves_completed)
        HIGH_SCORE_TEXT2a = str(high_score)


        h = HIGH_SCORE_FONT.render(HIGH_SCORE_TEXT, 1, WHITE)
        h1 = HIGH_SCORE_FONT1.render(HIGH_SCORE_TEXT1, 1, WHITE)
        h1a = HIGH_SCORE_FONT1.render(HIGH_SCORE_TEXT1a, 1, WHITE)
        h2 = HIGH_SCORE_FONT2.render(HIGH_SCORE_TEXT2, 1, WHITE)
        h2a = HIGH_SCORE_FONT2.render(HIGH_SCORE_TEXT2a, 1, WHITE)

        gap = 30

        SCREEN.blit(h, ( X_SCRNSIZE/2 - h.get_width()/2 , 40 + 0 ))
        SCREEN.blit(h1, ( X_SCRNSIZE/2 - h1.get_width() - gap, 40 + h.get_height()))
        SCREEN.blit(h1a, ( X_SCRNSIZE/2 + gap, 40 + h.get_height()))
        SCREEN.blit(h2, ( X_SCRNSIZE/2 - h1.get_width()/2 - h2.get_width()/2 - gap, 40 + h.get_height() + h1.get_height()))
        SCREEN.blit(h2a, ( X_SCRNSIZE/2 + h1a.get_width()/2 - h2a.get_width()/2 + gap, 40 + h.get_height() + h1.get_height()))

        return high_score