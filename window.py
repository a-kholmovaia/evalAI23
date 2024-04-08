import pygame
from pygame.locals import RESIZABLE
import constants

class Window:

    def __init__(self, height=800, width=600, FPS=60):
        self.height = height
        self.width = width
        self.delta = 0
        self.screen = None
        self.FPS = FPS
        self.clock = pygame.time.Clock()
    
    def show_screen(self):
        self.screen = pygame.display.set_mode((self.height, self.width), RESIZABLE)
        self.screen.fill(constants.BLACK)

    def update(self):
        pygame.display.update()
        self.clock.tick(self.FPS)
        self.screen.fill(constants.BLACK)
    
    def window_size_changed(self):
        self.delta = self.screen.get_height() - self.height
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
    
    def blit(self, object: pygame.Surface, dest: tuple[int,int]):
        self.screen.blit(object, dest)

    def get_screen(self):
        return self.screen
    
    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width
