from characters.enemy import Enemy
from scenes.scene_state import SceneState

class PrelevelEnemy0(Enemy):
    """
    Enemy class for the ScenePrelevel100
    """
    def __init__(self, game_screen, start_position, sprite_master):
        super().__init__(game_screen, start_position, sprite_master)

    def policy(self, scene_state: SceneState) -> str:
        """
        Just stays
        """
        return "idle"