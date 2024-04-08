import pygame
import constants
from idrawable import IDrawable
from window import Window

class EnemyHealthbar(IDrawable):
    def __init__(self, scene_path: str, font: pygame.font.Font):
        self.max_health_width = 200
        self.health_bar_height = 20
        self.border_padding = 15
        self.background_health = pygame.transform.scale(pygame.image.load(scene_path + "back_text.png"), (240, 80))
        self.font = font

    def draw(self, window: Window, health: int):
        window.blit(self.background_health, (window.get_width()-240, 0))
        pygame.draw.rect(window.get_screen(), (255, 0, 0), (window.get_width() - self.max_health_width - self.border_padding, self.border_padding, self.max_health_width, self.health_bar_height))
        pygame.draw.rect(window.get_screen(), (0, 255, 0), (
        window.get_width() - self.max_health_width - self.border_padding, self.border_padding, health*2, self.health_bar_height))
        window.blit(self.font.render("enemy  health", True, constants.BLACK), (window.get_width() - 13*self.border_padding, self.border_padding  + 5 + self.health_bar_height))

    
    def resize(self, window: Window):
        pass

    # Enemy health bar
        