from characters.enemy import Enemy
from characters.projectile import Projectile
from masters.sprite_master import SpriteMaster
from scenes.scene_state import SceneState


class Wizard(Enemy):

    def __init__(self, game_screen, start_position, projectile: Projectile):
        super().__init__(game_screen, start_position, SpriteMaster("levels/test_levels/distant_attack/wizard", 
                            idle=3, walk=5, attack=4, 
                            hurt=2, death=5, block=0, start_action="idle"))
        
        # Inject the projectile the wizard will use
        self.projectile = projectile

        # The flag that indicates if the wizard has already shot
        self.has_shot = False
    
    def policy(self, scene_state: SceneState) -> str:
        """
        Shoots once and then waits
        """
        
        # If it's the hitting frame then set the current action on "hit" instead of "fight"
        if self.current_action == "fight" and int(self.fight_counter) == len(self.sprite_master.attack_images) // 2:
            self.fight_counter -= self.speed
            return "shoot"
        
        # If it has been "fight" or "hit", the attack frames have left yet and it's currently not the hitting frame 
        # then return "fight"
        if (self.current_action == "fight" or self.current_action == "shoot") and self.fight_counter > 0:
            self.fight_counter -= self.speed
            return "fight"
        
        # If the wizard hasn't shot already  
        # then set the current action on "fight" and the flag has_shot on True
        if not self.has_shot:
            self.fight_counter = len(self.sprite_master.attack_images)
            self.has_shot = True
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
    
    def get_projectile(self):
        """
        Returns a copy of the injected projectile instance
        """
        return self.projectile.copy()
    
