import pygame
from sprite_master import SpriteMaster
from enemy import Enemy
from constants import BLACK, BACK_TEXT_PATH
from typing import List
from scene import Scene

class ScenePrelevel00(Scene):
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

    def take_step(self):
        """
        Contain the unique behaviour of this implementation of the class scene
        Parameters:
        ---
        Returns:
        Void
        """
        print("__take_step() entered")
        keys = pygame.key.get_pressed()
        self.player.take_action(keys)
        self.enemy.take_action(self.player.current_position)

        self.handle_collisions()

        self.draw_health_bars(self.player.health, self.enemy.health)
            
        if self.display_instructions:
            self.draw_instructions()



    def draw_instructions(self):
        border_padding = 35
        instructions1 = self.font.render("use  UP   RIGHT   LEFT", True, BLACK)
        instructions2 = self.font.render("arrows  to  move", True, BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, BLACK)
        self.game_screen.blit(self.background_text_instruction,
                         (border_padding-20, border_padding * 2 + 30))

        self.game_screen.blit(instructions1, (border_padding, border_padding * 2 + 45))
        self.game_screen.blit(instructions2, (border_padding, border_padding * 2 + 85))
        self.game_screen.blit(instructions3, (border_padding, border_padding * 2 + 120))
    

    def __get_enemy(self) -> List[Enemy]:
        sprite = SpriteMaster("levels/level0/enemy", 
                              idle=3, walk=5, attack=4, 
                              hurt=2, death=5, block=0,
                              )
        return Enemy(self.game_screen, self.enemy_pos, sprite)
    
