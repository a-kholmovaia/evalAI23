import random
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
        
        # If it's the hitting frame then set the current action on "hit" instead of "fight"
        if self.current_action == "fight" and int(self.fight_counter) == len(self.sprite_master.attack_images) // 2:
            self.fight_counter -= self.speed
            return "hit"
        
        # If it has been "fight" or "hit", the attack frames have left yet and it's currently not the hitting frame 
        # then return "fight"
        if (self.current_action == "fight" or self.current_action == "hit") and self.fight_counter > 0:
            self.fight_counter -= self.speed
            return "fight"
        
        # If it's not "fight" and the player's character is close enough 
        # then set the current action on "fight" with some probability depending on attack_prob 
        if self.cal_distance2player(scene_state.get_player_pos()) <= 70 and random.randint(1, self.attack_prob) > self.attack_prob * 0.75:
            self.fight_counter = len(self.sprite_master.attack_images)
            return "fight"
            
        if self.health > 10:
            return "idle"
        
        if self.health > 0:
            return "hurt"
        
        if self.health<=0 and self.death_counter>0:
            self.death_counter -= self.speed
            return "death"   
        
        if self.health <= 0 and self.death_counter <= 0:
            self.current_position = (-100, -100)
            return "death"
            
        return "idle"