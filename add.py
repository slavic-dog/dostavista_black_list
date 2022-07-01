import openpyxl
import telebot

file = 'black_list.xlsx'
token =
bot = telebot.TeleBot(token)


def correct_number(number):
    a = [' ', '+', '(', ')', '-']
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
        return 1


def start_list(message):
    mg = bot.send_message(message.chat.id, 'Введите номер телефона')
    bot.register_next_step_handler(mg, phon_number)


def phon_number(message):
    phon = message.text
    phon = correct_number(phon)
    if phon == 1:
        bot.send_message(message.chat.id, 'Номер не существует. Попробуйте еще раз.')
        start_list(message)

    else:
        client_info = [phon]
        address = bot.send_message(message.chat.id, 'Введите адрес')
        bot.register_next_step_handler(address, address_phone, client_info)


def address_phone(message, client_info):
    client_info.append(message.text)
    description = bot.send_message(message.chat.id, 'Опишите происшествие')
    bot.register_next_step_handler(description, address_phone_description, client_info)


def address_phone_description(message, client_info):
    client_info.append(message.text)
    data_writer(client_info, file)
    bot.send_message(message.chat.id, 'Запись добавлена')


def data_writer(client_info, output_file):
    workbook = openpyxl.load_workbook(output_file)
    ws = workbook['data']
    ws.append(client_info)
    workbook.save(output_file)
    workbook.close()
