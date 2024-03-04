import pygame
from main_menu import main_menu
from welcome_menu import welcome_menu
from play_intro import play_intro_video
from level import Level
from scene import Scene

class Game:
    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font("font.TTF", 24)

        # Screen dimensions
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()

    def run_game_loop(self):
        pygame.display.set_caption("AI-Lab: the final Battle")
        welcome_menu(self.screen)
        main_menu(self.screen)
        play_intro_video()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            scene_test = Scene("levels/level_1/scene_1/", "img/AnimationSheet_Character.png", "img/monster-pre.png", self.screen, self.clock, self.font)
            scene_test.run()

            pygame.display.flip()
            self.clock.tick(self.FPS)
