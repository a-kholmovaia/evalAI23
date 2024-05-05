import pygame
from masters.sprite_master import SpriteMaster
from characters.prelevel.prelevel_enemy1 import PrelevelEnemy1
from constants import BLACK
from typing import List
from scenes.scene import Scene
from masters.save_master import SaveMaster

class ScenePrelevel01(Scene):
    def __init__(self, scene_path: str, save_master: SaveMaster, game_screen: pygame.Surface, 
                 clock : pygame.time.Clock, font : pygame.font.Font, FPS=60, display_instructions=True):
        super().__init__(scene_path=scene_path, save_master=save_master, 
                         game_screen=game_screen, clock=clock, font=font, FPS=FPS)
        
        # Set ID 
        self.id = 101

        # Draw background
        self.background = pygame.transform.scale(pygame.image.load(scene_path + "background0.png"),
                                                 (self.game_screen.get_width(), self.game_screen.get_height()))
        # Set characters
        # To do: make out of that one method __set_char (player and enemy classes should be changed, maybe they should have the same parent)
        self.enemies.append(self.__get_enemy())

        # Set scene path
        self.scene_path = scene_path

        self.display_instructions = display_instructions

        self.load_platforms()
        platform_pos = self.platforms[1][1]
        self.enemies[0].current_position = pygame.Vector2(
            platform_pos[0] + platform_pos[2]*0.5, 
            platform_pos[1] - platform_pos[3]*1.2)

    def load_platforms(self):
        platform_image_path = self.scene_path + "platform.png"
        original_platform_image = pygame.image.load(platform_image_path)
        scaled_width = 170  # Define the desired width
        scaled_height = 75
       
        # Define platform positions (x position, y height)
        positions = [(300, 380), (600, 360)]
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
        keys = pygame.key.get_pressed()
        self.player.take_action(keys)
        for enemy in self.enemies:
            enemy.take_action(self.scene_state)
            
        self.handle_collisions()

        self.draw_health_bars(self.player.health, self.enemies[0].health)
                
        if self.display_instructions:
            self.draw_instructions()
    
    def draw_instructions(self):
        border_padding = 35
        instructions1 = self.font.render("use  B  key", True, BLACK)
        instructions2 = self.font.render("to  block", True, BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, BLACK)
        self.game_screen.blit(self.background_text_instruction,
                         (border_padding-20, border_padding * 2 + 30))

        self.game_screen.blit(instructions1, (border_padding, border_padding * 2 + 45))
        self.game_screen.blit(instructions2, (border_padding, border_padding * 2 + 85))
        self.game_screen.blit(instructions3, (border_padding, border_padding * 2 + 120))

    def __get_enemy(self) -> PrelevelEnemy1:
        sprite = SpriteMaster("levels/level0/enemy", 
                              idle=3, walk=5, attack=4, 
                              hurt=2, death=5, block=0)
        
        return PrelevelEnemy1(self.game_screen, self.enemy_pos, sprite, attack_prob=200)
