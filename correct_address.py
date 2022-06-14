#Проверка номера, Ввод адреса
def phon_number(message):
    phon = message.text
    phon = correct_number(phon)
    if phon == 1:
        bot.send_message(message.chat.id, 'Номер не существует. Попробуйте еще раз.')
        start_list(message)

    else:
        client_info = [phon]
        address = bot.send_message(message.chat.id, 'Введите адрес клиента')
        bot.register_next_step_handler(address, correct_address, client_info)


def repeat_address(message, client_info):
    address = bot.send_message(message.chat.id, 'Введите адрес клиента')
    bot.register_next_step_handler(address, correct_address, client_info)


def correct_address(message, client_info):
    address = message.text
    bot.register_next_step_handler(city, correct_address, client_info)





#Ввод проблемы
def address_phone(message, client_info):
    client_info.append(message.text)
    description = bot.send_message(message.chat.id, 'Опишите происшествие')
    bot.register_next_step_handler(description, address_phone_description, client_info)