import pygame
from question import Question
from typing import Optional

class MultiScaleQuestion(Question):
    def __init__(self, screen, img_path, level="teamwork"):
        super().__init__(screen, img_path, question_text=None, question_type="scale")
        self.font = pygame.font.Font(None, 24)
        self.font_options = pygame.font.Font(None, 25)
        self.level = level
        self.questions = self.get_scale_questions()  # Use the provided list of question texts
        self.options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]  # Scale options for each question
        self.user_inputs = [""] * len(self.questions)  # Initialize user inputs for each question
        self.spacing_x, self.spacing_y = 140, 150
        self.padding_question_option = 60
        self.initial_y = 100 # Initial Y position

    def display_question(self, question_text, y):
        # Create a surface for the question background
        question_background_color = (213, 139, 55)  # Light grey color
        text_margin = 10  # Margin around the text within the rectangle

        question_surface = self.font.render(question_text, True, (0, 0, 0))
        question_width, question_height = question_surface.get_size()

        # Create a rectangle surface with padding for the question text
        question_rect_surface = pygame.Surface((question_width + 2 * text_margin, question_height + 2 * text_margin))
        question_rect_surface.fill(question_background_color)

        # Blit the text onto the rectangle surface
        question_rect_surface.blit(question_surface, (text_margin, text_margin))

        # Calculate the position to center the question rectangle on the screen
        rect_x = self.screen.get_width() // 2 - (question_width + 2 * text_margin) // 2
        rect_y = y

        # Blit the rectangle surface onto the screen
        self.screen.blit(question_rect_surface, (rect_x, rect_y))

    def display_scale_questions(self):
        y = self.initial_y # Initial Y position
        for i, question_text in enumerate(self.questions):
            self.display_question(question_text, y)
            self.display_scale_options(i, y + self.padding_question_option)  # Display scale options below the question
            y += self.spacing_y

    def display_scale_options(self, question_index, y):
        start_x = self.screen.get_width() // 2 - (self.spacing_x * (len(self.options) - 1)) // 2

        for i, option in enumerate(self.options):
            option_surface = self.font_options.render(option, True, (0, 0, 0))
            option_rect = option_surface.get_rect(center=(start_x + i * self.spacing_x, y))
            self.screen.blit(option_surface, option_rect)

            if self.user_inputs[question_index] == option:
                pygame.draw.rect(self.screen, (0, 255, 0), option_rect.inflate(10, 10), 2)  # Highlight selected option with padding

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            y = self.initial_y  # Initial Y position for the first question

            for i in range(len(self.questions)):
                start_x = self.screen.get_width() // 2 - (self.spacing_x * (len(self.options) - 1)) // 2

                for j, option in enumerate(self.options):
                    option_surface = self.font.render(option, True, (0, 0, 0))
                    option_rect = option_surface.get_rect(
                        center=(start_x + j * self.spacing_x, y + self.padding_question_option
                                ))

                    if option_rect.collidepoint(event.pos):
                        self.user_inputs[i] = option  # Update the selected option for this question
                        break  # No need to check other options for this question

                y += self.spacing_y
            # Check if the continue button is clicked
            # Ensure this part is executed only if all questions have been answered
            all_answered = all(answer != "" for answer in self.user_inputs)
            if all_answered and self.continue_button_rect.collidepoint(event.pos):
                # Execute the action associated with the continue button
                self.continue_clicked = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.display_scale_questions()
        self.draw_continue_button()

    def run(self):
        while not self.continue_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.handle_event(event)
            self.draw()
            pygame.display.flip()

        return self.user_inputs  # Return user inputs for all questions

    def get_scale_questions(self):
        if self.level == "teamwork":
            return self.get_scale_questions_teamwork()

    def get_scale_questions_teamwork(self):
        questions = [
            "Tasks were fairly and appropriately assigned to team members.",
            "Our team was successful in combining diverse skills and knowledge to achieve our goals.",
            "All team members were actively and equally involved in the work process."
        ]
        return questions
