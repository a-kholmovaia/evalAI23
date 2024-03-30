from questions.question import Question
from questions.multiscale import MultiScaleQuestion
from questions.LLMResponse import LLMResponseHandler
from constants import OUTPUT_FILE_PATH
import pygame

class QuestionResponseBuilder:
        
    def __init__(self) -> None:
        pygame.display.set_caption("Question Screen")

        # Create question instances
        questions= [ "Wie war die Teamarbeit?"]
        open_question = Question(self.game_screen, self.scene_path, questions[0])

        multi_scale_question = MultiScaleQuestion(self.game_screen, self.scene_path)
        responses = multi_scale_question.run()
        print(responses)

        answer_open = open_question.run()

        context = f"\nQuestion: {questions[0]}\n" \
                f"Player's answer: {answer_open}\n" \
                f"Other questions answered: \n"
        questions_scale = multi_scale_question.get_scale_questions_teamwork()
        for question, option in zip(questions_scale, responses):
            context += f" Q:{question}, A: {option} \n"
        print(context)
        # Initialize the GPTResponseHandler with the screen and your OpenAI API key
        llm_handler = LLMResponseHandler(self.game_screen, context)
        # Run the game loop
        llm_response = llm_handler.run()
        context += "\n" + llm_response
        with open(OUTPUT_FILE_PATH,"a") as f:
            f.write(context)