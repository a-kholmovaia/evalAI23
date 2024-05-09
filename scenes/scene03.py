import pygame
from scenes.scene00 import ScenePrelevel00
from masters.save_master import SaveMaster
from characters.level2.projectile_level2 import Projectile
from characters.level2.wizard_level2 import SecondBoss
from tools import Video 
class Scene03(ScenePrelevel00):

    def __init__(self, scene_path: str, save_master: SaveMaster, game_screen: pygame.Surface, 
                 clock : pygame.time.Clock, font : pygame.font.Font, intro_video: Video, FPS=60, display_instructions=False):
        super().__init__(scene_path, save_master, game_screen, clock, font, display_instructions=False)
        self.id = 103
        self.level = 2
        self.enemy_pos = pygame.Vector2(self.game_screen.get_width()*0.75, self.game_screen.get_height() * 0.5)
        self.enemies = [SecondBoss(game_screen, self.enemy_pos.copy(), Projectile(game_screen, self.enemy_pos.copy()))]
        self.platform_positions = [(450, 320), (180, 330)]
        self.scaled_width_platforms = 110
        self.platforms = []
        self.intro_video = intro_video
        self.load_platforms()

        
