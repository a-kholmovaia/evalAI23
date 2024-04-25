import pygame
import random
from character import Character

class Enemy(Character):
    def __init__(self, game_screen, start_position, sprite_master, attack_prob = 10_000):
        super().__init__(sprite_master, game_screen, start_position)
        self.health = 100
        self.attack_prob = attack_prob


    def take_action(self, player_pos):
        # Randomly decide to attack or stay idle
        if self.cal_distance2player(player_pos):
            if random.randint(0, self.attack_prob) == 1:  # Adjust randomness as needed
                self.current_action = 'fight'
                self.fight_counter -= self.speed
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

    
    def cal_distance2player(self, player_position):
        # Simple collision detection (can be improved)
        distance = self.current_position.distance_to(player_position)
        return distance < 100  # Adjust threshold according to your game's scale
