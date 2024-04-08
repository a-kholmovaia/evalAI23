import pygame
from pygame.locals import RESIZABLE
from menu.main_menu import main_menu
from menu.welcome_menu import welcome_menu
from play_intro import play_intro_video
from level import Level
from scene00 import ScenePrelevel0
from window import Window

class Game:
    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font("font.TTF", 24)

        # Screen dimensions
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), RESIZABLE)

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        self.img_path = img_path

    def run(self):
        pygame.display.set_caption("AI-Lab: the final Battle")
        welcome_menu(self.screen)
        main_menu(self.screen)
        play_intro_video()

        window = Window()
        window.show_screen()
        level1 = Level([ScenePrelevel0("levels/level_1/scene_1/", "img/AnimationSheet_Character.png", "img/monster-pre.png", window, self.clock, self.font)])

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            level1.run()

            pygame.display.flip()
            self.clock.tick(self.FPS)
