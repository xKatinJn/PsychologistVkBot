from config import vk, longpoll, upload
from scripts.replies import Replies
from scripts.csv_helper import CsvHelper
from resources.keyboards import schizophrenia_start_keyboard, schizophrenia_answer_keyboard,\
    schizophrenia_another_start_keyboard
from resources.answers import schizophrenia_answer_almost_no_path, schizophrenia_answer_almost_yes_path, \
    schizophrenia_answer_no_path, schizophrenia_answer_yes_path

from vk_api.bot_longpoll import VkBotEventType


# dict in which
#   key == peer_id
#   value == extended_info_dict
# number_of_question == 0 means user ended test
QUESTIONS_PATH = 'resources/questions.csv'
HAVE_PASSED_PATH = 'resources/have_passed.csv'

users_progress = {
    # Here will be k:v like
    # 'peer_id': {
    #   'question_number': 0,
    #   'yes_answers': 0,
    #   'no_answers': 0,
    #   'previous_answers': [True if yes False if no]
    # }
    'have_passed': CsvHelper.read_have_passed(HAVE_PASSED_PATH)
}
questions = CsvHelper.read_questions(QUESTIONS_PATH)

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.text.lower() == 'приступить' \
                    and (str(event.obj.peer_id) not in users_progress.keys())\
                    and (str(event.obj.peer_id) not in users_progress['have_passed']):
                users_progress[str(event.obj.peer_id)] = {
                    'question_number': 0,
                    'yes_answers': 0,
                    'no_answers': 0,
                    'previous_answers': []  # True if yes False if no
                }
                user = users_progress[str(event.obj.peer_id)]
                Replies.reply_template(vk, questions[0] +\
                                       f' ({user["question_number"] + 1}/{len(questions)})',
                                       schizophrenia_answer_keyboard,
                                       event)

            elif (str(event.obj.peer_id) not in users_progress.keys()) \
                    and (str(event.obj.peer_id) not in users_progress['have_passed']):
                Replies.send_start_request(vk, schizophrenia_start_keyboard, event)

            elif event.obj.text.lower() == 'назад':
                user = users_progress[str(event.obj.peer_id)]
                if len(user['previous_answers']) == 0:
                    Replies.reply_template(vk, 'Отступать нельзя, только вперед!', None, event)
                else:
                    if user['previous_answers'].pop():
                        user['yes_answers'] -= 1
                    else:
                        user['no_answers'] -= 1
                    user['question_number'] -= 1
                Replies.reply_template(vk,
                                       questions[user['question_number']] +\
                                       f' ({user["question_number"] + 1}/{len(questions)})',
                                       schizophrenia_answer_keyboard,
                                       event)

            elif event.obj.text.lower() == 'пройти еще раз' \
                    and (str(event.obj.peer_id) in users_progress['have_passed']):
                CsvHelper.delete_user_from_have_passed(str(event.obj.peer_id), HAVE_PASSED_PATH)
                users_progress['have_passed'] = CsvHelper.read_have_passed(HAVE_PASSED_PATH)
                users_progress[str(event.obj.peer_id)] = {
                    'question_number': 0,
                    'yes_answers': 0,
                    'no_answers': 0,
                    'previous_answers': []  # True if yes False if no
                }
                user = users_progress[str(event.obj.peer_id)]
                Replies.reply_template(vk, questions[0] + \
                                       f' ({user["question_number"] + 1}/{len(questions)})',
                                       schizophrenia_answer_keyboard,
                                       event)

            elif str(event.object.peer_id) in users_progress.keys():
                user = users_progress[str(event.object.peer_id)]
                if event.obj.text.lower() in ['да', 'нет']:
                    if event.obj.text.lower() == 'да':
                        user['yes_answers'] += 1
                        user['previous_answers'].append(True)
                    else:
                        user['no_answers'] += 1
                        user['previous_answers'].append(False)
                    user['question_number'] += 1

                if user['question_number'] < len(questions):
                    Replies.reply_template(vk,
                                           questions[user['question_number']] +\
                                           f' ({user["question_number"]+1}/{len(questions)})',
                                           schizophrenia_answer_keyboard,
                                           event)
                else:
                    if 30 <= user['yes_answers'] <= 35:
                        Replies.reply_template_with_photo(vk, None, None, event, upload, schizophrenia_answer_yes_path)
                    elif 26 <= user['yes_answers'] <= 29:
                        Replies.reply_template_with_photo(vk, None, None, event, upload,
                                                          schizophrenia_answer_almost_yes_path)
                    elif 25 <= user['no_answers'] <= 35:
                        Replies.reply_template_with_photo(vk, None, None, event, upload, schizophrenia_answer_no_path)
                    else:
                        Replies.reply_template_with_photo(vk, None, None, event, upload,
                                                          schizophrenia_answer_almost_no_path)
                    user['yes_answers'], user['no_answers'] = 0, 0
                    user['question_number'] = -1
                    CsvHelper.write_user_have_passed(str(event.obj.peer_id), HAVE_PASSED_PATH)
                    users_progress['have_passed'] = CsvHelper.read_have_passed(HAVE_PASSED_PATH)
                    users_progress.pop(str(event.obj.peer_id))
                    Replies.reply_template(vk, 'Вы также можете пройти тест заново.',
                                           schizophrenia_another_start_keyboard, event)

            elif str(event.obj.peer_id) in users_progress['have_passed']:
                Replies.send_another_start_request(vk, schizophrenia_another_start_keyboard, event)
                continue

            else:
                Replies.reply_template(vk, 'Я тебя не понимаю!', None, event)
