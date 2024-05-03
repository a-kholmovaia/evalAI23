from characters.enemy import Enemy
from scenes.scene_state import SceneState

class Projectile(Enemy):
    def __init__(self, game_screen, start_position, sprite_master):
        super().__init__(game_screen, start_position, sprite_master)
        self.current_action = "hit"

    def policy(self, scene_state: SceneState) -> str:
        """
        Moves left and attacks constantly
        """
        self.current_position[0] -= self.speed 
        return "hit"


