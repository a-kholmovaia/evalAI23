import pygame

class SceneState:
    """
    Encapsulates all the necessary information about the current scene
    for the enemies' policies, in particular
    """
    def __init__(self, player_pos: pygame.math.Vector2, elapsed_time: int):
        self.player_pos = player_pos
        self.elapsed_time = elapsed_time
    
    def get_player_pos(self) -> pygame.math.Vector2:
        """
        Returns the player position as Vector2
        """
        return self.player_pos
    
    def get_elapsed_time(self):
        """
        Returns the time used in the previous tick
        """
        return self.elapsed_time