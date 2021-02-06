from collections import defaultdict

NUM_BOTS = 5
BOT_ACCURACY = 0.8

question_pool = [
    {
        'question': 'Which of these books was published several centuries ago?',
        'answers': [
            {'answer_id': 1, 'answer': 'Ready Player One'},
            {'answer_id': 2, 'answer': 'The Fault in Our Stars'},
            {'answer_id': 3, 'answer': 'Don Quixote'},
        ],
        'correct_id': 3
    },
    {
        'question': 'The first move in Scrabble must touch what part of the board?',
        'answers': [
            {'answer_id': 4, 'answer': 'Center'},
            {'answer_id': 5, 'answer': 'Corner'},
            {'answer_id': 6, 'answer': 'Edge'},
        ],
        'correct_id': 4
    },
    {
        'question': 'Nutella was sued in the US for ads implying it was what?',
        'answers': [
            {'answer_id': 7, 'answer': 'American-made'},
            {'answer_id': 8, 'answer': 'Healthy'},
            {'answer_id': 9, 'answer': 'Safe for dogs'},
        ],
        'correct_id': 8
    }
]


class GameData:
    started = False
    game_task = None
    round_ended = False
    answers = defaultdict(int)
    question = None
    users = 0
    bots = []


game_data = GameData()

