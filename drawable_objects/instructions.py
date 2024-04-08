import pygame
from idrawable import IDrawable
from window import Window
import constants

class Instructions(IDrawable):

    def __init__(self, scene_path: str, window: Window, font: pygame.font.Font):
        self.window = window
        self.font = font
        self.text = pygame.transform.scale(pygame.image.load(scene_path + "back_text.png"), (280, 140))
        self.border_padding = 35
       
    def draw(self, window: Window):
        instructions1 = self.font.render("use  LEFT  RIGHT  UP", True, constants.BLACK)
        instructions2 = self.font.render("arrow  to  move", True, constants.BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, constants.BLACK)
        self.window.blit(self.text,
                         (self.border_padding-20, self.border_padding * 2 + 30))

        self.window.blit(instructions1, (self.border_padding, self.border_padding * 2 + 45))
        self.window.blit(instructions2, (self.border_padding, self.border_padding * 2 + 85))
        self.window.blit(instructions3, (self.border_padding, self.border_padding * 2 + 120))
    
    def resize(self, window: Window):
        pass