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

        self.health = 100
        # New attributes for jumping
        self.is_jumping = False
        self.jump_speed = 10
        self.jump_height = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.ground_level = start_position[1]
        self.initial_position_y = start_position[1]
        self.padding = self.game_screen.get_width()*0.1
        self.reflect = False


    def take_action(self, keys):
        self.__handle_control_input(keys)
        self.__draw_current_action()
    
    def __handle_control_input(self, keys):
        # Handle input
        if keys[pygame.K_LEFT] and self.current_position[0] > 0:
            self.current_position[0] -= self.character_speed
            self.current_action = 'move_left'
            self.reflect = True
        elif keys[pygame.K_RIGHT] and self.current_position[0] < self.game_screen.get_width() - self.padding:
            self.current_position[0] += self.character_speed
            self.current_action = 'move_right'
            self.reflect = False
        elif keys[pygame.K_SPACE]:
            self.current_action = 'fight'
        elif keys[pygame.K_UP] and not self.is_jumping:
            # Initiate jump only if the player is not already jumping
            self.is_jumping = True
            self.current_action = 'jump'
            self.jump_direction = (keys[pygame.K_LEFT], keys[pygame.K_RIGHT]) 
        else:
            self.current_action = 'idle_1'

        if self.is_jumping:
            self.__jump()

    def __jump(self):
        # Calculate vertical jump
        if self.jump_height >= -10:
            neg = 1
            if self.jump_height < 0:
                neg = -1
            # Vertical jump mechanics
            self.current_position.y -= (self.jump_height ** 2) * 0.5 * neg
            self.jump_height -= 1

            # Horizontal movement during jump
            if self.jump_direction[0]:  # Left
                self.current_position.x -= self.character_speed
            elif self.jump_direction[1]:  # Right
                self.current_position.x += self.character_speed

        else:  # Reset jump
            self.is_jumping = False
            self.jump_height = 10
            self.current_position.y = self.initial_position_y  # Reset to initial y position
            self.jump_direction = (False, False)  # Reset direction after jump
    
    def __draw_current_action(self):
        # Draw current player's action on the game screen
        player_sprite = pygame.transform.scale(
            self.sprite_master.get_sprite_frame(self.current_action), 
            (86, 86))
        if self.reflect:
            player_sprite = pygame.transform.flip(player_sprite, True, False)
        self.game_screen.blit(player_sprite, self.current_position)
    
        


        