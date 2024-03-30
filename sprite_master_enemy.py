import pygame
import os

class EnemySprite:
    def __init__(self, path, idle: int, walk:int, attack:int, hurt:int, death:int, animation_speed=0.1):
        # Load images for different animations
        self.idle_images = [pygame.image.load(os.path.join(path, f'idle{i}.png')) for i in range(idle)]
        self.attack_images = [pygame.image.load(os.path.join(path, f'attack{i}.png')) for i in range(attack)]
        self.walk_images = [pygame.image.load(os.path.join(path, f'walk{i}.png')) for i in range(walk)]
        self.hurt_images = [pygame.image.load(os.path.join(path, f'hurt{i}.png')) for i in range(hurt)]
        self.death_images = [pygame.image.load(os.path.join(path, f'death{i}.png')) for i in range(death)]

        self.animation_speed = animation_speed
        # Default frame index
        self.frame_index = 0
        self.image = self.get_sprite_frame("idle")

    def get_sprite_frame(self, action):
        # Update animation based on action
        if action == 'idle':
            self.current_images = self.idle_images
        elif action == 'fight':
            self.current_images = self.attack_images
        elif action == 'walk':
            self.current_images = self.walk_images
        elif action == 'hurt':
            self.current_images = self.hurt_images
        elif action == 'death':
            self.current_images = self.death_images
        

        # Update frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.current_images):
            self.frame_index = 0

        # pick the correct frame
        frame = int(self.frame_index)
        self.image = self.current_images[frame]

        return self.image

