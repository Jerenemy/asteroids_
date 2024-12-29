from abc import ABC, abstractmethod
import pygame as pg
from utils.constants import BLACK, WHITE, X_SCRNSIZE, Y_SCRNSIZE
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
        # for element_group in self.elements:
        #     for element in element_group:
        #         element.render(self.screen)

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
        self.add_score_element(score)
        self.add_lives_element(lives)
        
    def render_hud(self, score: int, lives: int):
        self.init_hud_elements(score, lives)
        for element in self.hud_elements:
            element.render(self.screen)
        
        
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
    def __init_subclass__(cls):
        return super().__init_subclass__()


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
