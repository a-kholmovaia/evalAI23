import pygame
from character import Character
from constants import DEAD_POS
class Player(Character):

    def __init__(self, game_screen, start_position, sprite_master, speed_factor=50, size=(86,86)):
        super().__init__(sprite_master)
        # Pygame's screen
        self.game_screen = game_screen

        # Player's start position on the screen
        self.current_position = start_position

        self.ground_level = start_position[1]

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
        self.width, self.height = size
        self.current_position_rect = pygame.Rect(self.current_position.x, self.current_position.y, self.width, self.height)
        self.standing = False
        self.speed_factor = speed_factor

    def take_action(self, keys):
        if self.current_action != "dead":
            self.__handle_control_input(keys)
            self.update_physics()
            self.draw_current_action()
    
    def __handle_control_input(self, keys):
        # Handle input
        if keys[pygame.K_LEFT] and self.current_position[0] > 0:
            self.current_position[0] -= self.speed * self.speed_factor
            self.current_action = 'walk'
            self.reflect = True
        elif keys[pygame.K_RIGHT] and self.current_position[0] < self.game_screen.get_width() - self.padding:
            self.current_position[0] += self.speed * self.speed_factor
            self.current_action = 'walk'
            self.reflect = False
        elif keys[pygame.K_SPACE]:
            self.current_action = 'fight'
        elif keys[pygame.K_UP] and not self.is_jumping:
            # Initiate jump only if the player is not already jumping
            self.is_jumping = True
            self.current_action = 'jump'
            self.jump_direction = (keys[pygame.K_LEFT], keys[pygame.K_RIGHT]) 
        else:
            if self.health > 10:
                self.current_action = 'idle'
            elif self.health > 0:
                self.current_action = 'hurt'
            elif self.health<=0 and self.death_counter>0:
                self.current_action = "death"
                self.current_position.y = self.ground_level
                self.death_counter -= self.speed
            else:
                self.current_action = "dead"
                self.current_position = DEAD_POS
        if self.is_jumping:
            self.__jump()
    
    def update_position(self):
        # Method to update the Rect based on the Vector2 position
        self.current_position_rect.x = self.current_position.x
        self.current_position_rect.y = self.current_position.y
    
    def update_physics(self):
        # Apply gravity if not jumping or after reaching the jump apex
        if (not self.is_jumping or self.jump_height <= 0) and not self.standing:
            self.velocity_y += self.gravity

        # Update position based on velocity
        self.current_position.y += self.velocity_y

        # Collision with ground
        if self.current_position.y >= self.ground_level:
            self.current_position.y = self.ground_level
            self.velocity_y = 0
            self.is_jumping = False  # Ensure jumping is reset when on the ground

        self.update_position()  # Keep Rect in sync


    def __jump(self):
        # Initiate jump only if not already jumping
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_speed  # Set an initial upward velocity

        # Update the jump height based on the current jump state
        if self.jump_height >= -10:
            neg = 1
            if self.jump_height < 0:
                neg = -1

            # Adjust vertical velocity based on jump progression
            self.velocity_y = -(self.jump_height ** 2) * 0.5 * neg
            self.jump_height -= 1

            # Horizontal movement during jump
            if self.jump_direction[0]:  # Left
                self.current_position.x -= self.speed
            elif self.jump_direction[1]:  # Right
                self.current_position.x += self.speed
        else:
            # Reset jump mechanics
            self.reset_jump()

    def reset_jump(self):
        self.is_jumping = False
        self.jump_height = 10
        self.jump_direction = (False, False)  # Reset direction after jump
        # Do not reset y position here; let gravity handle it to smooth out the landing

        


        