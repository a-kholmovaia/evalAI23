import pygame
from menu.main_menu import main_menu
from menu.welcome_menu import welcome_menu
from menu.play_intro import play_intro_video
from scene import Scene
from scene00 import ScenePrelevel00
from scene01 import ScenePrelevel01
from questions.qa_evaluator import QAEvaluator
from save_master import SaveMaster


class Game:
    SCENE_PATHS = "levels/" 
    def __init__(self, FPS=60, img_path=""):

        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font("font.TTF", 24)

        # Screen dimensions
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Frame rate
        self.FPS = FPS
        self.clock = pygame.time.Clock()

        # Set a number of scenes
        self.biggest_scene_id = 101

        # Set the path to the images
        self.img_path = img_path

        # Initialize the save master
        self.save_master = SaveMaster()

    def bootstrap(self):
        pygame.display.set_caption("AI-Lab: the final Battle")
        #welcome_menu(self.screen)
        #main_menu(self.screen)
        #play_intro_video()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        """
        #evaluator = QAEvaluator(screen=self.screen, level=1)
        #evaluator.run()
        """

        scene = self.build_scene(100, False)
        while True:
            scene.run()
            scene = self.build_scene(scene.getID(), scene.isDone())
            if scene == None:
                break
    
    def build_scene(self, prev_scene_id: int, prev_scene_done: bool) -> Scene:
        """
        Instantiate the next scene

        Parameters:
        prev_scene_id: int - A number that uniquely identifies the previous scene
        prev_scene_done: bool - Was the previous scene successfully completed?
        Returns
        If there's another scene, it returns that scene, otherwise None
        """
        next_scene_id = prev_scene_id

        if prev_scene_done:
            next_scene_id += 1
        else:
            # If the previous scene was not completed then the last checkpoint should be loaded
            value = self.save_master.load_checkpoint()
            # If load_checkpoint returns 0 then the first scene should be built
            next_scene_id = value if value != 0 else 100
        
        if self.biggest_scene_id >= next_scene_id:
            if next_scene_id == 100:
                return ScenePrelevel00(scene_path=self.SCENE_PATHS + "level0/", save_master=self.save_master, 
                                     game_screen=self.screen, clock=self.clock,
                                     font=self.font, FPS=self.FPS
                                     )
            if next_scene_id == 101:
                return ScenePrelevel01(scene_path=self.SCENE_PATHS + "level0/", save_master=self.save_master,
                                     game_screen=self.screen, clock=self.clock,
                                     font=self.font, FPS=self.FPS
                                     )
        return None


        
