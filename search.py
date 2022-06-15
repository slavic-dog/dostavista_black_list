# функция превращает message в номер телефона в текстовом формате
def correct_number(message):
    a = [' ', '+', '(', ')', '-']
    number = message.text
    for s in a:
        number = number.replace(s, '')
    if number.startswith(('7', '8')) and len(number) == 11 and number.isdigit():
        number = f'+7 ({number[1:4]}) {number[4:7]}-{number[7:9]}-{number[9:]}'
        return number
    elif number.startswith(('9', '8')) and len(number) == 10 and number.isdigit():
        number = '1' + number
        number = f'+7 ({number[1:4]}) {number[4:7]}-{number[7:9]}-{number[9:]}'
        return number
    else:
        print('Номер не существует. Попробуйте еще раз.')
        return None


# функция превращает message в адрес в текстовом формае
def correct_address(message):
    address = message.text
    return address



def parameter_check(message):
    checker = {'number': ['Введите номер', correct_number, 0],
               'address': ['Введите адрес(без номера квартиры)', correct_address, 1]
               }
    if message.text in checker:
        mg = bot.send_message(message.chat.id, checker[message.text][0])
        bot.register_next_step_handler(mg, parameter_search, checker[message.text][1], checker[message.text][2], file)
    else:
        bot.send_message(message.chat.id, 'Неизвесная команда')


# Осуществляет поск. Возможно лучше разбить эту тварь
def parameter_search(message, func_message_to_parameter, parameter_type, output_file):
    parameter = func_message_to_parameter(message)
    if parameter is not None:
        workbook = openpyxl.load_workbook(output_file)
        ws = workbook['data']
        max_row = 'C' + str(ws.max_row)
        client_list = []
        for row in ws['A2':max_row]:
            if parameter == row[parameter_type].value:
                client_list.append('\n'.join([r.value for r in row]))
        workbook.close()
        if len(client_list) == 0:
            res_of_search = ['Клиент чист']
        elif len(client_list) == 1:
            res_of_search = client_list
        else:
            res_of_search = [f'{i+1}: {client}' for i, client in enumerate(client_list)]
        show_result(message, res_of_search)


# выводи результат поиска пользователю
def show_result(message, res_of_search):
    clients_info = '\n'.join(res_of_search)
    bot.send_message(message.chat.id, clients_info)


# поиск по параметру. вызывает пачку кнопок. зачем? загадка...
@bot.message_handler(commands=['search'])
def client_search_by_number(message):
    # тут будут кнопки
    mg = bot.send_message(message.chat.id, 'Выберите параметр поиска')
    # а тут они пропадут
    bot.register_next_step_handler(mg, parameter_check)

