import pygame
from window import Window
from scene import Scene
from game import Game


class EventHandler:

    def __init__(self, game: Game, window : Window):
        self.game = game
        self.window = window

    def listen_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.WINDOWRESIZED:
                    self.window.window_size_changed()
                    self.scene.__resize_scene()
        return True