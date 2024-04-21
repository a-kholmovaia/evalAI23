import pygame
from pygame.locals import RESIZABLE
import constants

class Window:

    def __init__(self, width=800, height=600, FPS=60):
        self.original_height = height
        self.original_width = width
        self.height = height
        self.width = width
        self.scale = 1
        self.screen = None
        self.FPS = FPS
        self.clock = pygame.time.Clock()
    
    def show_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        self.screen.fill(constants.BLACK)

    def update(self):
        pygame.display.update()
        self.clock.tick(self.FPS)
        self.screen.fill(constants.BLACK)
    
    def window_size_changed(self):
        self.scale = self.screen.get_width() / self.original_width
        self.height = self.original_height * self.scale
        self.width = self.screen.get_width()
        self.original_width = self.width
        self.original_height = self.height
        
    
    def blit(self, object: pygame.Surface, dest: tuple[int,int]):
        self.screen.blit(object, dest)

    def get_screen(self):
        return self.screen
    
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
    
    def get_scale(self):
        return self.scale
