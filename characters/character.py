import pygame
from masters.sprite_master import SpriteMaster
class Character():
    def __init__(self, 
                 sprite_master:SpriteMaster, game_screen, 
                 start_position: pygame.Vector2
                 ):
        # Pygame's screen
        self.game_screen = game_screen
        # Battle characteristics
        self.block_capacity = 10
        self.health = 100
        self.damage = 1
        # Defaults
        self.game_screen = game_screen
        self.current_position = start_position
        self.frame_index = 0

        self.sprite_master = sprite_master
        self.current_action = 'idle'
        self.speed = self.sprite_master.animation_speed
        self.death_counter = len(self.sprite_master.death_images)
        self.fight_counter = len(self.sprite_master.attack_images)
        self.reflect = True
        self.size = 128

    def handle_damage(self, damage: int):
        print(f"handle_damage() entered with damage {damage}")
        if self.current_action == "block":
            damage_block_diff = damage - self.block_capacity
            damage = damage_block_diff if damage_block_diff > 0 else 0
        self.health -= damage

    def get_damage(self):
        return self.damage
    
    def draw_current_action(self):
        sprite = pygame.transform.scale(self.sprite_master.get_sprite_frame(self.current_action), (self.size, self.size))
        if self.reflect:
            sprite = pygame.transform.flip(sprite, True, False)
        self.game_screen.blit(sprite, self.current_position)
