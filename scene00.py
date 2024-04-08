import pygame
from sprite_master_enemy import EnemySprite
from enemy import Enemy
from constants import BLACK
from typing import List
from scene import Scene
from window import Window
from drawable_objects.background import Background
from drawable_objects.instructions import Instructions

class ScenePrelevel0(Scene):
    def __init__(self, scene_path : str, player_sheet_path : str, enemy_sheet_path : str, window : Window, clock : pygame.time.Clock, font : pygame.font.Font, FPS=60):
        super().__init__(scene_path=scene_path, player_sheet_path=player_sheet_path,  
                       window=window, clock=clock, font=font, FPS=FPS)

        self.background = Background(scene_path, window)

        self.instructions = Instructions(scene_path, window, font)
       
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
            
            self.window.update()

            self.background.draw(self.window)
            

            keys = pygame.key.get_pressed()
            self.player.take_action(keys)
            self.enemy.take_action()

            if self.enemy.current_action == 'fight' and self.__detect_collision(self.player.current_position, self.enemy.current_position):
                self.player.health -= 1  # Reduce player health by 5 points
            if self.player.current_action == 'fight' and self.__detect_collision(self.player.current_position, self.enemy.current_position):
                self.enemy.health -= 1 # Reduce player health by 5 points

            self.player_healthbar.draw(self.window, self.player.health)
            self.enemy_healthbar.draw(self.window, self.enemy.health)
            
            self.instructions.draw(self.window)

    def __get_enemy(self) -> List[Enemy]:
        sprite = EnemySprite("levels/level0/enemy", idle=3, walk=5, attack=4, hurt=2, death=5)
        return Enemy(self.window.get_screen(), self.enemy_pos, sprite)

    def __detect_collision(self, position1, position2):
        # Simple collision detection (can be improved)
        distance = position1.distance_to(position2)
        return distance < 50  # Adjust threshold according to your game's scale