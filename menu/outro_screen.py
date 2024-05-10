import pygame 
import sys
from constants import BLACK, GREEN

class OutroScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("menu/back_text.png")
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.font = pygame.font.Font('font.TTF', 30)
        self.content = self.set_content()
        self.text_color = BLACK
        self.continue_button_rect = pygame.Rect(screen.get_width() * 0.7, screen.get_height() * 0.85, 180, 40)
        self.spirit_image = pygame.image.load('menu/sir_code_a_lot.png')
        self.spirit_image = pygame.transform.scale(self.spirit_image, 
                                            (self.screen.get_width()//4, self.screen.get_width()//4))
        self.running = True    

    def set_content(self):
        text = [
            "The  game  is  over!",
            "You  saved  PixelPuff!",
            "Thank  you  for  taking  part  in  our  survey!"
        ]
        return text

    def run(self):
        while self.running:
            self.handle_events()
            self.render()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button_rect.collidepoint(event.pos):
                    self.running = False

    def render(self):
        # Draw the background
        self.screen.blit(self.background, (0, 0))
        
        # Render and draw the text
        text_surface = self.font.render(self.content[0], True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.7))
        self.screen.blit(text_surface, text_rect)
        
        text_surface = self.font.render(self.content[1], True, GREEN)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.3))
        self.screen.blit(text_surface, text_rect)

        text_surface = self.font.render(self.content[2], True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_surface, text_rect)


        self.screen.blit(self.spirit_image, (self.screen.get_width()*0.1, self.screen.get_height()*0.57))

        # Render & draw continue button
        continue_surface = self.font.render('Close', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 128, 0), self.continue_button_rect)  # Green button
        self.screen.blit(continue_surface, (self.continue_button_rect.x + 50, self.continue_button_rect.y))
        
        # Update the display
        pygame.display.flip()
    