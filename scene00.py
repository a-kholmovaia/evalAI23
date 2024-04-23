import pygame
from sprite_master import SpriteMaster
from enemy import Enemy
from constants import BLACK, BACK_TEXT_PATH
from typing import List
from scene import Scene

class ScenePrelevel0(Scene):
    def __init__(self, scene_path : str, game_screen : pygame.Surface, 
                 clock : pygame.time.Clock, font : pygame.font.Font, FPS=60, display_instructions=True):
        super().__init__(scene_path=scene_path, 
                       game_screen=game_screen, clock=clock, font=font, FPS=FPS)

        # Draw background
        self.background = pygame.transform.scale(pygame.image.load(scene_path + "background0.png"),
                                                 (self.game_screen.get_width(), self.game_screen.get_height()))
        # Set characters
        # To do: make out of that one method __set_char (player and enemy classes should be changed, maybe they should have the same parent)
        self.enemy = self.__get_enemy()

        # Set scene path
        self.scene_path = scene_path

        self.display_instructions = display_instructions

        self.load_platforms()

    def load_platforms(self):
        platform_image_path = self.scene_path + "platform.png"
        original_platform_image = pygame.image.load(platform_image_path)
        scaled_width = 100  # Define the desired width
        # Assuming you want to maintain the aspect ratio
        aspect_ratio = original_platform_image.get_height() / original_platform_image.get_width()
        scaled_height = int(scaled_width * aspect_ratio)
        
        # Define platform positions (x position, y height)
        positions = [(450, 170), (670, 310), (300, 360)]
        for pos in positions:
            scaled_image = pygame.transform.scale(original_platform_image, (scaled_width, scaled_height))
            rect = scaled_image.get_rect(bottomleft=pos)
            self.platforms.append((scaled_image, rect))

    def run(self):
        while self.do_continue_game_loop:
            self.listen_events()
            
            self.game_screen.fill(BLACK)
            self.game_screen.blit(self.background, (0, 0))
            self.draw_platforms()

            keys = pygame.key.get_pressed()
            self.player.take_action(keys)
            self.enemy.take_action()

            self.handle_collisions()

            self.draw_health_bars(self.player.health, self.enemy.health)
            
            if self.display_instructions:
                self.draw_instructions()

            if self.enemy.health <= 0: 
                self.won()

            pygame.display.flip()
            self.clock.tick(self.FPS)  

    def __get_enemy(self) -> List[Enemy]:
        sprite = SpriteMaster("levels/level0/enemy", idle=3, walk=5, attack=4, hurt=2, death=5)
        return Enemy(self.game_screen, self.enemy_pos, sprite)
    
