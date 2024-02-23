import pygame
import sys
import psycopg2
# Initialize Pygame
pygame.init()
from constants import WHITE, BLUE, WIDTH, HEIGHT, OUTPUT_FILE_PATH
from tools import TextInputBox, Button
# Font
font = pygame.font.Font(None, 32)


# Main menu loop
def main_menu(screen):
    username_input = TextInputBox(500, 250, 200, 40, font)
    full_name_input = TextInputBox(500, 350, 200, 40, font)
    start_button = Button(WIDTH - 300, HEIGHT - 100, 200, 50, BLUE, "START", WHITE, font)
    background_img = pygame.transform.scale(pygame.image.load("img/username_menu.png"), (WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            username_input.handle_event(event)
            full_name_input.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    if username_input.text != "" and full_name_input.text != "":
                        with open(OUTPUT_FILE_PATH, "a") as f:
                            f.write(username_input.text + ", " + full_name_input.text)
                        return
        # Clear the screen
        screen.fill(WHITE)
        # Clear the screen
        screen.blit(background_img, (0, 0))
        # Draw text input fields

        username_text = font.render("Enter your username:", True, WHITE)
        screen.blit(username_text, (username_input.x-250, username_input.y))
        username_input.draw(screen)

        fullname_text = font.render("Enter your full name:", True, WHITE)
        screen.blit(fullname_text, (full_name_input.x-250, full_name_input.y))
        full_name_input.draw(screen)

        start_button.draw(screen)

        # Update the display
        pygame.display.flip()

# Main loop
#main_menu()