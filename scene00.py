import pygame
from sprite_master import SpriteMaster
from sprite_master_enemy import EnemySprite
from player import Player
from enemy import Enemy
from constants import BLACK
from typing import List
from scene import Scene

class ScenePrelevel0(Scene):
    def __init__(self, scene_path : str, player_sheet_path : str, enemy_sheet_path : str, game_screen : pygame.Surface, clock : pygame.time.Clock, font : pygame.font.Font, FPS=60):
        super().__init__(scene_path=scene_path, player_sheet_path=player_sheet_path,  
                       game_screen=game_screen, clock=clock, font=font, FPS=FPS)

        # Draw background
        self.background = pygame.transform.scale(pygame.image.load(scene_path + "background0.png"),
                                                 (self.game_screen.get_width(), self.game_screen.get_height()))
        self.background_text = pygame.transform.scale(pygame.image.load(scene_path + "back_text.png"), (280, 140))
       
        # Set characters
        # To do: make out of that one method __set_char (player and enemy classes should be changed, maybe they should have the same parent)
        self.enemy = self.__get_enemy()

        # Set scene path
        self.scene_path = scene_path

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.game_screen.fill(BLACK)
            self.game_screen.blit(self.background, (0, 0))

            keys = pygame.key.get_pressed()
            self.player.take_action(keys)
            self.enemy.take_action()

            if self.enemy.current_action == 'fight' and self.__detect_collision(self.player.current_position, self.enemy.current_position):
                self.player.health -= 1  # Reduce player health by 5 points
            if self.player.current_action == 'fight' and self.__detect_collision(self.player.current_position, self.enemy.current_position):
                self.enemy.health -= 1 # Reduce player health by 5 points

            self.draw_health_bars(self.player.health, self.enemy.health)
            
            self.__draw_instructions()

            pygame.display.flip()
            self.clock.tick(self.FPS)  

    def __get_enemy(self) -> List[Enemy]:
        sprite = EnemySprite("levels/level0/enemy", idle=3, walk=5, attack=4, hurt=2, death=5)
        return Enemy(self.game_screen, self.enemy_pos, sprite)

    def __draw_instructions(self):
        border_padding = 35
        instructions1 = self.font.render("use  LEFT  RIGHT  UP", True, BLACK)
        instructions2 = self.font.render("arrow  to  move", True, BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, BLACK)
        self.game_screen.blit(self.background_text,
                         (border_padding-20, border_padding * 2 + 30))

        self.game_screen.blit(instructions1, (border_padding, border_padding * 2 + 45))
        self.game_screen.blit(instructions2, (border_padding, border_padding * 2 + 85))
        self.game_screen.blit(instructions3, (border_padding, border_padding * 2 + 120))

    def __detect_collision(self, position1, position2):
        # Simple collision detection (can be improved)
        distance = position1.distance_to(position2)
        return distance < 50  # Adjust threshold according to your game's scale