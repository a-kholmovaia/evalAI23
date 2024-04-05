import pygame
import openai
from constants import IMG_PATH
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class LLMResponseHandler:
    def __init__(self, screen, context, level:int, round_:int):
        self.screen = screen
        self.round = round_
        self.level = level
        self.font_spirit = pygame.font.Font('font.TTF', 25)
        self.font = pygame.font.Font(None, 25)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_width(), screen.get_height()
        self.context = context
        self.answer = ""
        self.padding = 55  # Padding for text from the edge of the screen
        self.buttons = {
            'refine': pygame.Rect(100, screen.get_height() - 90, 200, 50),
            'submit': pygame.Rect(screen.get_width() - 300, screen.get_height() - 90, 200, 50)
        }
        self.visible = False  # Initially, the response and buttons are not visible
        self.background = pygame.transform.scale(pygame.image.load("questions/back_text.png"),
                                                 (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.request_sent_llm = False

    def fetch_response(self):
        self.waiting_for_response = True
        prompt = f"""
        You are a helpful assistant, represented by a benevolent AI spirit, in a teaching evaluation game for the AI Lab seminar. The player has provided an answer regarding their experiences with teamwork, the project undertaken in the AI Lab, and the provided learning materials and workshops.

Context:
The AI Lab is a project-based seminar focusing on AI & Society, where students collaborate in teams on a project. Each team typically has a mentor responsible for guiding the team, structuring their work, providing essential information, and assigning specific tasks to each team member. Additionally, the seminar offers online learning materials and workshops on topics such as "Introduction to Machine Learning and LLMs," Python, Machine Learning, and support hours (Tutorien) where students can seek help and support for their projects.

Task:
Please evaluate the player's answer based on the following criteria: Clarity and Coherence, Relevance, Specific Examples, and Constructive Criticism. Below are detailed descriptions of each criterion along with examples of good and bad responses. Each criterion is worth 1 to 10 points. If you identify areas for improvement in any of the criteria, please pose 2-3 refining questions to help the player enhance their answer. 
Refining questions should be in the same language as the response. Additionally, based on the answers provided, you may ask extra questions found in the "Other questions" section. Below are examples of refining questions you might consider asking, based on the player's responses:

Refining Questions Examples:
{self.get_extra_questions()}

You could also ask extra questions based on the answers in the "Other questions" section. Use the directions provided by the questions above as a basis for generating your refining questions.

Criteria:

1. Clarity and Coherence:
    - Detail: Effective responses should be clear, well-structured, and avoid vagueness, providing specific details where necessary.
    - Good Example: "The lecturer used clear, well-structured explanations to cover complex statistical concepts, making them easier to understand. For instance, the step-by-step breakdown of regression analysis was particularly effective." - 10 points.
    - Bad Example: "The lecture was good. I liked the statistics stuff." - 1 point
    - Good Example: "In the team project, communication was key. Our team leader organized weekly meetings that were well-structured, allowing each member to share progress and concerns effectively." - 10 points.
    - Bad Example: "Teamwork was fine. We did stuff together." - 1 point

2. Relevance:
    - Detail: Responses should directly address the seminar's aspects, focusing specifically on the lecture or teaching methods.
    - Good Example: "The lecture's focus on statistical software application was highly relevant to our coursework, allowing us to directly apply what we learned in class to our assignments." - 10 points.
    - Bad Example: "I think the university needs more parking spaces. It's hard to find a spot before class." - 1 point
    - Good Example: "The question on how roles were distributed within our team is relevant, as it highlights our strategy of leveraging individual strengths for task allocation, which significantly improved our efficiency." - 10 points.
    - Bad Example: "I think the cafeteria food could be better. It's not related, but it's important." - 1 point

3. Specific Examples:
    - Detail: Good responses connect feedback to specific instances from the lecture, providing clear, contextualized examples.
    - Good Example: "In response to the question about the clarity of statistical concepts presented, I appreciated the detailed breakdown of the 'Central Limit Theorem' in week 3's lecture, where the professor used the class's average quiz scores as a practical example to explain the concept." - 10 points.
    - Bad Example: "The professor explained statistical concepts well." - 1 point
    - Good Example: "When addressing the question on conflict resolution, I recall a specific instance where there was a disagreement on the project design. We resolved it by combining elements from each proposal, leading to a more innovative solution." - 10 points.
    - Bad Example: "We had some disagreements, but it was nothing." - 1 point

4. Constructive Criticism:
    - Detail: Criticism should pinpoint areas for improvement and offer specific, actionable suggestions.
    - Good Example: "While the lecture covered a lot of ground, some complex topics like hypothesis testing were rushed. It might be helpful to allocate more time to these areas or provide supplemental materials for further reading." - 10 points.
    - Bad Example: "I didn't get hypothesis testing. It was confusing." - 1 point
    - Good Example: "Although our team worked well overall, we could have benefited from a more structured approach to brainstorming sessions. Perhaps using a digital collaboration tool would help organize and record our ideas more effectively." - 10 points.
    - Bad Example: "I think some team members were lazy, but I'm not sure who." - 1 point

{self.context}

Template for Your Feedback:
"
Clarity and Coherence: _ points
Relevance: _ points
Specific Examples: _ points
Constructive Criticism: _ points

Feedback: write 3-4 sentences what was good in the response and what needs improvement.
Refining Questions: ask 2-3 questions that help to improve the player's answer.
"
Your Feedback:
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify the GPT-4 model
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant evaluating a player's response in a teaching evaluation game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            self.answer = response.choices[0].message['content']  # Accessing the content of the response
            print(self.answer)
            self.visible = True  # Make the response and buttons visible after fetching the answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Unable to evaluate the answer at this time."

    def draw(self):
        self.screen.fill((200, 200, 200))  # Fill the background
        self.screen.blit(self.background, (0, 0))
        if not self.visible:
            waiting_text = self.font.render("AI Spirit is thinking... Wait a moment...", True, (0, 0, 0))
            self.screen.blit(waiting_text, (self.SCREEN_WIDTH*0.2, self.SCREEN_HEIGHT*0.3))  # Adjust position as needed

        if not self.request_sent_llm:
            self.fetch_response()
            self.request_sent_llm = True

        if self.visible:
            rendered_answer = self.answer.split("Feedback:")[1]
            self.draw_multiline_text(rendered_answer, (self.padding, 50), self.font)

            instructions = self.font.render(
                "To finish answering questions and resume your game, please click on 'submit answer'.",
                True, (255, 0, 0)
            )
            self.screen.blit(instructions, (self.SCREEN_WIDTH*0.07, self.SCREEN_HEIGHT*0.8))

            # Draw buttons
            for key, rect in self.buttons.items():
                pygame.draw.rect(self.screen, (100, 100, 255) if key == 'refine' else (50, 205, 50), rect)
                button_text = 'Refine Answer' if key == 'refine' else 'submit answer'
                text_surface = self.font_spirit.render(button_text, True, (255, 255, 255))
                self.screen.blit(text_surface, (rect.x + 10, rect.y + 10))

    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons['refine'].collidepoint(event.pos):
                return 'refine'
            elif self.buttons['submit'].collidepoint(event.pos):
                return 'submit'
        return None

    def run(self):
        running = True
        clock = pygame.time.Clock()  # To control the frame rate
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle events for GPTResponseHandler
                action = self.handle_event(event)
                if action == 'refine':
                    # Handle the refining of the GPT answer here
                    print("Refine Answer clicked")
                    return self.answer, True
                elif action == 'submit':
                    # Handle the submission of the GPT answer here
                    print("Submit Answer clicked")
                    return self.answer, False

            self.screen.fill((200, 200, 200))  # Fill the background
            self.screen.blit(self.background, (0, 0))

            # Draw the GPT answer and buttons
            self.draw()

            pygame.display.flip()  # Update the full display Surface to the screen
            clock.tick(60)  # Cap the frame rate to 60 frames per second

    def draw_multiline_text(self, text, position, font, color=(0, 0, 0)):
        words = text.split(' ')
        space_width, line_height = font.size(' ')[0], font.get_linesize()
        x, y = position
        for word in words:
            if '\n' in word:  # Check for newline character
                lines = word.split('\n')
                for i, line in enumerate(lines):
                    word_surface = font.render(line, True, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= self.screen.get_width() - self.padding:
                        x = position[0]  # Reset to the starting x position
                        y += line_height  # Start a new line
                    self.screen.blit(word_surface, (x, y))
                    if i < len(lines) - 1:  # If there's another line coming
                        x = position[0]  # Reset x
                        y += line_height  # Move y to new line
                    else:
                        x += word_width + space_width
            else:
                word_surface = font.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= self.screen.get_width() - self.padding:
                    x = position[0]  # Reset to the starting x position
                    y += line_height  # Start a new line
                self.screen.blit(word_surface, (x, y))
                x += word_width + space_width

    def get_extra_questions(self):
        if self.level==1 and self.round==0:
            return self.get_extra_questions_teamwork()

    def get_extra_questions_teamwork(self):
        return """
- Roles: "Did everyone know what they were supposed to do in the team?"
- Talking: "Was it easy to talk and listen to each other in the team?"
- Solving Problems: "When there was a disagreement, how did the team solve it?"
- Helping Out: "Did everyone do their part in the team's work?"
- Leading: "How well did your team leader or mentor help the team?"
- Goals: "Did everyone agree on what the team was trying to achieve?"
- Getting Better: "Did the team discuss ways to improve for next time?"
- Trusting: "Could you count on everyone in the team?"
- New Ideas: "Was the team open to hearing new ideas?"
- Happy: "Were you satisfied working in the team, and what could make it better?"
- Learning from Each Other: "Did you learn anything new from team members with different expertise?"
- Different Skills: "Did team members utilize their diverse skills and knowledge to contribute?"
- Fair Work: "Were tasks distributed based on individuals' strengths or areas they wished to develop?"  
        """
    
    def refine_evaluate(self, context):
        prompt = f"""
        You are a helpful assistant, represented by a benevolent AI spirit, in a teaching evaluation game for the AI Lab seminar. The player has provided an answer regarding their experiences with teamwork, the project undertaken in the AI Lab, and the provided learning materials and workshops.

Context:
The AI Lab is a project-based seminar focusing on AI & Society, where students collaborate in teams on a project. Each team typically has a mentor responsible for guiding the team, structuring their work, providing essential information, and assigning specific tasks to each team member. Additionally, the seminar offers online learning materials and workshops on topics such as "Introduction to Machine Learning and LLMs," Python, Machine Learning, and support hours (Tutorien) where students can seek help and support for their projects.

Task:
The player was asked a question and after the player answered they become refinement suggestions. Based on the refining questions, player changed their answer. 
Please reevaluate the player's answer based on the following criteria: Clarity and Coherence, Relevance, Specific Examples, and Constructive Criticism. Below are detailed descriptions of each criterion along with examples of good and bad responses. Each criterion is worth 1 to 10 points. 

Criteria:

1. Clarity and Coherence:
    - Detail: Effective responses should be clear, well-structured, and avoid vagueness, providing specific details where necessary.
    - Good Example: "The lecturer used clear, well-structured explanations to cover complex statistical concepts, making them easier to understand. For instance, the step-by-step breakdown of regression analysis was particularly effective." - 10 points.
    - Bad Example: "The lecture was good. I liked the statistics stuff." - 1 point
    - Good Example: "In the team project, communication was key. Our team leader organized weekly meetings that were well-structured, allowing each member to share progress and concerns effectively." - 10 points.
    - Bad Example: "Teamwork was fine. We did stuff together." - 1 point

2. Relevance:
    - Detail: Responses should directly address the seminar's aspects, focusing specifically on the lecture or teaching methods.
    - Good Example: "The lecture's focus on statistical software application was highly relevant to our coursework, allowing us to directly apply what we learned in class to our assignments." - 10 points.
    - Bad Example: "I think the university needs more parking spaces. It's hard to find a spot before class." - 1 point
    - Good Example: "The question on how roles were distributed within our team is relevant, as it highlights our strategy of leveraging individual strengths for task allocation, which significantly improved our efficiency." - 10 points.
    - Bad Example: "I think the cafeteria food could be better. It's not related, but it's important." - 1 point

3. Specific Examples:
    - Detail: Good responses connect feedback to specific instances from the lecture, providing clear, contextualized examples.
    - Good Example: "In response to the question about the clarity of statistical concepts presented, I appreciated the detailed breakdown of the 'Central Limit Theorem' in week 3's lecture, where the professor used the class's average quiz scores as a practical example to explain the concept." - 10 points.
    - Bad Example: "The professor explained statistical concepts well." - 1 point
    - Good Example: "When addressing the question on conflict resolution, I recall a specific instance where there was a disagreement on the project design. We resolved it by combining elements from each proposal, leading to a more innovative solution." - 10 points.
    - Bad Example: "We had some disagreements, but it was nothing." - 1 point

4. Constructive Criticism:
    - Detail: Criticism should pinpoint areas for improvement and offer specific, actionable suggestions.
    - Good Example: "While the lecture covered a lot of ground, some complex topics like hypothesis testing were rushed. It might be helpful to allocate more time to these areas or provide supplemental materials for further reading." - 10 points.
    - Bad Example: "I didn't get hypothesis testing. It was confusing." - 1 point
    - Good Example: "Although our team worked well overall, we could have benefited from a more structured approach to brainstorming sessions. Perhaps using a digital collaboration tool would help organize and record our ideas more effectively." - 10 points.
    - Bad Example: "I think some team members were lazy, but I'm not sure who." - 1 point

{self.context}

Template for Your Feedback:
"
Clarity and Coherence: _ points
Relevance: _ points
Specific Examples: _ points
Constructive Criticism: _ points

Feedback:
"
Your Feedback:
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify the GPT-4 model
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant evaluating a player's response in a teaching evaluation game."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            self.answer = response.choices[0].message['content']  # Accessing the content of the response
            print(self.answer)
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Unable to evaluate the answer at this time."

