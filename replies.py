class Replies:
    @staticmethod
    def reply_to(vk, message, keyboard, event) -> None:
        vk.messages.send(peer_id=event.obj.peer_id,
                         message=message,
                         random_id=0,
                         keyboard=keyboard.get_keyboard())
