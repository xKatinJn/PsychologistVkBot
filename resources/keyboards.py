from vk_api.keyboard import VkKeyboard, VkKeyboardColor


schizophrenia_start_keyboard = VkKeyboard(one_time=True)

schizophrenia_start_keyboard.add_button('Приступить', color=VkKeyboardColor.POSITIVE)


schizophrenia_answer_keyboard = VkKeyboard(one_time=True)

schizophrenia_answer_keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
schizophrenia_answer_keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
