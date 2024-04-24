import pygame
from sprite_master import SpriteMaster
from player import Player
from enemy import Enemy
from constants import BLACK, BACK_TEXT_PATH, GREEN
from typing import List, Optional, Literal
import constants



class Scene:
    def __init__(self, scene_path : str,  game_screen : pygame.Surface, clock : pygame.time.Clock, font : pygame.font.Font, FPS=60):
        
        # Set the flag to continue the game loop
        self.do_continue_game_loop = True

        # Set current game screen
        self.game_screen = game_screen

        # Parse and set up pre-written configurations
        config = self.__parse_config(scene_path + "config.txt")
        for key in config.keys():
            if key == "player_start_pos":
                self.player_pos = config[key]
            elif key == "enemy_start_pos":
                self.enemy_pos = config[key]
        
        self.background_text = pygame.transform.scale(pygame.image.load(BACK_TEXT_PATH), (240, 80))
        self.pause_img = pygame.image.load("img/pause.png")

        self.background_text_instruction = pygame.transform.scale(self.background_text, (280, 140))

        # Set frame rate and clock
        self.FPS = FPS
        self.clock = clock

        # Set scene path
        self.scene_path = scene_path

        # Set font
        self.font = font

        self.player = self.get_player()

        self.continue_button_rect = pygame.Rect(self.game_screen.get_width() * 0.58 , 
                                                self.game_screen.get_height() * 0.58, 120, 40)
        
        self.platforms = []

        self.intro = True
        self.done = False

        
    def run(self):
        pass
    

    def __parse_config(self, file_path : str):

        #Initialize parsed config string to value dictionary
        config_values = {
            "default_player_pos" : pygame.Vector2(self.game_screen.get_width()*0.25, self.game_screen.get_height() * 0.66),
            "default_enemy_pos" : pygame.Vector2(self.game_screen.get_width()*0.8, self.game_screen.get_height() * 0.66)
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


    def get_player(self) -> Player:
        sprite = SpriteMaster("levels/player", idle=2, walk=6, attack=4, hurt=4, death=10)
        return Player(self.game_screen, self.player_pos, sprite)

    def draw_health_bars(self, player_health, enemy_health):
        # draws health bars on the top of a screen
        max_health_width = 200  # Width of the health bar at full health
        health_bar_height = 20
        border_padding = 15

        # Player health bar
        self.game_screen.blit(self.background_text, (0, 0))
        pygame.draw.rect(self.game_screen, (255, 0, 0),
                         (border_padding, border_padding, max_health_width, health_bar_height))
        pygame.draw.rect(self.game_screen, (0, 255, 0), (border_padding, border_padding, player_health*2, health_bar_height))
        your_health = self.font.render("  your  health", True, BLACK)
        self.game_screen.blit(your_health, (border_padding, border_padding + 5 + health_bar_height))
        # Enemy health bar
        self.game_screen.blit(self.background_text, (self.game_screen.get_width()-240, 0))
        pygame.draw.rect(self.game_screen, (255, 0, 0), (
        self.game_screen.get_width() - max_health_width - border_padding, border_padding, max_health_width, health_bar_height))
        pygame.draw.rect(self.game_screen, (0, 255, 0), (
        self.game_screen.get_width() - max_health_width - border_padding, border_padding, enemy_health*2, health_bar_height))

        enemys_health = self.font.render("enemy  health", True, BLACK)
        self.game_screen.blit(enemys_health, (self.game_screen.get_width() - 13*border_padding, border_padding  + 5 + health_bar_height))

   
    def battle_info(self, text:str):
            text = self.font.render(text, True, GREEN)
            self.draw_widget()
            self.game_screen.blit(text,
                         (self.game_screen.get_width()//2.1, self.game_screen.get_height()//2))
            
    def draw_pause_screen(self):
        pause_img = pygame.transform.scale(self.pause_img, (100, 30))
        self.draw_widget()
        self.game_screen.blit(pause_img,
                         (self.game_screen.get_width()//2.1, self.game_screen.get_height()//2))

    def draw_widget(self):
        self.background_text_info = pygame.transform.scale(self.background_text, (300, 150))
        self.game_screen.blit(self.background_text_info,
                         (self.game_screen.get_width()//2.5, self.game_screen.get_height()//2.3))
        self.draw_continue_button()

    def draw_instructions(self):
        border_padding = 35
        instructions1 = self.font.render("use  LEFT  RIGHT  UP", True, BLACK)
        instructions2 = self.font.render("arrow  to  move", True, BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, BLACK)
        self.game_screen.blit(self.background_text_instruction,
                         (border_padding-20, border_padding * 2 + 30))

        self.game_screen.blit(instructions1, (border_padding, border_padding * 2 + 45))
        self.game_screen.blit(instructions2, (border_padding, border_padding * 2 + 85))
        self.game_screen.blit(instructions3, (border_padding, border_padding * 2 + 120))    

    def detect_collision(self, position1, position2):
        # Simple collision detection (can be improved)
        distance = position1.distance_to(position2)
        return distance < 70  # Adjust threshold according to your game's scale
    
    def handle_platform_collisions(self):
        # Create a Rect for collision detection based on current Vector2 position
        player_rect = self.player.current_position_rect

        for platform in self.platforms:
            if player_rect.colliderect(platform[1]):  # Assuming each platform is stored as (image, rect)
                # Collision detected, adjust player position if falling down
                if self.player.velocity_y > 0:
                    self.standing = True
                    player_rect.bottom = platform[1].top
                    self.player.current_position.y = player_rect.top  # Correcting the assignment here

                    self.player.velocity_y = 0
                    self.player.is_jumping = False
                    break  # Break after handling collision to avoid multiple conflicting adjustments

        # Update the player's position Rectangle for continued accurate collision detection
        self.player.current_position_rect = player_rect
    
    def draw_platforms(self):
        if len(self.platforms) != 0:
            for img, rect in self.platforms:
                self.game_screen.blit(img, rect)

    def draw_continue_button(self):
        continue_surface = self.font.render('Continue', True, (255, 255, 255))
        pygame.draw.rect(self.game_screen, (0, 128, 0), self.continue_button_rect)  # Green button
        self.game_screen.blit(continue_surface, (self.continue_button_rect.x + 10, self.continue_button_rect.y+10))

    
    def handle_fight_collisions(self, object: Literal["player", "enemy"]):
        if object=="player":
            object = self.enemy
            subject = self.player
        else: 
            subject = self.enemy
            object = self.player
        
        if subject.current_action == 'fight' and self.detect_collision(object.current_position, subject.current_position):
            object.handle_damage(subject.get_damage()) # damage: int 
    
    def handle_collisions(self): 
        self.handle_platform_collisions()
        self.handle_fight_collisions("player")
        self.handle_fight_collisions("enemy")
    


    def event_end_game_loop(self):
        print("Quit event succesfully handled")
        self.do_continue_game_loop = False

    def listen_events(self):
        if self.intro:
            self.battle_info("Defeat the enemy!")
        if self.enemy.health <= 0: 
            self.battle_info("You   won!")
            self.done = True
        elif self.player.health <= 0: 
            self.battle_info("You  lose!")

        for event in pygame.event.get():
            print(f"event of the type {event.type} was fired")
            if event.type == pygame.QUIT:
                self.done = True
                self.event_end_game_loop()
            elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = True
                        self.set_game_on_pause()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button_rect.collidepoint(event.pos):
                    if self.intro:
                        self.intro = False
                    if (self.enemy.health <= 0 or self.player.health <= 0):
                        self.event_end_game_loop() 

    def set_game_on_pause(self):
        self.draw_pause_screen()
        pygame.display.flip()
        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.continue_button_rect.collidepoint(event.pos):
                            self.pause = False

    def draw_scene(self):
        self.game_screen.fill(BLACK)
        self.game_screen.blit(self.background, (0, 0))
        self.draw_platforms() 
        
        