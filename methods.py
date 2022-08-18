from datetime import datetime, date, time
from decouple import config
import telebot
import time as timer
import pymorphy2

from keyboard_menus_methods import *

morph = pymorphy2.MorphAnalyzer()

TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
time_of_msg = time(23, 10)  # 23:10:00 по МСК, время, после которого нужно публиковать сообщения

month_dict = {'01': "Январь", '02': "Февраль", '03': "Март", '04': "Апрель", '05': "Май", '06': "Июнь",
              '07': "Июль", '08': "Август", '09': "Сентябрь", '10': "Октябрь", '11': "Ноябрь", '12': "Декабрь"}


def send_birthday_msg(name):
    bot.send_message("@birthdaysGenshin",
                     "<b>{name}</b> сегодня празднует свой день рождения!".format(name=name))
    # когда будет пак картинок для сообщений, надо заменить send_message на send_photo
    # bot.send_photo("@birthdaysGenshin", photo, caption='желаемый текст')


def send_hello_msg(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj9pi-XwJ6DuPzfFzrNhgFAo74cNd6gACPw8AAnqS-EtUlG9v__OqzSkE',
                     reply_markup=main_menu())


def send_closest_bday(message):
    # сохраняем сегодняшнюю дату и заодно вытаскиваем оттуда год (для того, чтобы потом форматировать даты из словаря)
    today = date.today()
    year_today = str(today.year)
    year_today = "." + year_today

    closest_bday_persons = []
    delta = -1
    date_of_closest_bday = ""
    # перебираем все даты из словаря (предварительно переведя их из строки в формат даты) до тех пор,
    # пока не найдем ближайшую к сегодняшней дате (в будущем, не в прошлом)
    for key in birthdays_and_names.keys():
        bday = key + year_today
        bday = bday.replace('.', '/')
        if (key == '29.02') and (
                int(year_today[3:]) % 4 != 0):  # если дата - 29 ферваля, но год не високосный, пропускаем
            continue
        else:
            bday_format = datetime.strptime(bday, "%d/%m/%Y")
            bday_format = bday_format.date()
        cur_delta = bday_format - today
        if cur_delta.days >= 0:  # как только находим неотрицательную разницу, прерываем цикл
            delta = cur_delta.days
            closest_bday_persons = birthdays_and_names[key]
            date_of_closest_bday = key
            break

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

    celebrate = ""
    if len(closest_bday_persons) > 1 and delta == 0:
        celebrate = "празднуют"
    elif len(closest_bday_persons) > 1 and delta > 0:
        celebrate = "будут праздновать"
    elif len(closest_bday_persons) == 1 and delta == 0:
        celebrate = "празднует"
    elif len(closest_bday_persons) == 1 and delta > 0:
        celebrate = "будет праздновать"

    bot.send_message(message.chat.id, f"{when}, {date_of_closest_bday}, {chars} {celebrate} свой день рождения!",
                     reply_markup=main_menu())


def send_bday_closest_to_my_bday(message):
    bot.send_message(message.chat.id, '⚙ Эта функция очень нескоро будет готова 😢️', reply_markup=main_menu())


def send_alphabet(message):
    bot.send_message(message.chat.id, 'Выберите первую букву имени персонажа', reply_markup=alphabet_menu())


def send_list_of_chars(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите нужного персонажа",
                          reply_markup=char_menu(call.data))


def send_bday_of_char(call):
    bday_of_char = ''
    exitFlag = False
    # цикл ищет переданное имя в словаре. Как только находит, сохраняет дату рождения и прерывается
    for bday, names in birthdays_and_names.items():
        for name in names:
            if name == call.data:
                bday_of_char = bday
                exitFlag = True
                break
        if exitFlag:
            break
    # перевод числового обозначения месяца в текстовый в родительном падеже (09 -> сентября)
    month = bday_of_char[3:]
    month_text = ""
    for key, value in month_dict.items():
        if key == month:
            month_text = value
            break
    month_text = morph.parse(month_text)[0]
    month_text = month_text.inflect({'gent'})  # родительный падеж

    # если день формата 01, 02, .., 09, то обрезаем 0 в начале
    bday_of_char = bday_of_char[:2]
    if bday_of_char[0] == '0':
        bday_of_char = bday_of_char[1:]

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{call.data} празднует свой день рождения {bday_of_char} {month_text.word}",
                          reply_markup=btn_back_to_start())


def send_that_month_bdays(message):
    current_month = str(date.today())[5:7]
    names_of_chars = "Дни рождения в этом месяце:\n\n"
    text_of_msg = find_bdays_in_month(current_month, names_of_chars)
    bot.send_message(message.chat.id, text_of_msg, reply_markup=main_menu())


def send_bdays_of_selected_month(call, month):
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
    for key in birthdays_and_names.keys():
        month_of_bday = key[3:]
        if required_month == month_of_bday:
            names = birthdays_and_names[key]
            names_one_day = ""
            if len(names) > 1:
                for name in names:
                    names_one_day += name + ", "
            if names_one_day == "":
                names_of_chars += "{bday}: {name}\n".format(bday=key, name=names[0])
            else:
                names_one_day = names_one_day[:-2]
                names_of_chars += "{bday}: {name}\n".format(bday=key, name=names_one_day)
    return names_of_chars


def send_month_menu(message):
    bot.send_message(message.chat.id, text="Какой месяц интересует?", reply_markup=month_menu())


def check_time():
    """
    Метод постоянно прокручивает массив дней рождений.
    Когда находит совпадение по дате, проверяет время.
    Если оно больше или равно заданного в переменной и сегодня он еще не публиковал ничего,
    тогда метод публикует сообщение на канале и делает отметку, что он это сделал.
    Отметка сбрасывается при наступлении следующего дня
    """
    saved_date = ''
    is_msg_sent = False
    while True:
        today = date.today().strftime("%d.%m")
        if saved_date != today:
            saved_date = today
            is_msg_sent = False

        for birthday in birthdays_and_names.keys():
            if birthday == today:
                time_now = datetime.now().time()
                if time_now >= time_of_msg and not is_msg_sent:
                    names = birthdays_and_names[birthday]
                    for name in names:
                        send_birthday_msg(name)
                        timer.sleep(15)
                    is_msg_sent = True
        timer.sleep(600)  # сон на 10 минут
