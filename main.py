from config import vk, longpoll
from replies import Replies
from resources.keyboards import schizophrenia_keyboard

from vk_api.bot_longpoll import VkBotEventType


# dict in which
#   key == peer_id
#   value == extended_info_dict
# number_of_question == 0 means user ended test

users_progress = {}
questions = []

if __name__ == '__main__':
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not questions:
                # load questions from csv
                pass
            if event.object.peer_id in users_progress.keys():
                # send question or not
                pass
            Replies.reply_to(vk, 'Test_msg', schizophrenia_keyboard, event)
            print(event)

