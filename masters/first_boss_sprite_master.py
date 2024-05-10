import pygame
import os
from masters.sprite_master import SpriteMaster


class FirstBossSpriteMaster(SpriteMaster):
    """
    The first level boss's sprite master
    It extends the SpriteMaster by distinguishing between close attacks and distant attacks
    """

    def __init__(self, path, 
                 idle: int, walk:int, close_attack:int, 
                 distant_attack:int, hurt:int, death:int, 
                 block: int, animation_speed=0.1, start_action="idle"):
        super().__init__(path, idle=idle, walk=walk, attack=close_attack,
                         hurt=hurt, death=death, block=block, animation_speed=animation_speed, start_action=start_action)
        # Load images for different animations
        self.shoot_images = [pygame.image.load(os.path.join(path, f'shoot{i}.png')) for i in range(distant_attack)]
    
    def get_sprite_frame(self, action):
        self.round_done = False
        # Update animation based on action
        if action == 'idle':
            self.current_images = self.idle_images
        elif action == 'close_fight' or action == "hit":
            self.current_images = self.attack_images
        elif action == "distant_fight" or action == "shoot":
            self.current_images = self.shoot_images
        elif action == 'walk':
            self.current_images = self.walk_images
        elif action == 'hurt':
            self.current_images = self.hurt_images
        elif action == 'death' or action == "dying":
            self.current_images = self.death_images
        elif action == 'block':
            self.current_images = self.block_images
        

        # Update frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_images):
            self.frame_index = 0
            self.round_done = True

        # pick the correct frame
        frame = int(self.frame_index)
        self.image = self.current_images[frame]

        return self.image