import pygame
import sys
from game import Game
from constants import WIDTH, HEIGHT
from main_menu import main_menu
from welcome_menu import welcome_menu
from play_intro import play_intro_video
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI-Lab: the final Battle")
    # Initialize game
    game = Game( screen, img_path="img/",)
    welcome_menu(screen)
    main_menu(screen)
    play_intro_video()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game.run_game_loop()
    print("the game has succesfully ended")