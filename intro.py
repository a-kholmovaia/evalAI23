import pygame
import sys
from constants import WIDTH, HEIGHT, WHITE, BLUE
from tools import  Button
import random
pygame.init()
# Load images
background_img = pygame.transform.scale(pygame.image.load("img/background_kidnap.png"), (WIDTH, HEIGHT))
person_imgs = [pygame.image.load("img/person{}.png".format(i)) for i in range(1, 6)]
wizard_img = pygame.image.load("img/evil_wizard.png")
storm_img = pygame.transform.scale(pygame.image.load("img/storm.png"), (200, 200))  # Resize the storm image

# Font
font = pygame.font.Font(None, 36)

# Define classes
class Person:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (100, 100))  # Resize the person image
        self.speed = random.randint(1, 3)  # Random speed
        self.direction = random.choice(["left", "right"])

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        direction = self.direction
        if direction == "up":
            self.y -= self.speed
        elif direction == "down":
            self.y += self.speed
        elif direction == "left":
            self.x -= self.speed
        elif direction == "right":
            self.x += self.speed
        # Ensure the person stays within the screen bounds
        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))

class EvilWizard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(wizard_img, (150, 150))  # Resize the wizard image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Storm:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = storm_img

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= 5

def intro_kidnapping(screen, seq: int):
    start_button = Button(WIDTH - 300, HEIGHT - 100, 200, 50, BLUE, "START", WHITE, font)
    if seq == 1:
        path = "img/username_menu.png"
    elif seq == 2:
        path = "img/username_menu.png"
    elif seq == 3:
        path = "img/username_menu.png"
    background_img = pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                        return
        # Clear the screen
        screen.fill(WHITE)
        # Clear the screen
        screen.blit(background_img, (0, 0))

        start_button.draw(screen)

        # Update the display
        pygame.display.flip()

def walking_scene(screen):
    # Generate 5 people with random positions
    people = [Person(
        random.randint(WIDTH*0.3, WIDTH*0.7), random.randint(HEIGHT*0.7, HEIGHT*0.8), person_imgs[i]
    ) for i in range(5)]

    # Main loop
    start_time = pygame.time.get_ticks()  # Get the start time
    while pygame.time.get_ticks() - start_time < 10000:  # Run for 10 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)
        screen.blit(background_img, (0, 0))

        # Move and draw people
        for person in people:
            person.move()
            person.draw(screen)

        # Update the display
        pygame.display.flip()

        # Adjust game speed
        pygame.time.Clock().tick(60)

def kidnapping_scene(screen):
    # Initialize objects
    persons = [Person(30 + i * 80, 400, person_imgs[i]) for i in range(5)]
    wizard = EvilWizard(WIDTH - 200, 400)
    storm = Storm(WIDTH - 350, 300)
    # Main game loop
    kidnapping = True
    curse_timer = 0
    storm_timer = 0
    wizard_laughed = False
    wizard_cursed = False
    storm_started = False
    while kidnapping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.blit(background_img, (0, 0))

        # Draw objects
        for person in persons:
            if storm.x > person.x:
                person.draw(screen)
        wizard.draw(screen)
        if storm_started:
            storm.draw(screen)

        # Update the display
        pygame.display.flip()

        # Adjust game speed
        pygame.time.Clock().tick(60)

        # Update timers
        curse_timer += 1
        storm_timer += 1

        # Display curse text
        if not wizard_cursed:
            curse_text = font.render("You are cursed!", True, (255, 0, 0))
            screen.blit(curse_text, (wizard.x - 150, wizard.y - 50))
            pygame.display.flip()
            pygame.time.delay(2000)
            wizard_cursed = True
        elif not storm_started:
            storm_started = True

        # Move the storm towards the people
        if storm_started and not storm.x <= persons[0].x:  # Wait for the curse to finish
            storm.move()
            if storm.x == persons[0].x:
                storm_started = False

        # Check if the storm reached the people
        if storm_started and storm.x <= 30:  # Storm reached the people
            for person in persons:
                person.x = -100  # Move people out of the screen
            storm.x = -100  # Reset storm position for next use
            if not wizard_laughed:
                wizard_laughed = True
                ha_ha_text = font.render("HAHAHA", True, (255, 0, 0))
                screen.blit(ha_ha_text, (wizard.x - 100, wizard.y - 100))
                pygame.display.flip()

                # Wait for a moment
                pygame.time.delay(1000)

            kidnapping = False

def intro(screen):
    intro_kidnapping(screen, 1)
    walking_scene(screen)
    intro_kidnapping(screen, 2)
    kidnapping_scene(screen)
    intro_kidnapping(screen, 3)