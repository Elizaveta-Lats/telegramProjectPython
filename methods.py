from datetime import datetime, date, time
from decouple import config
import telebot
import sqlite3
import time as timer
import pymorphy2

from keyboard_menus_methods import *

morph = pymorphy2.MorphAnalyzer()

TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


conn = sqlite3.connect('db/database.db', check_same_thread=False)
cursor = conn.cursor()


# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
time_of_msg = time(23, 10)  # 23:10:00 по МСК, время, после которого нужно публиковать сообщения

month_dict = {'01': "Январь", '02': "Февраль", '03': "Март", '04': "Апрель", '05': "Май", '06': "Июнь",
              '07': "Июль", '08': "Август", '09': "Сентябрь", '10': "Октябрь", '11': "Ноябрь", '12': "Декабрь"}


def send_birthday_msg(name):
    """ публикует запись в канале о том, что некий персонаж празднует свой день рождения """
    bot.send_message("@birthdaysGenshin",
                     "<b>{name}</b> сегодня празднует свой день рождения!".format(name=name))
    # когда будет пак картинок для сообщений, надо заменить send_message на send_photo
    # bot.send_photo("@birthdaysGenshin", photo, caption='желаемый текст')


def send_hello_msg(message):
    """ отвечает заданным стикером на приветствие """
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj9pi-XwJ6DuPzfFzrNhgFAo74cNd6gACPw8AAnqS-EtUlG9v__OqzSkE',
                     reply_markup=main_menu())


def send_closest_bday(message):
    """ ищет и отправляет ближайший день рождения """
    # определяем текущий день и месяц
    current_month = date.today().month
    current_day = date.today().day
    # пробуем получить записи с будущими ДР в текущем месяце
    # (например, если запрос был 20.08, он будет искать ДР в диапазоне 20.08-31.08)
    cursor.execute(f"SELECT * FROM birthdays where month = {current_month} AND day >= {current_day} ORDER BY day")
    characters = cursor.fetchall()  # лист кортежей

    if len(characters) == 0:  # если в текущем месяце уже нет грядущих ДР, запрашиваем ДР следующего месяца
        next_month = (current_month + 1) if current_month <= 11 else 1
        cursor.execute(f"SELECT * FROM birthdays where month = {next_month} ORDER BY day")
        characters = cursor.fetchall()

    closest_bday_persons = [characters[0][0]]  # сохраняем в отдельный лист имя из первой записи полученного запроса,
    day = characters[0][1]  # а также в отдельных переменных сохраняем день и месяц рождения этого персонажа
    month = characters[0][2]
    characters.pop(0)  # удаляем из листа с запросом первую запись
    for char in characters:  # перебираем оставшиеся элементы в листе
        if day == char[1]:  # если есть совпадения по дате рождения
            closest_bday_persons.append(char[0])  # добавляем имя персонажа в closest_bday_persons
        else:  # как только совпадения заканчиваются, цикл прерывается
            break

    # получаем сегодняшнюю дату, отдельно сохраняем год (для того, чтобы потом вычислять разницу в датах)
    today = date.today()
    year_today = today.year
    # так как Беннет родился 29.02, отслеживаем, чтобы код не попытался в невисокосный год высветить дату 29 февраля
    isBennet = False
    if day == 29 and month == 2 and year_today % 4 != 0:
        closest_bday = f"{28}.{month}.{year_today}"
        isBennet = True
    else:
        closest_bday = f"{day}.{month}.{year_today}"

    # форматируем ДР в тип date, вычисляем разницу в днях между сегодняшним днем и ДР
    bday_format = datetime.strptime(closest_bday, "%d.%m.%Y").date()
    delta = (bday_format - today).days

    # форматирование даты ДР, чтобы был вид 01.06, а не 1.6
    str_day = "0" + str(day) if 1 <= day <= 9 else str(day)
    str_month = "0" + str(month) if 1 <= month <= 9 else str(month)
    date_of_closest_bday = f"{str_day}.{str_month}"

    # формируем список персонажей-именинников
    chars = ""  # если имен больше чем 1, они будут в формате имя1, имя2 и имя3 (или имя1 и имя2)
    if len(closest_bday_persons) > 1:
        for person in closest_bday_persons:
            if closest_bday_persons.index(person) == len(closest_bday_persons) - 1:
                chars = chars[:-2]
                chars += " и " + person
            else:
                chars += person + ", "
    else:
        chars = closest_bday_persons[0]

    # формируем сообщение о том, через сколько дней ДР перса
    when = ""
    if delta == 0:
        when = "Сегодня"
    elif delta == 1:
        when = "Завтра"
    elif delta == 2:
        when = "Послезавтра"
    else:
        if (11 <= delta <= 19) or (delta % 10 == 0) or (5 <= delta % 10 <= 9) \
                or (111 <= delta <= 119) or (211 <= delta <= 219) or (311 <= delta <= 319):
            when = f"Через {delta} дней"
        elif 2 <= delta % 10 <= 4:
            when = f"Через {delta} дня"
        elif delta % 10 == 1:
            when = f"Через {delta} день"

    # задаем число (ед./множ.) и время (наст./будущ.) для сказуемого
    celebrate = ""
    if len(closest_bday_persons) > 1 and delta == 0:
        celebrate = "празднуют"
    elif len(closest_bday_persons) > 1 and delta > 0:
        celebrate = "будут праздновать"
    elif len(closest_bday_persons) == 1 and delta == 0:
        celebrate = "празднует"
    elif len(closest_bday_persons) == 1 and delta > 0:
        celebrate = "будет праздновать"

    # формируем текст сообщения
    if isBennet:
        response = f"{when}, {date_of_closest_bday}, {chars} {celebrate} свой день рождения! Письмо придет 28.02"
    else:
        response = f"{when}, {date_of_closest_bday}, {chars} {celebrate} свой день рождения!"

    # бот отправляет в чат сообщение
    bot.send_message(message.chat.id, response, reply_markup=main_menu())


