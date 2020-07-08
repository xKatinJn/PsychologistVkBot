import os

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.upload import VkUpload


vk_session = vk_api.VkApi(token=str(os.environ.get('token')) if os.environ.get('token') else 'write_token_here',
                          api_version=5.95)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, os.environ.get('group_id'))
upload = VkUpload(vk_session)
