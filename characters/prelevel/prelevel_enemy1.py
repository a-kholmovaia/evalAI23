import pygame
from characters.enemy import Enemy
from scenes.scene_state import SceneState
class PrelevelEnemy1(Enemy):
    """
    Enemy class for the ScenePrelevel101
    """
    def __init__(self, game_screen, start_position, sprite_master, attack_prob = 10_000):
        super().__init__(game_screen, start_position, sprite_master)
        self.attack_prob = attack_prob
        self.damage = 10
        self.collision_distance = 50
    
    def policy(self, scene_state: SceneState) -> str:

        if self.current_health<=0:
            if self.sprite_master.round_done:
                self.current_position= pygame.Vector2((-100, -100))
                return "death"
            return "dying"
        
         # Decide to attack if the player's character is close enough
        if self.cal_distance2player(scene_state.get_player_pos()) < 100:
            return self.close_attack()   
        else:
            if self.current_health > 10:
                return 'idle'
            else:
                return 'hurt'