def send_bday_closest_to_my_bday(message):
    bot.send_message(message.chat.id, '⚙ Эта функция очень нескоро будет готова 😢️', reply_markup=main_menu())


def send_alphabet(message):
    """ отправляет сообщение с инлайн клавиатурой с алфавитом """
    bot.send_message(message.chat.id, 'Выберите первую букву имени персонажа', reply_markup=alphabet_menu())


def send_list_of_chars(call):
    """ в зависимости от выбранной буквы алфавита возвращает список персонажей, редактируя сообщение """
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите нужного персонажа",
                          reply_markup=char_menu(call.data))


def send_bday_of_char(call):
    """ ищет день рождения конкретного персонажа при алфавитном поиске """
    cursor.execute(f'SELECT * FROM birthdays where name = "{call.data}"')
    char = cursor.fetchone()  # кортеж
    # перевод числового обозначения месяца в текстовый в родительном падеже (09 -> сентября)
    month = str(char[2]) if len(str(char[2])) == 2 else '0' + str(char[2])
    month_text = ""
    for key, value in month_dict.items():
        if key == month:
            month_text = value
            break
    month_text = morph.parse(month_text)[0]
    month_text = month_text.inflect({'gent'})  # родительный падеж

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{call.data} празднует свой день рождения {char[1]} {month_text.word}",
                          reply_markup=btn_back_to_start())


def send_that_month_bdays(message):
    """
    получает сегодняшнюю дату и достает из нее месяц. Месяц передает в find_bdays_in_month(),
    который возвращает список ДР, после чего публикует сообщение
     """
    current_month = str(date.today().month)
    names_of_chars = "Дни рождения в этом месяце:\n\n"
    text_of_msg = find_bdays_in_month(current_month, names_of_chars)
    bot.send_message(message.chat.id, text_of_msg, reply_markup=main_menu())


