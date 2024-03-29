import pygame
from sprite_master import SpriteMaster
from player import Player
from enemy import Enemy
from constants import BLACK
from typing import List

class Scene:

    def __init__(self, scene_path : str, player_sheet_path : str, enemy_sheet_path : str, game_screen : pygame.Surface, clock : pygame.time.Clock, font : pygame.font.Font, FPS=60):
        
        # Set current game screen
        self.game_screen = game_screen

        # Initialize enemy counter with zero
        self.enemy_counter = 0

        # Initialize characters list
        self.chars = []

        # Parse and set up pre-written configurations
        config = self.__parse_config(scene_path + "config.txt")
        for key in config.keys():
            if key == "player_start_pos":
                self.player_pos = config[key]
            elif key == "enemy_start_pos":
                self.enemy_pos = config[key]
                self.enemy_counter += 1
        
        # Draw background
        self.background = pygame.transform.scale(pygame.image.load(scene_path + "background0.png"),
                                                 (self.game_screen.get_width(), self.game_screen.get_height()))
        self.background_text = pygame.transform.scale(pygame.image.load(scene_path + "back_text.png"), (280, 140))
        self.background_health = pygame.transform.scale(pygame.image.load(scene_path + "back_text.png"), (240, 80))

        # Set characters
        # To do: make out of that one method __set_char (player and enemy classes should be changed, maybe they should have the same parent)
        self.player = self.__get_player(player_sheet_path)
        self.enemies = self.__get_enemies(enemy_sheet_path)

        # Set frame rate and clock
        self.FPS = FPS
        self.clock = clock

        # Set font
        self.font = font

                
        

    def run(self):
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.game_screen.fill(BLACK)
            self.game_screen.blit(self.background, (0, 0))

            keys = pygame.key.get_pressed()
            self.player.take_action(keys)
            for enemy in self.enemies:
                enemy.take_action()

                if enemy.current_action == 'fight' and self.__detect_collision(self.player.current_position, enemy.current_position):
                    self.player.health -= 1  # Reduce player health by 5 points
                if self.player.current_action == 'fight' and self.__detect_collision(self.player.current_position, enemy.current_position):
                    enemy.health -= 1 # Reduce player health by 5 points

                self.__draw_health_bars(self.player.health, enemy.health)
            
            self.__draw_instructions()

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def __parse_config(self, file_path : str):

        #Initialize parsed config string to value dictionary
        config_values = {
            "default_player_pos" : pygame.Vector2(self.game_screen.get_width() / 5, self.game_screen.get_height() * 0.7),
            "default_enemy_pos" : pygame.Vector2(self.game_screen.get_width(), self.game_screen.get_height() * 0.7)
        } 

        # Initialize an empty dictionary to store the key-value pairs
        config = {}

        # Open the text file in read mode
        with open(file_path, 'r') as file:
            # Read the file line by line
            for line in file:
                # Strip leading and trailing whitespace
                stripped_line = line.strip()
                # If the line is not empty and does not start with '#', process it
                if stripped_line and not stripped_line.startswith('#'):
                    # Split the line into two parts at the '=' character
                    key, value = stripped_line.split('=')
                    # Add the key-value pair to the dictionary
                    config[key] = config_values[value]

        # Return the dictionary containing the configurations
        return config        


    def __get_player(self, sheet_path : str) -> Player:

        actions_dict = {
            'idle_1': {'row': 0, 'frames': 2},
            'idle_2': {'row': 0, 'frames': 2},
            'move_up': {'row': 3, 'frames': 8},
            'move_down': {'row': 3, 'frames': 8},
            'move_left': {'row': 3, 'frames': 8},
            'move_right': {'row': 3, 'frames': 8},
            'jump': {'row': 5, 'frames': 8},
            'fight': {'row': 8, 'frames': 8},
        }

        return Player(self.game_screen, self.player_pos, SpriteMaster(actions_dict, sheet_path, 32, 32))

    def __get_enemies(self, sheet_path : str) -> List[Enemy]:

        actions_dict = {
            'idle': {'row': 0, 'frames': 4},
            'fight': {'row': 1, 'frames': 4},
        }
        
        return [Enemy(self.game_screen, self.enemy_pos, SpriteMaster(actions_dict, sheet_path, 32, 32, animation_speed=0.01))]

    def __draw_health_bars(self, player_health, enemy_health):
        max_health_width = 200  # Width of the health bar at full health
        health_bar_height = 20
        border_padding = 15

        # Player health bar
        self.game_screen.blit(self.background_health, (0, 0))
        pygame.draw.rect(self.game_screen, (255, 0, 0),
                         (border_padding, border_padding, max_health_width, health_bar_height))
        pygame.draw.rect(self.game_screen, (0, 255, 0), (border_padding, border_padding, player_health*2, health_bar_height))
        your_health = self.font.render("  your  health", True, BLACK)
        self.game_screen.blit(your_health, (border_padding, border_padding + 5 + health_bar_height))
        # Enemy health bar
        self.game_screen.blit(self.background_health, (self.game_screen.get_width()-240, 0))
        pygame.draw.rect(self.game_screen, (255, 0, 0), (
        self.game_screen.get_width() - max_health_width - border_padding, border_padding, max_health_width, health_bar_height))
        pygame.draw.rect(self.game_screen, (0, 255, 0), (
        self.game_screen.get_width() - max_health_width - border_padding, border_padding, enemy_health*2, health_bar_height))

        enemys_health = self.font.render("enemy  health", True, BLACK)
        self.game_screen.blit(enemys_health, (self.game_screen.get_width() - 13*border_padding, border_padding  + 5 + health_bar_height))

    def __draw_instructions(self):
        border_padding = 35
        instructions1 = self.font.render("use  LEFT  RIGHT  UP", True, BLACK)
        instructions2 = self.font.render("arrow  to  move", True, BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, BLACK)
        self.game_screen.blit(self.background_text,
                         (border_padding-20, border_padding * 2 + 30))

        self.game_screen.blit(instructions1, (border_padding, border_padding * 2 + 45))
        self.game_screen.blit(instructions2, (border_padding, border_padding * 2 + 85))
        self.game_screen.blit(instructions3, (border_padding, border_padding * 2 + 120))

    def __detect_collision(self, position1, position2):
        # Simple collision detection (can be improved)
        distance = position1.distance_to(position2)
        return distance < 50  # Adjust threshold according to your game's scale