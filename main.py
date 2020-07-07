from config import vk, longpoll
from scripts.replies import Replies
from scripts.csv_helper import CsvHelper
from resources.keyboards import schizophrenia_start_keyboard, schizophrenia_answer_keyboard
from resources.answers import schizophrenia_answer_almost_no, schizophrenia_answer_almost_yes, schizophrenia_answer_no, \
    schizophrenia_answer_yes

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
    #   'previous_answer': [True if yes False if no]
    # }
    'have_passed': CsvHelper.read_have_passed(HAVE_PASSED_PATH)
}
questions = CsvHelper.read_questions(QUESTIONS_PATH)

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if str(event.object.peer_id) in users_progress.keys():
                user = users_progress[str(event.object.peer_id)]
                if str(event.obj.peer_id) in users_progress['have_passed']:
                    Replies.send_antoher_start_request(vk, schizophrenia_start_keyboard, event)
                    continue
                if event.obj.text.lower() in ['да', 'нет']:
                    if event.obj.text.lower() == 'да':
                        user['yes_answers'] += 1
                    else:
                        user['no_answers'] += 1
                    user['question_number'] += 1
                if user['question_number'] < len(questions):
                    Replies.reply_template(vk, questions[user['question_number']], schizophrenia_answer_keyboard, event)
                else:
                    if 30 <= user['yes_answers'] <= 35:
                        Replies.reply_template(vk, schizophrenia_answer_yes, None, event)
                    elif 26 <= user['yes_answers'] <= 29:
                        Replies.reply_template(vk, schizophrenia_answer_almost_yes, None, event)
                    elif 25 <= user['no_answers'] <= 35:
                        Replies.reply_template(vk, schizophrenia_answer_no, None, event)
                    else:
                        Replies.reply_template(vk, schizophrenia_answer_almost_no, None, event)
                    user['yes_answers'], user['no_answers'] = 0, 0
                    user['question_number'] = -1
                    CsvHelper.write_user_have_passed(str(event.ojb.peer_id), HAVE_PASSED_PATH)
                    users_progress['have_passed'] = CsvHelper.read_have_passed(HAVE_PASSED_PATH)

            elif event.obj.text.lower() == 'приступить' and (str(event.obj.peer_id) not in users_progress.keys()):
                users_progress[str(event.obj.peer_id)] = {
                    'question_number': 0,
                    'yes_answers': 0,
                    'no_answers': 0,
                    'previous_answer': None  # True if yes False if no
                }
                Replies.reply_template(vk, questions[0], schizophrenia_answer_keyboard, event)

            else:
                Replies.send_start_request(vk, schizophrenia_start_keyboard, event)

            print(questions)
            print(len(questions))
            print(event)


# TODO: Recognize retests
# TODO:

"""
Если “ДА” от 30 до 35
У Вас большая вероятность развития явной формы шизофрении. 
Вам необходимо как можно скорее обратиться за консультацией к психиатру.

Если “Да” от 26 до 30
У Вас вполне может быть латентная шизофрения (то есть, её скрытая форма). 
Кроме того, подобные симптомы могут наблюдаться и при других психических заболеваниях. 
Для уточнения диагноза сходите на консультацию к специалисту.


Если “НЕТ” от 25 до 35
Согласно тесту, шизофрения однозначно вам не грозит. 
Ваша психика устойчива и стабильна. 
Чтобы она оставалась такой всегда, старайтесь избегать стрессов.

Если “НЕТ” от 10 до 25
Скорее всего, с вашей психикой всё в порядке, кроме некоторых временных психологических проблем, 
вызванных ситуативным стрессом. Для их решения можно проконсультироваться с психологом.
"""