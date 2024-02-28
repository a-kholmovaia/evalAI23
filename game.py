import pygame
import sys
from player import Player
from sprite_master import SpriteMaster
from enemy import Enemy
from constants import BLACK
from main_menu import main_menu
from welcome_menu import welcome_menu
from play_intro import play_intro_video
class Game:
    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font("font.TTF", 24)

        # Screen dimensions
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.img_path = img_path
        # Set player's start position
        self.start_position_player = pygame.Vector2(self.SCREEN_WIDTH / 5, self.SCREEN_HEIGHT * 0.7)
        self.start_position_enemy = pygame.Vector2(self.SCREEN_WIDTH * 0.8, self.SCREEN_HEIGHT * 0.7)


        self.background = pygame.transform.scale(pygame.image.load(img_path + "background0.png"),
                                                 (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background_text = pygame.transform.scale(pygame.image.load(self.img_path + "back_text.png"), (280, 140))
        self.background_health = pygame.transform.scale(pygame.image.load(self.img_path + "back_text.png"), (240, 80))

        self.set_player()
        self.set_enemy()

    def set_player(self):
        # Initialize sprite master
        actions_dict = {
            'idle_1': {'row': 0, 'frames': 2},
            'idle_2': {'row': 0, 'frames': 2},
            'move_up': {'row': 3, 'frames': 8},
            'move_down': {'row': 3, 'frames': 8},
            'move_left': {'row': 3, 'frames': 8},
            'move_right': {'row': 3, 'frames': 8},
            'jump': {'row': 5, 'frames': 8},
            'fight': {'row': 8, 'frames': 8},
        }
        sprite_master_player = SpriteMaster(actions_dict, self.img_path + 'AnimationSheet_Character.png', 32, 32)
        self.player = Player(self.screen, self.start_position_player, sprite_master_player)

    def set_enemy(self):
        actions_enemy_dict = {
            'idle': {'row': 0, 'frames': 4},
            'fight': {'row': 1, 'frames': 4},
        }
        sprite_master_enemy = SpriteMaster(actions_enemy_dict, self.img_path + 'monster-pre.png', 32, 32,
                                           animation_speed=0.01)
        self.enemy = Enemy(self.screen, self.start_position_enemy, sprite_master_enemy)

    def run_game_loop(self):
        pygame.display.set_caption("AI-Lab: the final Battle")
        welcome_menu(self.screen)
        main_menu(self.screen)
        play_intro_video()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused  # Toggle pause state
                elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                    mouse_pos = pygame.mouse.get_pos()
                    if resume_button.collidepoint(mouse_pos):
                        paused = False  # Unpause the game
            if paused:
                resume_button = self.draw_pause_screen(self.screen)
                pygame.display.flip()  # Update the display to show the pause screen
                continue  # Skip the rest of the game loop while paused
            self.screen.fill(BLACK)
            self.screen.blit(self.background, (0, 0))

            keys = pygame.key.get_pressed()
            self.player.take_action(keys)
            self.enemy.take_action()

            if self.enemy.current_action == 'fight' and self.detect_collision(self.player.current_position, self.enemy.current_position):
                self.player.health -= 1  # Reduce player health by 5 points
            if self.player.current_action == 'fight' and self.detect_collision(self.player.current_position, self.enemy.current_position):
                self.enemy.health -= 1 # Reduce player health by 5 points

            self.draw_health_bars(self.player.health, self.enemy.health)
            self.draw_instructions()

            pygame.display.flip()
            self.clock.tick(self.FPS)

    def draw_health_bars(self, player_health, enemy_health):
        max_health_width = 200  # Width of the health bar at full health
        health_bar_height = 20
        border_padding = 15

        # Player health bar
        self.screen.blit(self.background_health, (0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (border_padding, border_padding, max_health_width, health_bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (border_padding, border_padding, player_health*2, health_bar_height))
        your_health = self.font.render("  your  health", True, BLACK)
        self.screen.blit(your_health, (border_padding, border_padding + 5 + health_bar_height))
        # Enemy health bar
        self.screen.blit(self.background_health, (self.SCREEN_WIDTH-240, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), (
        self.SCREEN_WIDTH - max_health_width - border_padding, border_padding, max_health_width, health_bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (
        self.SCREEN_WIDTH - max_health_width - border_padding, border_padding, enemy_health*2, health_bar_height))

        enemys_health = self.font.render("enemy  health", True, BLACK)
        self.screen.blit(enemys_health, (self.SCREEN_WIDTH - 13*border_padding, border_padding  + 5 + health_bar_height))

    def draw_instructions(self):
        border_padding = 35
        instructions1 = self.font.render("use  LEFT  RIGHT  UP", True, BLACK)
        instructions2 = self.font.render("arrow  to  move", True, BLACK)
        instructions3 = self.font.render("space  key  to  attack", True, BLACK)
        self.screen.blit(self.background_text,
                         (border_padding-20, border_padding * 2 + 30))

        self.screen.blit(instructions1, (border_padding, border_padding * 2 + 45))
        self.screen.blit(instructions2, (border_padding, border_padding * 2 + 85))
        self.screen.blit(instructions3, (border_padding, border_padding * 2 + 120))

    def detect_collision(self, position1, position2):
        # Simple collision detection (can be improved)
        distance = position1.distance_to(position2)
        return distance < 50  # Adjust threshold according to your game's scale

    def draw_pause_screen(self, screen):
        self.background_resume = pygame.transform.scale(pygame.image.load(self.img_path + "back_text.png"), (250, 150))
        # Darken the screen to indicate a pause
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)  # Transparency (0-255)
        overlay.fill((0, 0, 0))  # Black overlay
        screen.blit(overlay, (0, 0))
        self.screen.blit(self.background, (0, 0))

        # Draw the "Resume" button with extra padding
        font = pygame.font.Font("font.TTF", 36)
        text = font.render('Resume', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))

        # Define padding
        padding_x, padding_y = 20, 10  # You can adjust the padding values as needed

        # Create a larger rectangle based on the text size plus padding
        button_rect = pygame.Rect(0, 0, text_rect.width + padding_x * 2, text_rect.height + padding_y * 2)
        button_rect.center = text_rect.center  # Center the button rect where the text is

        screen.blit(self.background_resume, (screen.get_width()*0.35, screen.get_height()*0.37))
        pygame.draw.rect(screen, (0, 128, 0), button_rect)  # Green button
        screen.blit(text, text_rect)  # Draw the text over the button

        return button_rect  # Return the button rect for click detection