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
        self.attack_info = AttackInfo(10, True)
    
    def policy(self, scene_state: SceneState) -> str:
        pass

    def copy(self):
        """
        Copy constructor
        """
        return Ghost(self.game_screen, self.current_position.copy())

