import pygame

class SceneState:
    """
    Encapsulates all the necessary information about the current scene
    for the enemies' policies, in particular
    """
    def __init__(self, player_pos: pygame.math.Vector2):
        self.player_pos = player_pos
    
    def get_player_pos(self) -> pygame.math.Vector2:
        """
        Returns the player position as Vector2
        """
        return self.player_pos