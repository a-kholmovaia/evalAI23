from characters.enemy import Enemy
from characters.attack_info import AttackInfo
from scenes.scene_state import SceneState
from masters.sprite_master import SpriteMaster
import pygame
import random
class Projectile(Enemy):
    def __init__(self, game_screen, start_position):
        super().__init__(game_screen, start_position, SpriteMaster("levels/level3/projectile", 
                              idle=0, walk=0, attack=4, 
                              hurt=0, death=3, block=0, start_action="hit"))
        self.current_action = "hit"
        self.attack_info = AttackInfo(10, False)
        self.speed = 3
        self.collision_distance = 80
        self.current_position[1] += 20
        self.text = self.get_text_projectile()
        self.font = pygame.font.Font(None, 23)

        # Initialize the target for the projectile with None value
        # Must be set when first time entering policy
        self.target_vec = None

        # Initialize the elapsed life time in milliseconds
        self.elapsed_time = 0

        # Set the life time in milliseconds
        self.life_time = 2700

    def policy(self, scene_state: SceneState) -> str:
        """
        Moves left and attacks constantly
        """

        # Update the elapsed time
        self.elapsed_time += scene_state.elapsed_time

        if self.target_vec == None:
            self.target_vec = scene_state.get_player_pos().copy()

        if self.cal_distance2player(scene_state.get_player_pos()) < self.collision_distance:
            self.current_health = 0

        if self.current_health<=0 or self.current_position[0] < 0:
            if self.sprite_master.round_done:
                self.current_position= pygame.Vector2((-100, -100))
                return "death"
            return "death" 
        

        player_x, player_y = scene_state.get_player_pos()
        self.move_to_target(player_x, player_y)

        return "hit"
    
    def move_to_target(self, target_x: float, target_y: float):
        """
        Moves the projectile towards a target position and sets its health to 0 if close enough.
        """
        projectile_x, projectile_y = self.current_position[0], self.current_position[1]

        vector_x = target_x - projectile_x
        vector_y = target_y - projectile_y

        # Calculate the distance to the target using the Euclidean distance
        distance = (vector_x ** 2 + vector_y ** 2) ** 0.5
    
        # Normalize the vector (make it unit length)
        if distance != 0:
            unit_vector_x = vector_x / distance
            unit_vector_y = vector_y / distance
        else:
            unit_vector_x, unit_vector_y = 0, 0

        # Move the projectile by its speed along the unit vector towards the target
        self.current_position[0] += unit_vector_x * self.speed
        self.current_position[1] += unit_vector_y * self.speed
    
        # Check if the projectile is close enough to the target to consider it a "hit"
        if self.life_time < self.elapsed_time:
            self.current_health = 0  # Set health to 0 to indicate the projectile should be destroyed or removed



    def copy(self):
        """
        Copy constructor
        """
        return Projectile(self.game_screen, self.current_position.copy())
    
    def draw_current_action(self):
        text = self.text
        rendered_text = self.font.render(text, True, (255,0,0))
        sprite = pygame.transform.scale(self.sprite_master.get_sprite_frame(self.current_action), (self.size, self.size))
        if self.reflect:
            sprite = pygame.transform.flip(sprite, True, False)
        self.game_screen.blit(sprite, self.current_position)
        self.game_screen.blit(rendered_text, (self.current_position[0], self.current_position[1]+30))


    def get_text_projectile(self):
        texts = ['…approaching deadline…',"…I’m on vacation…", 
                 '…last-minute changes…','…lost the source code…', '…zoom meeting at 8 AM…',
                 '…group chat exploded…', '…buggy software…', "…model overfitting…",
                 "…misaligned objectives…", "…missing deadlines…", "…motivation draining…", "…unresolved merge conflicts…"]
        return random.choice(texts)



