import pygame
from scenes.scene00 import ScenePrelevel00
from masters.save_master import SaveMaster
from masters.sprite_master import SpriteMaster
from characters.projectile import Projectile

class DistantAttackTestScene(ScenePrelevel00):

    def __init__(self, scene_path: str, save_master: SaveMaster, game_screen: pygame.Surface, 
                 clock : pygame.time.Clock, font : pygame.font.Font, FPS=60, display_instructions=True):
        super().__init__(scene_path, save_master, game_screen, clock, font)
        self.id = 102
        self.enemies = [Projectile(game_screen, self.enemy_pos, SpriteMaster("levels/test_levels/distant_attack/enemy", 
                              idle=0, walk=0, attack=1, 
                              hurt=0, death=0, block=0, start_action="hit"))]
