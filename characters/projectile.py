from characters.enemy import Enemy
from scenes.scene_state import SceneState
from masters.sprite_master import SpriteMaster

class Projectile(Enemy):
    def __init__(self, game_screen, start_position):
        super().__init__(game_screen, start_position, SpriteMaster("levels/test_levels/distant_attack/enemy", 
                              idle=0, walk=0, attack=4, 
                              hurt=0, death=3, block=0, start_action="hit"))
        self.current_action = "hit"

    def policy(self, scene_state: SceneState) -> str:
        """
        Moves left and attacks constantly
        """
        self.current_position[0] -= self.speed 
        return "hit"


