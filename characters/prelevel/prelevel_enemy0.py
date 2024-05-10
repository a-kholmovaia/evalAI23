import pygame
from characters.enemy import Enemy
from scenes.scene_state import SceneState

class PrelevelEnemy0(Enemy):
    """
    Enemy class for the ScenePrelevel100
    """
    def __init__(self, game_screen, start_position, sprite_master):
        super().__init__(game_screen, start_position, sprite_master)
        self.collision_distance = 50

    def policy(self, scene_state: SceneState) -> str:
        """
        Just stays
        """

        if self.current_health<=0:
            if self.sprite_master.round_done:
                self.current_position= pygame.Vector2((-100, -100))
                return "death"
            return "dying"

        return "idle"