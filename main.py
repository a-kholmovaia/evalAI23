import pygame
from constants import WIDTH, HEIGHT
from intro import intro
from main_menu import  main_menu
from welcome_menu import welcome_menu
pygame.init()
# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Lab: Final Battle")
welcome_menu(screen)
main_menu(screen)
intro(screen)