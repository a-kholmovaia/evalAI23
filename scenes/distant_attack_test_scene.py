import pygame
from scenes.scene00 import ScenePrelevel00
from masters.save_master import SaveMaster
from characters.projectile import Projectile
from characters.wizard import Wizard

class DistantAttackTestScene(ScenePrelevel00):

    def __init__(self, scene_path: str, save_master: SaveMaster, game_screen: pygame.Surface, 
                 clock : pygame.time.Clock, font : pygame.font.Font, FPS=60, display_instructions=True):
        super().__init__(scene_path, save_master, game_screen, clock, font)
        self.id = 102
        self.proj_pos = pygame.Vector2(self.enemy_pos[0], self.enemy_pos[1])
        self.enemies = [Wizard(game_screen, self.enemy_pos, Projectile(game_screen, self.proj_pos))]
