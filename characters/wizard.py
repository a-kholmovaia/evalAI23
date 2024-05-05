import pygame
from characters.enemy import Enemy
from characters.projectile import Projectile
from masters.first_boss_sprite_master import FirstBossSpriteMaster
from scenes.scene_state import SceneState


class Wizard(Enemy):

    def __init__(self, game_screen, start_position, projectile: Projectile):
        super().__init__(game_screen, start_position, FirstBossSpriteMaster("levels/test_levels/distant_attack/wizard", 
                            idle=3, walk=6, close_attack=12, distant_attack=5, 
                            hurt=2, death=5, block=0, animation_speed=0.1, start_action="idle"))
        
        # Inject the projectile the wizard will use and adjust its position
        self.projectile = projectile
        self.projectile.current_position[1] = self.current_position[1] + self.size * 0.2
        
        self.size = 220

        self.collision_distance = 90

        # Flag indicating that the wizard has already passed the shooting phase
        self.shooting_phase_done = False 

        # Flag indicating that the wizard has already passed the close combat phase
        self.close_combat_phase_done = False 

        # Flag indicating that the wizard has already passed the weakness phase
        self.weakness_phase_done = False 

        # Flag indicating that the wizard has already passed the combat alert phase
        self.combat_alert_phase_done = False 

        # Duration of the shooting phase in milliseconds 
        self.shooting_duration = 5000

        # Duration of the close combat phase in milliseconds 
        self.close_combat_duration = 5000

        # Duration of the weakness phase in milliseconds 
        self.weakness_duration = 200

        # Duration of the combat alert phase in milliseconds 
        self.combat_alert_duration = 200

        # Flag that indicates if the wizard has already shot within his distant attack
        self.has_shot = False

        # Cooldown time for attacks in milliseconds 
        self.distant_attack_cooldown = 500

        # Elapsed time since last action
        self.elapsed_time = 0

        # Elapsed time since last shot
        self.shot_elapsed_time = 0

    def policy(self, scene_state: SceneState) -> str:
        """
        Has 4 phases of the fight: shooting, close combat, being weak, being alert
        """
        
        if self.health<=0:
            if self.sprite_master.round_done:
                self.current_position= (-100, -100)
            return "death"   
    
        self.elapsed_time += scene_state.get_elapsed_time()

        if not self.shooting_phase_done:
            if self.elapsed_time < self.shooting_duration:
                return self.fire(scene_state)
            else:
                self.shooting_phase_done = True
                self.elapsed_time = 0
        elif not self.close_combat_phase_done:
            if self.elapsed_time < self.close_combat_duration:
                return self.hit(scene_state)
            else:
                self.close_combat_phase_done = True
                self.elapsed_time = 0
        elif not self.weakness_phase_done:
            if self.elapsed_time < self.weakness_duration:
                return self.be_weak()
            else:
                self.weakness_phase_done = True
                self.elapsed_time = 0
        elif not self.combat_alert_phase_done:
            if self.elapsed_time < self.combat_alert_duration:
                return self.be_alert()
            else:
                self.combat_alert_phase_done = True
                self.elapsed_time = 0
        else:
            self.shooting_phase_done = False
            self.close_combat_phase_done = False
            self.weakness_phase_done = False
            self.combat_alert_phase_done = False
            self.elapsed_time = 0

        return "idle"
    
    def fire(self, scene_state: SceneState):
        
        if self.current_action in ["distant_fight", "shoot"]:
            # If it's one of the hit frames and it hasn't fired yet then return "shoot" instead of "fight"
            if 3.0 <= self.sprite_master.frame_index and not self.has_shot:
                self.has_shot = True
                return "shoot"
            # If the attack animation isn't over yet then return "fight"
            if not self.sprite_master.round_done:
                return "distant_fight"
            # Otherwise return "idle"
            else:
                self.shot_elapsed_time = 0
                self.has_shot = False
                return "idle"
        # If the current action is "idle" 
        # then update the elapsed time and check if it's bigger than the cooldown time 
        else:
            self.shot_elapsed_time += scene_state.get_elapsed_time()
            print(f"elapsed time = {self.shot_elapsed_time}")
            # If the cooldown is over then return "fight" to begin a new attack
            # otherwise keep waiting
            if self.shot_elapsed_time >= self.distant_attack_cooldown:
                return "distant_fight"
            else:
                return "idle"
            
    def hit(self, scene_state: SceneState):

        if self.current_action in ["close_fight", "hit"]:
            if self.sprite_master.round_done:
                return "idle"
            elif 8.0 <= self.sprite_master.frame_index <= 9.0:
                return "hit"
            else:
                return "close_fight"
        elif self.cal_distance2player(scene_state.get_player_pos()) < 100:
            return "close_fight"
    
    def be_weak(self):
        return "hurt"
    
    def be_alert(self):
        return "idle"


    def get_projectile(self):
        """
        Returns a copy of the injected projectile instance
        """
        return self.projectile.copy()
    
