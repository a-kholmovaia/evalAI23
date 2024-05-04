import random
from characters.enemy import Enemy
from scenes.scene_state import SceneState
import random
class PrelevelEnemy1(Enemy):
    """
    Enemy class for the ScenePrelevel101
    """
    def __init__(self, game_screen, start_position, sprite_master, attack_prob = 10_000):
        super().__init__(game_screen, start_position, sprite_master)
        self.attack_prob = attack_prob
        self.damage = 10
    
    def policy(self, scene_state: SceneState) -> str:
        selected_action = ""
         # Randomly decide to attack or stay idle
        if self.cal_distance2player(scene_state.get_player_pos()) < 100:
            selected_action = self.close_attack()
        elif self.health<=0 and self.death_counter>0:
            selected_action = "death"
            self.death_counter -= self.speed     
        else:
            if self.health > 10:
                selected_action = 'idle'
            else:
                selected_action = 'hurt'
        if self.health<=0 and self.death_counter<=0:     
            self.current_position = (-100, -100)
            return "death"
            
        return selected_action