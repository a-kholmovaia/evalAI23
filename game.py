import pygame
from pygame.locals import RESIZABLE
from menu.main_menu import main_menu
from menu.welcome_menu import welcome_menu
from play_intro import play_intro_video
from level import Level
from scene00 import ScenePrelevel0
from window import Window
from event_handler import EventHandler

class Game:
    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font("font.TTF", 24)

        # Screen dimensions
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)

        self.window = Window()

        self.event_handler = EventHandler(self.window)

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        self.img_path = img_path

    def run(self):
        #pygame.display.set_caption("AI-Lab: the final Battle")
        #welcome_menu(self.screen)
        #main_menu(self.screen)
        #play_intro_video()

        self.window.show_screen()
        level1 = Level([ScenePrelevel0(self.event_handler, "levels/level_1/scene_1/", "img/AnimationSheet_Character.png", "img/monster-pre.png", self.window, self.clock, self.font)])

        paused = False
        while self.event_handler.listen_events():
            self.window.update()
            level1.run()