def send_bdays_of_selected_month(call, month):
    """
    метод получает из инлайн клавиатуры название месяца, переводит его в предложный падеж
    и ищет цифровой код этого месяца в соответствующем словаре (month_dict), затем вызывает find_bdays_in_month(),
    чтобы получить список ДР в заданном месяце, после чего редактирует сообщение с инлайн клавиатурой
    "
    """
    month_analyse = morph.parse(month)[0]
    month_loct = month_analyse.inflect({'loct'})  # предложный падеж

    digit_month = ''
    for key, value in month_dict.items():  # перевод текстового формата названия месяца в числовой (январь -> 01)
        if month == value:
            digit_month = key
    names_of_chars = "Дни рождения в {month}:\n\n".format(month=month_loct.word)
    text_of_msg = find_bdays_in_month(digit_month, names_of_chars)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text_of_msg,
                          reply_markup=month_menu())


def find_bdays_in_month(required_month, names_of_chars):
    """ ищет дни рождения в переданном ему месяце """
    cursor.execute(f'SELECT * FROM birthdays where month = {required_month} ORDER BY day')
    characters = cursor.fetchall()  # лист кортежей
    for char in characters:
        day = str(char[1])
        if len(day) == 1:  # "приклеиваем" 0 спереди, если день 1-9
            day = '0' + day
        month = str(char[2])
        if len(month) == 1:  # "приклеиваем" 0 спереди, если месяц 1-9
            month = '0' + month
        birthday = f"{day}.{month}"
        names_of_chars += "{bday}: {name}\n".format(bday=birthday, name=char[0])
    return names_of_chars


def send_month_menu(message):
    """ при нажатии на кнопку "дни рождения в заданном месяце" отправляет сообщение с инлайн клавиатурой с месяцами """
    bot.send_message(message.chat.id, text="Какой месяц интересует?", reply_markup=month_menu())


def char_menu(letter):
    """
    Метод получает букву из алфавита, а затем в словаре ищет все имена, начинающиеся на эту букву,
    и добавляет их в список. После этого на основе списка формируется набор кнопок
    """
    char_keyboard = types.InlineKeyboardMarkup()

    cursor.execute(f"SELECT name FROM birthdays where name LIKE '{letter}%' ORDER BY name")
    names_list = cursor.fetchall()  # лист кортежей

    for name in names_list:
        char_keyboard.add(types.InlineKeyboardButton(name[0], callback_data=name[0]))

    char_keyboard.add(types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
    return char_keyboard


def check_time():
    """
    Метод постоянно запрашивает у БД, есть ли ДР в этот день.
    Когда БД возвращает запись, метод проверяет время.
    Если оно больше или равно заданного в переменной и сегодня он еще не публиковал ничего,
    тогда метод публикует сообщение на канале и делает отметку, что он это сделал.
    Отметка сбрасывается при наступлении следующего дня
    """
    saved_date = ''
    is_msg_sent = False
    while True:
        today = date.today()
        if saved_date != today:
            saved_date = today
            is_msg_sent = False

        if int(today.day) == 28 and int(today.month) == 2 and int(today.year) % 4 != 0:
            cursor.execute(f"SELECT name FROM birthdays WHERE (day = 28 OR day = 29) AND month = 2")
        else:
            cursor.execute(f"SELECT name FROM birthdays WHERE day = {today.day} AND month = {today.month}")
        characters = cursor.fetchall()  # лист кортежей
        if len(characters) > 0:
            time_now = datetime.now().time()
            if time_now >= time_of_msg and not is_msg_sent:
                names = []
                for char in characters:
                    names.append(char[0])
                for name in names:
                    send_birthday_msg(name)
                    timer.sleep(15)
                is_msg_sent = True
        timer.sleep(600)  # сон на 10 минут
