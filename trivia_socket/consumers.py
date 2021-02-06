import asyncio
import random
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from . import game
from .bot import TriviaBot


# a useful resource for using django channels: https://github.com/codyparker/channels-obstruction
# TODO: send new players the most recent question if they just joined
# TODO: deny if the same user answers more than once (might need authentication?)
# TODO: display correct answer text in the client
# TODO: full game statistics, not just single question

class GameConsumer(AsyncWebsocketConsumer):
    group_name = 'game'  # can change this per game so you can have multiple games going at once

    async def game(self):
        for _ in range(game.NUM_BOTS):
            game.game_data.bots.append(TriviaBot(game.BOT_ACCURACY))

        while True:
            game.game_data.round_ended = False
            game.game_data.answers.clear()
            game.game_data.question = random.choice(game.question_pool)

            correct_id = game.game_data.question['correct_id']
            correct_answer = None
            answer_ids = []
            for answer in game.game_data.question['answers']:
                answer_ids.append(answer['answer_id'])

                if answer['answer_id'] == correct_id:
                    assert correct_answer is None, "multiple correct IDs found"
                    correct_answer = answer

            assert correct_answer is not None, "no correct IDs found"

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_question',
                    'question': game.game_data.question['question'],
                    'answers': game.game_data.question['answers']
                }
            )

            for bot in game.game_data.bots:
                bot_ans = bot.answer_question(game.game_data.question['question'],
                                              answer_ids, answer_ids.index(correct_id))
                game.game_data.answers[bot_ans] += 1

            await asyncio.sleep(10)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_round_end'
                }
            )
            game.game_data.round_ended = True

            await asyncio.sleep(2)

            num_correct = game.game_data.answers[correct_id]
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_results',
                    'num_correct': num_correct,
                    'num_incorrect': sum(game.game_data.answers.values()) - num_correct,
                    'correct_id': correct_id
                }
            )

            await asyncio.sleep(5)

    async def accept(self, subprotocol=None):
        """
        Accepts an incoming socket
        """
        await super().accept(subprotocol=subprotocol)

        game.game_data.users += 1

        if not game.game_data.started:
            print('Not started yet, starting game...')
            game.game_data.started = True
            game.game_data.game_task = asyncio.create_task(self.game())

    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        game.game_data.users -= 1
        if game.game_data.users == 0:
            print('all users disconnected, killing game task...')
            game.game_data.game_task.cancel()
            game.game_data.started = False
            game.game_data.game_task = None

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if 'answer_id' in text_data_json:
            valid = not game.game_data.round_ended

            if valid:
                # does not check if the same user answered more than once...
                answer_id = text_data_json['answer_id']
                game.game_data.answers[answer_id] += 1

                print(f'User answered {answer_id}')

            await self.send(text_data=json.dumps({
                'message_type': 'received',
                'valid': valid
            }))
        else:
            print(text_data_json)

    async def send_question(self, event):
        question = event['question']
        answers = event['answers']

        await self.send(text_data=json.dumps({
            'message_type': 'question',
            'question': question,
            'answers': answers
        }))

    async def send_round_end(self, event):
        await self.send(text_data=json.dumps({
            'message_type': 'round_end',
        }))

    async def send_results(self, event):
        num_correct = event['num_correct']
        num_incorrect = event['num_incorrect']
        correct_id = event['correct_id']

        await self.send(text_data=json.dumps({
            'message_type': 'results',
            'num_correct': num_correct,
            'num_incorrect': num_incorrect,
            'correct_id': correct_id
        }))
