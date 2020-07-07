class Replies:
    @staticmethod
    def reply_template(vk, message, keyboard, event) -> None:
        if keyboard:
            vk.messages.send(peer_id=event.obj.peer_id,
                             message=message,
                             random_id=0,
                             keyboard=keyboard.get_keyboard())
        else:
            vk.messages.send(peer_id=event.obj.peer_id,
                             message=message,
                             random_id=0)

    @staticmethod
    def send_start_request(vk, keyboard, event) -> None:
        message = 'Привет! Предлагаю тебе пройти тест на наличие шизофрении. Приступим?'
        vk.messages.send(peer_id=event.obj.peer_id,
                         message=message,
                         random_id=0,
                         keyboard=keyboard.get_keyboard())

    @staticmethod
    def send_another_start_request(vk, keyboard, event) -> None:
        message = 'Я вижу, что тобою уже пройден этот тест. Хочешь пройти его заново?'
        vk.messages.send(peer_id=event.obj.peer_id,
                         message=message,
                         random_id=0,
                         keyboard=keyboard.get_keyboard())
