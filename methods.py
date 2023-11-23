import os
from datetime import datetime, date
import calendar
import telebot
import sqlite3
import pymorphy2

from keyboard_menus_methods import *

morph = pymorphy2.MorphAnalyzer()

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('/function/storage/tg-bot-account/database.db', check_same_thread=False)
cursor = conn.cursor()

month_dict = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь',
              '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}
text_input_bday = 'Пожалуйста, введи дату рождения в формате дд.мм\n' \
                  'Например, 01.08 или 30.11; также допускаются варианты 1.8, 01.8, 1.08'


def format_str_date(bday):
    return datetime.strptime(bday, '%Y-%m-%d').date()


def format_str_day(day):
    return '0' + str(day) if len(str(day)) == 1 else str(day)


def format_str_month(month):
    return '0' + str(month) if len(str(month)) == 1 else str(month)


def send_hello_msg(message):
    """ отвечает заданным стикером на приветствие """
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj9pi-XwJ6DuPzfFzrNhgFAo74cNd6gACPw8AAnqS-EtUlG9v__OqzSkE',
                     reply_markup=main_menu())


def send_closest_bday(message):
    """ ищет и отправляет ближайший день рождения """
    current_year = date.today().year
    current_month = date.today().month
    current_day = date.today().day

    our_date = date(2020, current_month, current_day)

    cursor.execute(f'SELECT * FROM birthdays WHERE bday = (SELECT bday '
                   f'FROM birthdays WHERE bday >= "{our_date}" ORDER BY bday LIMIT 1) ORDER BY name')
    closest_bday_persons = cursor.fetchall()

    bday_format = format_str_date(closest_bday_persons[0][1])
    delta = (bday_format - our_date).days

    isBennet = False
    if current_year % 4 != 0 and str(bday_format) == '2020-02-29':
        delta -= 1
        isBennet = True

    date_of_closest_bday = f'{format_str_day(bday_format.day)}.{format_str_month(bday_format.month)}'

    chars = ''  # если имен больше чем 1, они будут в формате имя1, имя2 и имя3 (или имя1 и имя2)
    if len(closest_bday_persons) > 1:
        for person in closest_bday_persons:
            if closest_bday_persons.index(person) == len(closest_bday_persons) - 1:
                chars = chars[:-2]
                chars += ' и ' + person[0]
            else:
                chars += person[0] + ', '
    else:
        chars = closest_bday_persons[0][0]

    # формируем сообщение о том, через сколько дней ДР перса
    if delta == 0:
        when = 'Сегодня'
    elif delta == 1:
        when = 'Завтра'
    elif delta == 2:
        when = 'Послезавтра'
    else:
        parsed_word = morph.parse('день')[0]
        when = parsed_word.make_agree_with_number(delta).word

    # задаем число (ед./множ.) и время (наст./будущ.) для сказуемого
    celebrate = ''
    if len(closest_bday_persons) > 1 and delta == 0:
        celebrate = 'празднуют'
    elif len(closest_bday_persons) > 1 and delta > 0:
        celebrate = 'будут праздновать'
    elif len(closest_bday_persons) == 1 and delta == 0:
        celebrate = 'празднует'
    elif len(closest_bday_persons) == 1 and delta > 0:
        celebrate = 'будет праздновать'

    # формируем текст сообщения
    if isBennet:
        response = f'{date_of_closest_bday} {chars} {celebrate} свой день рождения! {when}, 28.02, придет письмо'
    else:
        response = f'{when}, {date_of_closest_bday}, {chars} {celebrate} свой день рождения!'

    # бот отправляет в чат сообщение
    bot.send_message(message.chat.id, response, reply_markup=main_menu())


def send_bday_closest_to_my_bday(message, user_bday):
    sql_diff = f'ABS( julianday(bday) - julianday("{str(user_bday)}") )'

    subquery = f'SELECT {sql_diff} FROM birthdays ORDER BY {sql_diff} LIMIT 1'
    cursor.execute(subquery)
    bday_difference = int(cursor.fetchone()[0])

    # поскольку январь и декабрь не воспринимаются как граничные месяцы, нужна доп. проверка
    subquery = f'SELECT {sql_diff} FROM birthdays ORDER BY {sql_diff} DESC LIMIT 1'
    cursor.execute(subquery)
    additional_bday_difference = int(cursor.fetchone()[0])

    if 366 - additional_bday_difference < bday_difference:
        bday_difference = 366 - additional_bday_difference
        query = f'SELECT * FROM birthdays WHERE {sql_diff} = {additional_bday_difference} ORDER BY bday, name'
    else:
        query = f'SELECT * FROM birthdays WHERE {sql_diff} = {bday_difference} ORDER BY bday, name'
    cursor.execute(query)
    chars = cursor.fetchall()

    if bday_difference == 0:
        message_for_user = 'У тебя день рождения в один день со следующими персонажами:\n'
    else:
        parsed_word = morph.parse('день')[0]
        word_day = parsed_word.make_agree_with_number(bday_difference).word
        message_for_user = f'Никто из персонажей, к сожалению, не празднует день рождения в один день с тобой.\n' \
                           f'Но есть те, разница с которыми составляет всего {bday_difference} {word_day}:\n'

    for char in chars:
        bday_format = format_str_date(char[1])
        message_for_user += f'{char[0]} ({format_str_day(bday_format.day)}.{format_str_month(bday_format.month)})\n'
    bot.send_message(message.chat.id, message_for_user, reply_markup=main_menu())


