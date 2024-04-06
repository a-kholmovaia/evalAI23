from questions.question import Question
from questions.multiscale import MultiScaleQuestion
from questions.LLMResponse import LLMResponseHandler
from constants import OUTPUT_FILE_PATH
import pygame

class QAEvaluator:      
    def __init__(self, level: int, screen: pygame.Surface) -> None:
        self.screen = screen
        pygame.display.set_caption("Question Screen")
        self.round = 0
        self.level = level

    def _init_level(self):
        self.open_question = Question(self.screen, self.level, self.round)
        self.multi_scale_question = MultiScaleQuestion(self.screen, self.level, self.round)

    def get_answers(self):
        responses = self.multi_scale_question.run()
        answer_open = self.open_question.run()
        context = f"\nQuestion: {self.open_question.get_question_text()[self.round]}\n" \
                f"Player's answer: {answer_open}\n" \
                f"Other questions answered: \n"
        questions_scale = self.multi_scale_question.get_scale_questions()
        for question, option in zip(questions_scale, responses):
            context += f" Q:{question}, A: {option} \n"
        self.context = context
    
    def handle_answer(self):
        # Initialize the GPTResponseHandler with the screen and your OpenAI API key
        self.llm_handler = LLMResponseHandler(self.screen, self.context, self.level, self.round)

        llm_response, self.refine = self.llm_handler.run()
        self.scores = self.get_points(llm_response)
        self.get_refining_questions(llm_response)
        self.context += "\n" + llm_response
    
    def get_points(self, response):
        response = response.split('Feedback:')[0].split('point')[:4]
        print(response)
        scores = []
        for i in response:
            score = i.split(':')[1]
            scores.append(int(score))
        print(scores)
        return scores
    
    def get_refining_questions(self, llm_response):
        self.refining_questions = llm_response.split('Refining Questions:')[-1]
    
    def refine_answer(self):
        self.refining_question = Question(self.screen, self.level, self.round, refine=True)
        self.refining_question.set_question_text(self.refining_questions)
        self.context += self.refining_question.run()
        self.llm_handler.set_context(self.context)
        self.llm_handler.refine_evaluate()
        llm_answer = self.llm_handler.answer
        self.context += llm_answer
        self.scores_refining = self.get_points(llm_answer)
    
    def run(self):
        while(self.round<2):
            self._init_level() 
            self.get_answers()
            self.handle_answer()
            if self.refine:
                self.refine_answer()

            with open(OUTPUT_FILE_PATH,"a") as f:
                f.write(self.context)

            self.round += 1 

        

