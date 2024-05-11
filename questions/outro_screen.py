import pygame 
import sys
from constants import BLACK, GREEN
from questions.introduction_screen import IntroductionScreen

class Artifact(IntroductionScreen):
    def __init__(self, screen, level=1):
        super().__init__(screen, level=level)  

    def set_content(self, level, round):
        path = "img/artifacts/"
        text = ["Congratulations!  You  won"]
        if level==1:
            text.append("Synergy  Stone        20   Health   Points")
            path += "synergy_stone.png"
            self.effect = 20
            self.type = "p_health"
        elif level==2:
            text.append("Alliance Amulet        30  Damage Increase")
            path += "alliance_amulet.png"
            self.effect = 30
            self.type = "damage"
        elif level==3:
            text.append("Resilience Ring       20 Health  Points")
            path += "resilience_ring.png"
            self.effect = -20
            self.type = "e_health"
        else:
            raise NotImplementedError
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, 
                                            (self.screen.get_width()//4, self.screen.get_height()//4))
        return text

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

        img_rect = self.image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 1.5))
        self.screen.blit(self.image, img_rect)

        # Render & draw continue button
        continue_surface = self.font.render('Continue', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 128, 0), self.continue_button_rect)  # Green button
        self.screen.blit(continue_surface, (self.continue_button_rect.x + 10, self.continue_button_rect.y))
        
        # Update the display
        pygame.display.flip()