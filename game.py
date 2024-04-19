import pygame
from menu.main_menu import main_menu
from menu.welcome_menu import welcome_menu
from play_intro import play_intro_video
from scene00 import ScenePrelevel0
from qa_evaluator import QAEvaluator

class Game:
    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font("font.TTF", 24)

        # Screen dimensions
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        self.img_path = img_path

    def run(self):
        pygame.display.set_caption("AI-Lab: the final Battle")
        welcome_menu(self.screen)
        main_menu(self.screen)
        play_intro_video()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        evaluator = QAEvaluator(screen=self.screen, level=1)
        evaluator.run()
