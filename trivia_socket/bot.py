import random
from typing import List


class TriviaBot:
    """Answers a question randomly based on a percentage chance of the correct answer"""

    def __init__(self, accuracy: float):
        self.accuracy = accuracy

    def answer_question(self, question: str, answers: List, correct_idx: int):
        """Answer a question.

        Doesn't actually have to take in the question itself but could be useful if you
        wanted to have the bot do something with it in the future.
        """

        print(f'Answering question "{question}"')

        if random.random() < self.accuracy:
            print('choosing the correct answer...')
            return answers[correct_idx]

        print('choosing the wrong answer...')
        options = list(range(0, correct_idx))
        options += list(range(correct_idx + 1, len(answers)))
        return answers[random.choice(options)]


if __name__ == '__main__':
    bot = TriviaBot(0.8)  # will choose the correct answer 80% of the time

    for _ in range(5):
        answer = bot.answer_question(
            'What year was Python first released?',
            ['1989', '1991', '2000'],
            1
        )

        print(answer)
        print()