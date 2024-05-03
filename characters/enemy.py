from characters.character import Character
from scenes.scene_state import SceneState

class Enemy(Character):
    def __init__(self, game_screen, start_position, sprite_master):
        super().__init__(sprite_master, game_screen, start_position)
        self.health = 100


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
