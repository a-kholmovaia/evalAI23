import pygame

class Player:

    def __init__(self, game_screen, start_position, sprite_master, character_speed=5):
        # Pygame's screen
        self.game_screen = game_screen

        # Player's start position on the screen
        self.current_position = start_position

        # Player's default action
        self.current_action = 'idle_1'

        # Sprite master
        self.sprite_master = sprite_master

        # Define character speed
        self.character_speed = character_speed

        # Default frame index
        self.frame_index = 0


    def take_action(self, keys):
        
        self.__handle_control_input(keys)
        
        self.__draw_current_action()
    
    def __handle_control_input(self, keys):
        # Handle input
        if keys[pygame.K_UP]:
            self.current_position[1] -= self.character_speed
            self.current_action = 'move_up'
        elif keys[pygame.K_DOWN]:
            self.current_position[1] += self.character_speed
            self.current_action = 'move_down'
        elif keys[pygame.K_LEFT]:
            self.current_position[0] -= self.character_speed
            self.current_action = 'move_left'
        elif keys[pygame.K_RIGHT]:
            self.current_position[0] += self.character_speed
            self.current_action = 'move_right'
        elif keys[pygame.K_SPACE]:
            self.current_action = 'fight'
        else:
            self.current_action = 'idle_1'
    
    def __draw_current_action(self):
        # Draw current player's action on the game screen
        player_sprite = self.sprite_master.get_player_sprite_frame(self.current_action)
        print(f"current position is {self.current_position}")
        self.game_screen.blit(player_sprite, self.current_position)
    
        


        