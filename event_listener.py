import pygame
from scene import Scene

class EventListener:

    def __init__(self):
        self.scene_subscriber = None
    
    def set_scene_subscriber(self, scene: Scene) -> None:
        self.scene_subscriber = scene

    def listen_events(self) -> None:
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.scene_subscriber.event_end_game_loop

