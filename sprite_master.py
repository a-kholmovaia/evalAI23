import pygame

class SpriteMaster:

    def __init__(self, actions_frames: dict, player_sprite_sheet_path : str, player_sprite_width : int, player_sprite_height : int, animation_speed=0.2):
        # Load character sprites
        self.player_sprite_sheet = pygame.image.load(player_sprite_sheet_path).convert_alpha()
        # Set player's sprite height and width
        self.player_sprite_height = player_sprite_height
        self.player_sprite_width = player_sprite_width

        # Default frame index
        self.frame_index = 0

        # Adjust as necessary for smooth animation
        self.animation_speed = animation_speed
        # Map sheet rows to actions
        self.player_actions = actions_frames

    
    def get_sprite_frame(self, action):
        """Extracts and returns a specific frame from the sprite sheet."""

        # Update frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= self.player_actions[action]['frames']:
            self.frame_index = 0

        frame = int(self.frame_index)
        row = self.player_actions[action]['row']
        y = row * self.player_sprite_height
        x = frame * self.player_sprite_width
        return self.player_sprite_sheet.subsurface(pygame.Rect(x, y, self.player_sprite_width, self.player_sprite_height))
    