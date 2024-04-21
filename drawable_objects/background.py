import pygame
from drawable_objects.drawable_object import DrawableObject
from window import Window

class Background(DrawableObject):

    def __init__(self, scene_path: str, window: Window):
        super().__init__(window, 0, 0, window.get_width(), window.get_height())
        self.scene_path = scene_path
        self.image = pygame.image.load(scene_path + "background0.png")


    def draw(self):
        surface = pygame.transform.scale(self.image,
                                                 (self.width, self.height))
        self.window.blit(surface, (self.x, self.y))