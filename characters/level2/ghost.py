from characters.enemy import Enemy
from characters.attack_info import AttackInfo
from masters.sprite_master import SpriteMaster
from scenes.scene_state import SceneState

class Ghost(Enemy):
    """
    A simple and weak opponent moving towards the player and dealing blows
    """

    def __init__(self, game_screen, start_position):
        super().__init__(game_screen, start_position, SpriteMaster("levels/level2/ghost", 
                              idle=3, walk=5, attack=4, 
                              hurt=2, death=5, block=0))
        self.health = 1
        self.attack_info = AttackInfo(1, True)
    
    def policy(self, scene_state: SceneState) -> str:

        if self.health<=0:
            if self.sprite_master.round_done:
                self.current_position= (-100, -100)
            return "death"
        
        return self.hit(scene_state) 
        
    def hit(self, scene_state: SceneState):
        if self.current_action in ["fight", "hit"]:
            if self.sprite_master.round_done:
                return "idle"
            elif 3.0 <= self.sprite_master.frame_index < 3.2:
                return "hit"
            else:
                return "fight"
        elif self.cal_distance2player(scene_state.get_player_pos()) < 50:
            return "fight"

    def copy(self):
        """
        Copy constructor
        """
        return Ghost(self.game_screen, self.current_position.copy())

