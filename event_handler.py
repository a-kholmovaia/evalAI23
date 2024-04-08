import pygame
from window import Window
from scene import Scene


class EventHandler:

    def __init__(self, scene: Scene, window : Window):
        self.scene = scene
        self.window = window

    def listen_events(self):
        for event in pygame.event.get():
                if event.type == pygame.WINDOWRESIZED:
                    self.window.window_size_changed()
                    self.scene.__resize_scene()