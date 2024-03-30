from typing import List
from scene00 import Scene


class Level:

    def __init__(self, scenes : List[Scene]):
        self.scenes = scenes

    def run(self):
        
        self.__run_intro()

        for scene in self.scenes:
            scene.run()

        self.__run_outro()

    def __run_intro(self):
        pass

    def __run_outro(self):
        pass
