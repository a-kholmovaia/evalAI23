from characters.enemy import Enemy
from scenes.scene_state import SceneState

class PrelevelEnemy1(Enemy):
    """
    Enemy class for the ScenePrelevel101
    """
    def __init__(self, game_screen, start_position, sprite_master, attack_prob = 10_000):
        super().__init__(game_screen, start_position, sprite_master)
        self.attack_prob = attack_prob
    
    def policy(self, scene_state: SceneState) -> str:
        # Randomly decide to attack or stay idle (temporarily removed)
        selected_action = ""
        if self.cal_distance2player(scene_state.get_player_pos()):
            selected_action = 'fight'
            self.fight_counter -= self.speed
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
        print(f"policy returns {selected_action}")
        return selected_action