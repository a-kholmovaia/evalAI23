from game import Game
from question import Question
from multiscale import MultiScaleQuestion
from LLMResponse import LLMResponseHandler
from constants import OUTPUT_FILE_PATH
if __name__ == "__main__":
    # Initialize game
    game = Game(img_path="img/")
    game.run()
    print("the game has succesfully ended")

    # Pygame setup
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    # pygame.display.set_caption("Question Screen")

    # # Create question instances
    # questions= [ "Wie war die Teamarbeit?"]
    # open_question = Question(screen, questions[0])

    # multi_scale_question = MultiScaleQuestion(screen)
    # responses = multi_scale_question.run()
    # print(responses)

    # answer_open = open_question.run()

    # context = f"\nQuestion: {questions[0]}\n" \
    #           f"Player's answer: {answer_open}\n" \
    #           f"Other questions answered: \n"
    # questions_scale = multi_scale_question.get_scale_questions_teamwork()
    # for question, option in zip(questions_scale, responses):
    #     context += f" Q:{question}, A: {option} \n"
    # print(context)
    # # Initialize the GPTResponseHandler with the screen and your OpenAI API key
    # llm_handler = LLMResponseHandler(screen, context)
    # # Run the game loop
    # llm_response = llm_handler.run()
    # context += "\n" + llm_response
    # with open(OUTPUT_FILE_PATH,"a") as f:
    #     f.write(context)




