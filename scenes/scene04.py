import pygame
from scenes.scene00 import ScenePrelevel00
from masters.save_master import SaveMaster
from characters.level3.projectile_level3 import Projectile
from characters.level3.wizard_level3 import ThirdBoss
from tools import Video 

class Scene04(ScenePrelevel00):

    def __init__(self, scene_path: str, save_master: SaveMaster, game_screen: pygame.Surface, 
                 clock : pygame.time.Clock, font : pygame.font.Font, intro_video: Video, FPS=60, display_instructions=False):
        super().__init__(scene_path, save_master, game_screen, clock, font, display_instructions=False)
        self.id = 104
        self.level = 3
        self.enemy_pos = pygame.Vector2(self.game_screen.get_width()*0.75, self.game_screen.get_height() * 0.59)
        self.enemies = [ThirdBoss(game_screen, self.enemy_pos.copy(), Projectile(game_screen, self.enemy_pos.copy()))]
        self.platform_positions = [(600, 320), (180, 320)]
        self.scaled_width_platforms = 110
        self.platforms = []
        self.intro_video = intro_video
        self.load_platforms()

        self.enemies[0].current_position = pygame.Vector2(550, 80)
        
