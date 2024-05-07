import pygame 
import sys
from constants import BLACK, GREEN

class IntroductionScreen:
    def __init__(self, screen, level=1, round=0):
        self.screen = screen
        self.background = pygame.image.load("questions/back_text.png")
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.font = pygame.font.Font('font.TTF', 36)
        self.content = self.set_content(level, round)
        self.text_color = BLACK
        self.continue_button_rect = pygame.Rect(screen.get_width() * 0.7, screen.get_height() * 0.85, 180, 40)
        self.running = True    

    def set_content(self, level, round):
        text = ["Willkommen  im  Bereich"]
        topics = {
            (1,0): "Arbeit  im  Team",
            (1,1): "Arbeit  mit  Mentor",
            (2, 0): "Projekt",
            (3, 0): "Lernunterstuetzung",
        }
        text.append(topics.get((level, round)))
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
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.25))
        self.screen.blit(text_surface, text_rect)
        
        text_surface = self.font.render(self.content[1], True, GREEN)
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text_surface, text_rect)

        # Render & draw continue button
        continue_surface = self.font.render('Continue', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 128, 0), self.continue_button_rect)  # Green button
        self.screen.blit(continue_surface, (self.continue_button_rect.x + 10, self.continue_button_rect.y))
        
        # Update the display
        pygame.display.flip()
    