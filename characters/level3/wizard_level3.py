from characters.enemy import Enemy
from characters.level1.projectile_level1 import Projectile
from characters.attack_info import AttackInfo
from masters.second_boss_sprite_master import SecondBossSpriteMaster
from scenes.scene_state import SceneState


class ThirdBoss(Enemy):

    def __init__(self, game_screen, start_position, projectile: Projectile, summoned_enemy: Enemy):
        super().__init__(game_screen, start_position, SecondBossSpriteMaster("levels/level3/wizard", 
                            idle=3, walk=6, close_attack=6, distant_attack=5, summoning=5, 
                            hurt=2, death=6, block=0, start_action="idle"))
        
       # Inject the projectile the wizard will use and adjust its position
        self.projectile = projectile
        self.projectile.current_position[1] = self.current_position[1] + self.size * 0.2

        # Inject the enemy the wizard will summon
        self.summoned_enemy = summoned_enemy


        self.attack_info = AttackInfo(3, True)
        self.collision_distance = 100
        self.size = 220

        self.max_health = 500
        self.current_health = self.max_health

        # Flag indicating that the wizard has already passed the summoning phase
        self.summoning_phase_done = False

        # Flag indicating that the wizard has already passed the shooting phase
        self.shooting_phase_done = False 

        # Flag indicating that the wizard has already passed the close combat phase
        self.close_combat_phase_done = False 

        # Duration of the summoning phase in milliseconds 
        self.summoning_duration = 1500

        # Duration of the shooting phase in milliseconds 
        self.shooting_duration = 7000

        # Duration of the close combat phase in milliseconds 
        self.close_combat_duration = 5000

        # Flag that indicates if the wizard has already shot within his distant attack
        self.has_shot = False

        # Cooldown time for attacks in milliseconds 
        self.distant_attack_cooldown = 800

        # Elapsed time since last action
        self.elapsed_time = 0

        # Elapsed time since last shot
        self.shot_elapsed_time = 0

        # Flag that indicates if the wizard has already summoned within his summoning_phase
        self.has_summoned = False
    
    
    def policy(self, scene_state: SceneState) -> str:
        """
        Has 4 phases of the fight: shooting, close combat, summoning
        """
        
        if self.current_health<=0:
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
        elif not self.summoning_phase_done:
            if self.elapsed_time < self.summoning_duration:
                return self.summon()
            else:
                self.summoning_phase_done = True
                self.elapsed_time = 0
                # The flag must be set on False here because there must be only one summoned creature during the phase
                self.has_summoned = False
        else:
            self.shooting_phase_done = False
            self.close_combat_phase_done = False
            self.summoning_phase_done = False
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
            elif 4.0 <= self.sprite_master.frame_index <= 5.0:
                return "hit"
            else:
                return "close_fight"
        elif self.cal_distance2player(scene_state.get_player_pos()) < 100:
            return "close_fight"
    
    def be_weak(self):
        return "hurt"
    
    def be_alert(self):
        return "idle"
    
    def summon(self):

        if self.current_action in ["summon", "commit_summoning"]:

            if 3.0 <= self.sprite_master.frame_index and not self.has_summoned:
                self.has_summoned = True
                return "commit_summoning"
            if not self.sprite_master.round_done:
                return "summon"
            else:
                return "idle"
        else:
            if self.has_summoned:
                return "idle"
            else:
                return "summon"
        
    
    def get_projectile(self):
        """
        Returns a copy of the injected projectile instance
        """
        projectile = self.projectile.copy()
        projectile.current_position = self.current_position.copy()
        return projectile
    
    def get_summoned_creature(self):
        """
        Returns a copy of the injected enemy instance
        """
        return self.summoned_enemy.copy()

