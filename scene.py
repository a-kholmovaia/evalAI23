import pygame
from sprite_master import SpriteMaster
from player import Player
from enemy import Enemy
from constants import BLACK
from typing import List
from window import Window
from event_handler import EventHandler

class Scene:

    def __init__(self, event_handler: EventHandler, scene_path : str, player_sheet_path : str,  window : Window, clock : pygame.time.Clock, font : pygame.font.Font, FPS=60):
        
        self.event_handler = event_handler


        # Set window
        self.window = window

        # Parse and set up pre-written configurations
        config = self.__parse_config(scene_path + "config.txt")
        for key in config.keys():
            if key == "player_start_pos":
                self.player_pos = config[key]
            elif key == "enemy_start_pos":
                self.enemy_pos = config[key]
        

        # Set frame rate and clock
        self.FPS = FPS
        self.clock = clock

        # Set scene path
        self.scene_path = scene_path

        # Set font
        self.font = font

        self.player = self.__get_player(player_sheet_path)

        #List[DrawableObject] to draw when resizing window
        self.drawable_objects = [] 

        
    def run(self):
        while self.event_handler.listen_events():
            self.run_scenario()
        
    def run_scenario(self):
        #Abstract method to be overriden in subclasses
        pass
        
    

    def __parse_config(self, file_path : str):

        #Initialize parsed config string to value dictionary
        config_values = {
            "default_player_pos" : pygame.Vector2(self.window.get_width()*0.25, self.window.get_height() * 0.7),
            "default_enemy_pos" : pygame.Vector2(self.window.get_width()*0.8, self.window.get_height() * 0.65)
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

        return Player(self.window.get_screen(), self.player_pos, SpriteMaster(actions_dict, sheet_path, 32, 32))

    def __get_enemy(self, sheet_path : str) -> List[Enemy]:
        pass
   
    def __detect_collision(self, position1, position2):
        pass
    
    def __resize_scene(self):
        for o in self.drawable_objects:
            o.draw()
