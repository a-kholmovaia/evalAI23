import pygame
from characters.enemy import Enemy
from characters.projectile import Projectile
from masters.first_boss_sprite_master import FirstBossSpriteMaster
from scenes.scene_state import SceneState


class Wizard(Enemy):

    def __init__(self, game_screen, start_position, projectile: Projectile):
        super().__init__(game_screen, start_position, FirstBossSpriteMaster("levels/test_levels/distant_attack/wizard", 
                            idle=3, walk=6, close_attack=5, distant_attack=5, 
                            hurt=2, death=5, block=0, start_action="idle"))
        
        # Inject the projectile the wizard will use and adjust its position
        self.projectile = projectile
        self.projectile.current_position[1] = self.current_position[1] + self.size * 0.2
        self.collision_distance = 90

        # Flag that indicates if the wizard has already shot
        self.has_shot = False

        self.size = 220

        # Cooldown time for attacks in milliseconds 
        self.attack_cooldown = 500

        # Elapsed time since last attack action
        self.elapsed_time = 0
    
    def policy(self, scene_state: SceneState) -> str:
        """
        Shoots once per preset time
        Dies when your health is less than or equal to 0
        """

        if self.health<=0 and self.death_counter>0:
            self.death_counter -= self.speed
            return "death"   
        
        if self.health <= 0 and self.death_counter <= 0:
            self.current_position = (-100, -100)
            return "death"

        if self.current_action in ["fight", "shoot"]:
            # If it's one of the hit frames and it hasn't fired yet then return "shoot" instead of "fight"
            if int(self.fight_counter) == len(self.sprite_master.attack_images) // 2 and not self.has_shot:
                self.fight_counter -= self.speed
                self.has_shot = True
                return "shoot"
            # If the attack animation isn't over yet then return "fight"
            if self.fight_counter > 0:
                self.fight_counter -= self.speed
                return "fight"
            # Otherwise return "idle"
            else:
                self.fight_counter = len(self.sprite_master.attack_images)
                self.elapsed_time = 0
                self.has_shot = False
                return "idle"
        # If the current action is "idle" 
        # then update the elapsed time and check if it's bigger than the cooldown time 
        else:
            self.elapsed_time += scene_state.get_elapsed_time()
            print(f"elapsed time = {self.elapsed_time}")
            # If the cooldown is over then return "fight" to begin a new attack
            # otherwise keep waiting
            if self.elapsed_time >= self.attack_cooldown:
                return "fight"
            else:
                print("I'm waiting")
                return "idle"
    
    def get_projectile(self):
        """
        Returns a copy of the injected projectile instance
        """
        return self.projectile.copy()
    
