class Replies:
    @staticmethod
    def reply_template(vk, message, keyboard, event) -> None:
        vk.messages.send(peer_id=event.obj.peer_id,
                         message=message,
                         random_id=0,
                         keyboard=keyboard.get_keyboard())

    @staticmethod
    def reply_start_request(vk, keyboard, event) -> None:
        message = 'Предлагаю тебе пройти тест на наличие шизофрении. Приступим?'
        vk.messages.send(peer_id=event.obj.peer_id,
                         message=message,
                         random_id=0,
                         keyboard=keyboard.get_keyboard())
