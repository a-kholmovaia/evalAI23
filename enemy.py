import pygame
import random
from character import Character

class Enemy(Character):
    def __init__(self, game_screen, start_position, sprite_master):
        super().__init__(sprite_master)
        self.game_screen = game_screen
        self.current_position = start_position

        self.health = 100


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
        self.draw_current_action()

    

