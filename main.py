from game import Game

if __name__ == "__main__":
    # Initialize game
    game = Game(img_path="img/")
    game.run_game_loop()
    print("the game has succesfully ended")