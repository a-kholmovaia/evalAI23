import pygame
import random
class Enemy:
    def __init__(self, game_screen, start_position, sprite_master, character_speed=2):
        self.game_screen = game_screen
        self.current_position = start_position
        self.sprite_master = sprite_master
        self.character_speed = character_speed
        self.current_action = 'idle'
        self.health = 100

    def take_action(self):
        if self.health <= 0:
            self.current_position = (-100, -100)
        # Randomly decide to attack or stay idle
        if random.randint(0, 100) == 1:  # Adjust randomness as needed
            self.current_action = 'fight'
        else:
            self.current_action = 'idle'
        self.__draw_current_action()

    def __draw_current_action(self):
        enemy_sprite = pygame.transform.scale(self.sprite_master.get_sprite_frame(self.current_action), (86, 86))
        self.game_screen.blit(enemy_sprite, self.current_position)

