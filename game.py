import pygame
import sys
from player import Player
from sprite_master import SpriteMaster

class Game:

    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Colors
        self.BLACK = (0, 0, 0)

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        # Set player's start position
        self.start_position = pygame.Vector2(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)

        # Initialize sprite master
        sprite_master = SpriteMaster(img_path + 'AnimationSheet_Character.png', 32, 32)

        # Initialize player's representation
        self.player = Player(self.screen, self.start_position, sprite_master)

    def run_game_loop(self):

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Draw background
            self.screen.fill(self.BLACK)

            # Render scene

            # Let the player take an action according to the keys pressed
            keys = pygame.key.get_pressed()
            self.player.take_action(keys)
            

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()