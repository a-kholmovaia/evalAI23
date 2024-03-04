import pygame
from constants import IMG_PATH

class Question:
    def __init__(self, screen, question_text, question_type="open"):
        self.screen = screen
        self.question_text = question_text
        self.question_type = question_type  # "open" or "scale"
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_width(), screen.get_height()

        self.user_input = ""
        self.font_button = pygame.font.Font('font.TTF', 36)
        self.font = pygame.font.Font(None, 36)

        # Enlarged text box for multiline input
        self.text_box_rect = pygame.Rect(screen.get_width() * 0.1, screen.get_height() * 0.3,
                                         screen.get_width() * 0.8, self.SCREEN_HEIGHT * 0.5)

        self.continue_button_rect = pygame.Rect(screen.get_width() * 0.7, screen.get_height() * 0.85, 180, 40)

        self.background = pygame.transform.scale(pygame.image.load(IMG_PATH + "back_text.png"),
                                                 (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.continue_clicked = False
        self.line_height = self.font.get_height()


    def draw_text_box(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.text_box_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.text_box_rect, 2)  # Border

    def display_answer(self):
        lines = self.split_text_into_lines(self.user_input, self.text_box_rect.width - 10)  # Adjust for padding
        for i, line in enumerate(lines):
            line_surface = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(line_surface, (self.text_box_rect.x + 5, self.text_box_rect.y + 5 + i * self.line_height))

    def split_text_into_lines(self, text, max_width):
        lines = []
        current_line = ""
        for word in text.split(' '):
            if self.font.size(word)[0] > max_width:
                # If the word itself exceeds the max width, split the word
                if current_line:
                    lines.append(current_line)  # Add the current line to lines
                    current_line = ""  # Start a new line
                lines.extend(self.split_long_word(word, max_width))  # Split the long word into lines
            else:
                # Check if adding the word exceeds the max width
                test_line = f"{current_line} {word}".strip()
                if self.font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)  # Add the current line to lines
                    current_line = word  # Start a new line with the current word

        if current_line:  # Add the last line
            lines.append(current_line)
        return lines

    def split_long_word(self, word, max_width):
        # Split a long word into chunks that fit within max_width
        chunks = []
        current_chunk = ""
        for char in word:
            test_chunk = f"{current_chunk}{char}"
            if self.font.size(test_chunk)[0] <= max_width:
                current_chunk = test_chunk
            else:
                chunks.append(current_chunk)  # Add the current chunk to chunks
                current_chunk = char  # Start a new chunk with the current char
        if current_chunk:
            chunks.append(current_chunk)  # Add the last chunk
        return chunks

    def draw(self):
        self.display_question()
        if self.question_type == "open":
            self.draw_text_box()
            self.display_answer()
        self.draw_continue_button()

    def run(self):
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                self.handle_event(event)
                if self.continue_clicked:
                    return self.user_input

            self.screen.fill((200, 200, 200))  # Fill the background
            self.screen.blit(self.background, (0, 0))
            self.draw()
            pygame.display.flip()

        return self.user_input  # Return the user's input after clicking "Continue"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.question_type == "open":
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                self.user_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button_rect.collidepoint(event.pos):
                self.continue_clicked = True
                # Potentially call a method to handle the continue action

    def display_question(self):
        question_surface = self.font.render(self.question_text, True, (0, 0, 0))
        question_rect = question_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 5))
        self.screen.blit(question_surface, question_rect)

    def draw_continue_button(self):
        continue_surface = self.font_button.render('Continue', True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 128, 0), self.continue_button_rect)  # Green button
        self.screen.blit(continue_surface, (self.continue_button_rect.x + 10, self.continue_button_rect.y))


