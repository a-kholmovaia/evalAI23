from game import Game
import os, sys


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        os.chdir(application_path)
        print(application_path)
    Game(img_path="img/").bootstrap()
    print("the game has succesfully ended")