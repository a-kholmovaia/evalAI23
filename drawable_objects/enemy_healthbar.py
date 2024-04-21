import pygame
import constants
from drawable_objects.drawable_object import DrawableObject
from window import Window

class EnemyHealthbar(DrawableObject):
    def __init__(self, window: Window, scene_path: str, font: pygame.font.Font):
        super().__init__(window, window.get_width() - 240, 0, 240, 80)
        self.cur_health = 100
        self.original_max_health_width = 200
        self.original_health_bar_height = 20
        self.original_border_padding = 15
        self.max_health_width = 200
        self.health_bar_height = 20
        self.border_padding = 15
        self.image = pygame.image.load(scene_path + "back_text.png")
        self.font = font

    def draw(self):
        background_health = pygame.transform.scale(self.image, (self.width, self.height))
        self.window.blit(background_health, (self.x, self.y))
        pygame.draw.rect(self.window.get_screen(), (255, 0, 0), (self.window.get_width() - self.max_health_width - self.border_padding, self.border_padding, self.max_health_width, self.health_bar_height))
        pygame.draw.rect(self.window.get_screen(), (0, 255, 0), (
        self.window.get_width() - self.max_health_width - self.border_padding, self.border_padding, self.cur_health*2, self.health_bar_height))
        self.window.blit(self.font.render("enemy  health", True, constants.BLACK), (self.window.get_width() - 13*self.border_padding, self.border_padding  + 5 + self.health_bar_height))

    def scale(self):
        self.x = self.original_x * self.window.get_scale()
        self.y = self.original_y * self.window.get_scale()
        self.width = self.original_width * self.window.get_scale()
        self.height = self.original_height * self.window.get_scale()
        self.max_health_width = self.original_max_health_width * self.window.get_scale()
        self.health_bar_height = self.original_health_bar_height * self.window.get_scale()
        self.border_padding = self.original_border_padding * self.window.get_scale()

        self.original_x = self.x
        self.original_y = self.y
        self.original_width = self.width
        self.original_height = self.height
        self.original_max_health_width = self.max_health_width
        self.original_health_bar_height = self.health_bar_height
        self.original_border_padding = self.border_padding

        self.draw()
    
    def set_cur_health(self, cur_health: int):
        self.cur_health = cur_health
        