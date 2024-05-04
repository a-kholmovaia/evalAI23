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
    
    def policy(self, scene_state: SceneState) -> str:
        selected_action = ""
         # Randomly decide to attack or stay idle
        if self.cal_distance2player(scene_state.get_player_pos()):
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

    def close_attack(self):
        if self.current_action == "fight": 
                    # if the action was fight and the frame index is 0 again (action was executed)
                if self.sprite_master.round_done:
                    selected_action = 'idle'
                else: # excetion was not executed, continue
                    selected_action = 'fight'
        elif random.random() > 0.97:  # probability to attack
            selected_action = 'fight'
        else:
            selected_action = 'idle'
        return selected_action