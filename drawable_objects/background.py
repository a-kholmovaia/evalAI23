import pygame
from idrawable import IDrawable
from window import Window

class Background(IDrawable):

    def __init__(self, scene_path: str, window: Window):
        self.window = window
        self.rect = pygame.transform.scale(pygame.image.load(scene_path + "background0.png"),
                                                 (self.window.get_width(), self.window.get_height()))
       
    def draw(self, window: Window):
        self.window.blit(self.rect, (0, 0))
    
    def resize(self, window: Window):
        pass