import pygame
import sys
from tools import Button
from constants import WHITE, BLUE

# Main menu
def welcome_menu(screen):
    # Font
    title_font = pygame.font.Font(None, 48)
    text_font = pygame.font.Font(None, 24)

    # Load background image
    background_img = pygame.transform.scale(pygame.image.load("img/welcome_menu.png"), (screen.get_width(), screen.get_height()))

    start_button = Button(screen.get_width()-300, screen.get_height()-100, 200, 50, BLUE, "START", WHITE, title_font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    return
        screen.fill((0,0,0))
        # Clear the screen
        screen.blit(background_img, (0, 0))

        # Draw start button
        start_button.draw(screen)

        # Update the display
        pygame.display.flip()