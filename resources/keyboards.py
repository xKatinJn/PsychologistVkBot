from vk_api.keyboard import VkKeyboard, VkKeyboardColor


schizophrenia_keyboard = VkKeyboard(one_time=True)

schizophrenia_keyboard.add_button('Да', color=VkKeyboardColor.POSITIVE)
schizophrenia_keyboard.add_button('Нет', color=VkKeyboardColor.NEGATIVE)
