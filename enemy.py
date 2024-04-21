import pygame
import random
from character import Character

class Enemy(Character):
    def __init__(self, game_screen, start_position, sprite_master):
        super().__init__()
        self.game_screen = game_screen
        self.current_position = start_position
        self.sprite_master = sprite_master
        self.speed = self.sprite_master.animation_speed
        self.current_action = 'idle'
        self.health = 100
        self.death_counter = len(self.sprite_master.death_images)
        self.fight_counter = len(self.sprite_master.attack_images)


    def take_action(self):
        # Randomly decide to attack or stay idle
        if self.current_action=="fight" or random.randint(0, 10) == 1:  # Adjust randomness as needed
            self.current_action = 'fight'
            self.fight_counter -= self.speed
            if self.fight_counter <= 0:
                self.fight_counter = len(self.sprite_master.attack_images)
                self.current_action="idle"
        elif self.health<=0 and self.death_counter>0:
            self.current_action = "death"
            self.death_counter -= self.speed     
        else:
            if self.health > 10:
                self.current_action = 'idle'
            else:
                self.current_action = 'hurt'
        if self.health<=0 and self.death_counter<=0:
            self.current_position = (-100, -100)
        self.__draw_current_action()

    def __draw_current_action(self):
        enemy_sprite = pygame.transform.scale(self.sprite_master.get_sprite_frame(self.current_action), (128, 128))
        enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
        self.game_screen.blit(enemy_sprite, self.current_position)

