import pygame
from masters.sprite_master import SpriteMaster
from characters.attack_info import AttackInfo

class Character():
    def __init__(self, 
                 sprite_master:SpriteMaster, game_screen, 
                 start_position: pygame.Vector2
                 ):
        # Pygame's screen
        self.game_screen = game_screen
        # Battle characteristics
        self.block_capacity = 10
        self.current_health = 100
        self.max_health = 100

        # Initialize an attack info object with default settings
        self.attack_info = AttackInfo(1, True)
        # Defaults
        self.game_screen = game_screen
        self.current_position = start_position
        self.frame_index = 0
        self.font = pygame.font.Font(None, 23)

        self.sprite_master = sprite_master
        self.current_action = 'idle'
        self.speed = self.sprite_master.animation_speed
        self.death_counter = len(self.sprite_master.death_images)
        self.fight_counter = len(self.sprite_master.attack_images)
        self.reflect = True
        self.size = 128

    def handle_damage(self, damage: int, canBeBlocked: bool):
        """
        Reduces Charater's health points taking into account whether the damage can be blocked
        Parameters:
        damage: int - amount of the damage points
        canBeBlocked: bool -  flag that indicates if the damage can be blocked
        """
        if self.current_action == "block" and canBeBlocked:
            damage_block_diff = damage - self.block_capacity
            damage = damage_block_diff if damage_block_diff > 0 else 0
        self.current_health -= damage

    def get_attack_info(self):
        return self.attack_info
    
    def get_health(self) -> int:
        """
        Maps the current health points to the scale from 0 to 100
        and returns that value
        """
        res = int((self.current_health * 100) / self.max_health)

        # If the HPs are less than or equal to 0, but the enemy is still dying
        # return 1 to avoid the premature end of the scene
        if res <= 0 and not self.current_action == "death":
            res = 1

        return res

    
    def draw_current_action(self):
        sprite = pygame.transform.scale(self.sprite_master.get_sprite_frame(self.current_action), (self.size, self.size))
        if self.reflect:
            sprite = pygame.transform.flip(sprite, True, False)
        self.game_screen.blit(sprite, self.current_position)
