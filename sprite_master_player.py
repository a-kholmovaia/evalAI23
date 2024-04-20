import pygame

class SpriteMasterPlayer:
    SPRITE_PATH = "img/player_sheet.png"
    def __init__(self, actions_to_rows : dict, frame_width : int, frame_height : int, animation_speed=0.2):
        # Load sprite
        self.sprite_sheet = pygame.image.load(self.SPRITE_PATH).convert_alpha()

        # Set player's sprite height and width
        self.frame_height = frame_height
        self.frame_width = frame_width

        # Default frame index
        self.frame_index = 0

        # Adjust as necessary for smooth animation
        self.animation_speed = animation_speed

        # Set specific actions_to_rows dict
        self.actions_to_rows = actions_to_rows

    
    def get_sprite_frame(self, action):
        """Extracts and returns a specific frame from the sprite sheet."""

        # Update frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= self.actions_to_rows[action]['frames']:
            self.frame_index = 0

        # Cut the frame out of the png sheet
        frame = int(self.frame_index)
        row = self.actions_to_rows[action]['row']
        y = row * self.frame_height
        x = frame * self.frame_width
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
    