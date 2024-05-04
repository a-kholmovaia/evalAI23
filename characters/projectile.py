from characters.enemy import Enemy
from scenes.scene_state import SceneState
from masters.sprite_master import SpriteMaster

class Projectile(Enemy):
    def __init__(self, game_screen, start_position):
        super().__init__(game_screen, start_position, SpriteMaster("levels/test_levels/distant_attack/projectile", 
                              idle=0, walk=0, attack=4, 
                              hurt=0, death=3, block=0, start_action="hit"))
        self.current_action = "hit"
        self.damage = 10
        self.speed = 0.5

    def policy(self, scene_state: SceneState) -> str:
        """
        Moves left and attacks constantly
        """

        if self.cal_distance2player(scene_state.get_player_pos()) < 50:
            self.health = 0

        if self.health<=0 and self.death_counter>0:
            self.death_counter -= self.speed
            return "death"   
        
        if self.health <= 0 and self.death_counter <= 0:
            self.current_position = (-100, -100)
            return "death"
        
        self.current_position[0] -= self.speed 
        return "hit"

    def copy(self):
        """
        Copy constructor
        """
        return Projectile(self.game_screen, self.current_position)

