from vk_api.keyboard import VkKeyboard, VkKeyboardColor


schizophrenia_start_keyboard = VkKeyboard(one_time=False)

schizophrenia_start_keyboard.add_button('Приступить', color=VkKeyboardColor.POSITIVE)


schizophrenia_answer_keyboard = VkKeyboard(one_time=False)

schizophrenia_answer_keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
schizophrenia_answer_keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
schizophrenia_answer_keyboard.add_line()
schizophrenia_answer_keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)

schizophrenia_another_start_keyboard = VkKeyboard(one_time=False)

schizophrenia_another_start_keyboard.add_button('Пройти еще раз', color=VkKeyboardColor.POSITIVE)
