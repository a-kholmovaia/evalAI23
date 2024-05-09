from characters.character import Character
from scenes.scene_state import SceneState
import random

class Enemy(Character):
    def __init__(self, game_screen, start_position, sprite_master, attack_probability=0.97):
        super().__init__(sprite_master, game_screen, start_position)
        self.attack_probability = attack_probability
        self.collision_distance = 50


    def take_action(self, scene_state: SceneState) -> None:
        self.current_action = self.policy(scene_state)
        self.draw_current_action()

    def policy(self, scene_state: SceneState) -> str:
        """
        Evaluates the current state to return the next action to take
        Parameters:
        scene_state: SceneState - a state the policy is basing on to select an action
        Returns:
        next_action: String - the next action to take based on the SceneState instance 
        """
        pass

    
    def cal_distance2player(self, player_position):
        # Simple collision detection (can be improved)
        distance = self.current_position.distance_to(player_position)
        return distance  # Adjust threshold according to your game's scale
    
    def close_attack(self):
        if self.current_action == "fight": 
                    # if the action was fight and the frame index is 0 again (action was executed)
                if self.sprite_master.round_done:
                    selected_action = 'idle'
                elif self.sprite_master.frame_index > 2:
                    selected_action = "hit"
                else: # excetion was not executed, continue
                    selected_action = 'fight'
        elif random.random() > self.attack_probability:  # probability to attack
            selected_action = 'fight'
        else:
            selected_action = 'idle'
        return selected_action
