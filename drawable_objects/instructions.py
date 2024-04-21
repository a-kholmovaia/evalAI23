import pygame
from drawable_objects.drawable_object import DrawableObject
from window import Window
import constants

class Instructions(DrawableObject):

    def __init__(self, scene_path: str, window: Window, font: pygame.font.Font):
        super().__init__(window, 0, 0, 280, 140)
        self.window = window
        self.font = font
        self.scene_path = scene_path
        self.text_image = pygame.image.load(scene_path + "back_text.png")
        self.origin_border_padding = 35
        self.border_padding = 35
       
    def draw(self):
        text = pygame.transform.scale(self.text_image, (self.width, self.height))
        instructions1 = self.font.render("use  LEFT  RIGHT  UP", True, constants.BLACK)
        instructions2 = self.font.render("arrow  to  move", True, constants.BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, constants.BLACK)
        self.window.blit(text,
                         (self.border_padding-20, self.border_padding * 2 + 30))

        self.window.blit(instructions1, (self.border_padding, self.border_padding * 2 + 45))
        self.window.blit(instructions2, (self.border_padding, self.border_padding * 2 + 85))
        self.window.blit(instructions3, (self.border_padding, self.border_padding * 2 + 120))
    
    def scale(self):
        self.border_padding = self.origin_border_padding * self.window.get_scale()
        self.width = self.original_width * self.window.get_scale()
        self.height = self.original_height * self.window.get_scale()

        self.original_border_padding = self.border_padding
        self.original_width = self.width
        self.original_height = self.height

        self.draw()

    
