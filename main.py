from config import vk, longpoll
from scripts.replies import Replies
from scripts.question_reader import QuestionReader
from resources.keyboards import schizophrenia_start_keyboard, schizophrenia_answer_keyboard

from vk_api.bot_longpoll import VkBotEventType


# dict in which
#   key == peer_id
#   value == extended_info_dict
# number_of_question == 0 means user ended test
QUESTIONS_PATH = 'resources/questions.csv'

users_progress = {}
questions = QuestionReader.read_questions(QUESTIONS_PATH)

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if str(event.object.peer_id) in users_progress.keys():
                user = users_progress[str(event.object.peer_id)]
                if event.obj.text.lower() in ['да', 'нет']:
                    if event.obj.text.lower() == 'да':
                        user['yes_answers'] += 1
                    else:
                        user['no_answers'] += 1
                    user['question_number'] += 1
                if user['question_number'] < len(questions)-1:
                    Replies.reply_template(vk, questions[user['question_number']], schizophrenia_answer_keyboard, event)
                else:
                    # count the result
                    pass
            elif event.obj.text.lower() == 'приступить' and (str(event.obj.peer_id) not in users_progress.keys()):
                users_progress[str(event.obj.peer_id)] = {
                    'question_number': 0,
                    'yes_answers': 0,
                    'no_answers': 0
                }
                Replies.reply_template(vk, questions[0], schizophrenia_answer_keyboard, event)
            else:
                Replies.reply_start_request(vk, schizophrenia_start_keyboard, event)

            print(questions)
            print(len(questions))
            print(event)

# TODO: Count result
# TODO: Output result
# TODO: Recognize retests