def send_alphabet(message):
    """ отправляет сообщение с инлайн клавиатурой с алфавитом """
    bot.send_message(message.chat.id, 'Выберите первую букву имени персонажа', reply_markup=alphabet_menu())


def send_list_of_chars(call):
    """ в зависимости от выбранной буквы алфавита возвращает список персонажей, редактируя сообщение """
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберите нужного персонажа',
                          reply_markup=char_menu(call.data))


def send_bday_of_char(call):
    """ ищет день рождения конкретного персонажа при алфавитном поиске """
    cursor.execute(f'SELECT * FROM birthdays where name = "{call.data}"')
    char = cursor.fetchone()  # кортеж
    # перевод числового обозначения месяца в текстовый в родительном падеже (09 -> сентября)
    bday_format = format_str_date(char[1])
    month = format_str_month(bday_format.month)
    month_text = ''
    for key, value in month_dict.items():
        if key == month:
            month_text = value
            break
    month_text = morph.parse(month_text)[0]
    month_text = month_text.inflect({'gent'})  # родительный падеж

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'{call.data} празднует свой день рождения {bday_format.day} {month_text.word}',
                          reply_markup=btn_back_to_start())


def send_that_month_bdays(message):
    """
    получает сегодняшнюю дату и достает из нее месяц. Месяц передает в find_bdays_in_month(),
    который возвращает список ДР, после чего публикует сообщение
     """
    current_month = str(date.today().month)
    names_of_chars = 'Дни рождения в этом месяце:\n\n'
    text_of_msg = find_bdays_in_month(current_month, names_of_chars)
    bot.send_message(message.chat.id, text_of_msg, reply_markup=main_menu())


def send_bdays_of_selected_month(call, month):
    """
    метод получает из инлайн клавиатуры название месяца, переводит его в предложный падеж
    и ищет цифровой код этого месяца в соответствующем словаре (month_dict), затем вызывает find_bdays_in_month(),
    чтобы получить список ДР в заданном месяце, после чего редактирует сообщение с инлайн клавиатурой
    """
    month_analyse = morph.parse(month)[0]
    month_loct = month_analyse.inflect({'loct'})  # предложный падеж

    digit_month = ''
    for key, value in month_dict.items():  # перевод текстового формата названия месяца в числовой (январь -> 01)
        if month == value:
            digit_month = key
    names_of_chars = f'Дни рождения в {month_loct.word}:\n\n'
    text_of_msg = find_bdays_in_month(digit_month, names_of_chars)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text_of_msg,
                          reply_markup=month_menu())


def find_bdays_in_month(required_month, names_of_chars):
    """ ищет дни рождения в переданном ему месяце """
    _, last_day = calendar.monthrange(date.today().year, int(required_month))
    start_date = '"' + str(date(2020, int(required_month), 1)) + '"'
    end_date = '"' + str(date(2020, int(required_month), last_day)) + '"'
    cursor.execute(f'SELECT * FROM birthdays WHERE bday BETWEEN {start_date} AND {end_date} ORDER BY bday')
    characters = cursor.fetchall()  # лист кортежей
    for char in characters:
        bday_format = format_str_date(char[1])
        birthday = f'{format_str_day(bday_format.day)}.{format_str_month(bday_format.month)}'
        names_of_chars += f'{birthday}: {char[0]}\n'
    return names_of_chars


def send_month_menu(message):
    """ при нажатии на кнопку "дни рождения в заданном месяце" отправляет сообщение с инлайн клавиатурой с месяцами """
    bot.send_message(message.chat.id, text='Какой месяц интересует?', reply_markup=month_menu())


def char_menu(letter):
    """
    Метод получает букву из алфавита, а затем в словаре ищет все имена, начинающиеся на эту букву,
    и добавляет их в список. После этого на основе списка формируется набор кнопок
    """
    char_keyboard = types.InlineKeyboardMarkup()

    cursor.execute(f'SELECT name FROM birthdays where name LIKE "{letter}%" ORDER BY name')
    names_list = cursor.fetchall()  # лист кортежей

    for name in names_list:
        char_keyboard.add(types.InlineKeyboardButton(name[0], callback_data=name[0]))

    char_keyboard.add(types.InlineKeyboardButton('Вернуться назад', callback_data='back'))
    return char_keyboard
