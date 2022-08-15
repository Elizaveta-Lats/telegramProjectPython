from datetime import datetime, date, time
from decouple import config
from threading import Thread
import telebot
from telebot import types
import time as timer

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

time_of_msg = time(23, 10)  # 23:10:00 по МСК, время, после которого нужно публиковать сообщения

birthdays_and_names = {'01.06': ["Итто", "Паймон"], '24.07': ["Сиканоин Хэйдзо"], '15.08': ["Коллеи"]}

text_for_btn_hello = "👋 Поздороваться"
text_for_btn_closest_bday = "❓ Ближайший ДР"
text_for_btn_that_month_bdays = "🎉 Дни рождения в этом месяце"
text_for_btn_selected_month_bdays = "🎂 Дни рождения в заданном месяце"
text_for_btn_bday_closest_to_my_bday = "🤔 Узнать, чей ДР ближе всего к моему"
text_for_btn_find_bday_of_char = "🔍 Узнать ДР персонажа"


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, когда я вырасту, я буду сообщать про ДР персонажей геншина',
                     reply_markup=main_menu())
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj6Zi-UrjcS6F5m3hXB44mFi_KPDn2wACdw0AAnDa8UsVqatk3kgIuSkE')


@bot.message_handler(commands=['help', 'about'])
def about_handler(message):
    bot.send_message(message.chat.id, "Привет!\nЗдесь ты можешь узнать, чей день рождения скоро наступит, "
                                      "у кого дни рождения в текущем (или выбранном тобой) месяце. "
                                      "Для этого тебе нужно всего лишь нажать на кнопки внизу!\n\n"
                                      "Кроме того, в этом канале https://t.me/birthdaysGenshin "
                                      "я буду тебе напоминать про дни рождения "
                                      "персонажей Genshin Impact. Переходи туда!")


@bot.message_handler(commands=['hello'])
def hello_handler(message):
    send_hello_msg(message)


@bot.message_handler(commands=['closestbday'])
def closest_bday_handler(message):
    send_closest_bday(message)


@bot.message_handler(commands=['bdaysthatmonth'])
def bdays_that_month_handler(message):
    send_that_month_bdays(message)


@bot.message_handler(commands=['bdaysselectedmonth'])
def bdays_selected_month_handler(message):
    send_selected_month_bdays(message)


@bot.message_handler(commands=['bdayclosesttomybday'])
def bdays_closest_to_my_bday_handler(message):
    send_bday_closest_to_my_bday(message)


@bot.message_handler(commands=['findbdayofchar'])
def find_bday_of_char_handler(message):
    send_bday_of_char(message)


@bot.message_handler(content_types=['text'])
# заменить на inline кнопки выбор месяца (с inline пока не получилось)
def get_text_messages(message):
    if message.text == text_for_btn_hello or message.text.lower() == "hello" or message.text.lower() == "привет":
        send_hello_msg(message)
    elif message.text == text_for_btn_closest_bday:
        send_closest_bday(message)
    elif message.text == text_for_btn_that_month_bdays:
        send_that_month_bdays(message)
    elif message.text == text_for_btn_selected_month_bdays:
        send_selected_month_bdays(message)
    elif message.text == "Январь" or message.text == "Февраль" or message.text == "Март" or message.text == "Апрель" \
            or message.text == "Май" or message.text == "Июнь" or message.text == "Июль" or message.text == "Август" \
            or message.text == "Сентябрь" or message.text == "Октябрь" or message.text == "Ноябрь" \
            or message.text == "Декабрь":
        bot.send_message(message.chat.id, 'Да, это тоже в процессе разработки ⚙️')
    elif message.text == text_for_btn_bday_closest_to_my_bday:
        send_bday_closest_to_my_bday(message)
    elif message.text == text_for_btn_find_bday_of_char:
        send_bday_of_char(message)
    elif message.text == "Вернуться в главное меню":
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=main_menu())

    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help или /about")


def send_birthday_msg(name):
    bot.send_message("@birthdaysGenshin",
                     "<b>{name}</b> сегодня празднует свой день рождения!".format(name=name))
    # когда будет пак картинок для сообщений, надо заменить send_message на send_photo
    # bot.send_photo("@birthdaysGenshin", photo, caption='желаемый текст')


def send_hello_msg(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj9pi-XwJ6DuPzfFzrNhgFAo74cNd6gACPw8AAnqS-EtUlG9v__OqzSkE')


def send_closest_bday(message):
    bot.send_message(message.chat.id, 'Эта функция в процессе разработки ⚙️')


def send_that_month_bdays(message):
    bot.send_message(message.chat.id, '⚙ Эта функция в процессе разработки ⚙️')


def send_selected_month_bdays(message):
    bot.send_message(message.chat.id, text="Какой месяц интересует?", reply_markup=month_menu())


def send_bday_closest_to_my_bday(message):
    bot.send_message(message.chat.id, '⚙ Эта функция очень нескоро будет готова 😢️')


def send_bday_of_char(message):
    bot.send_message(message.chat.id, 'Я бы с радостью рассказал, но пока не умею 😢️')


def main_menu():
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_keyboard.row_width = 2
    btn_hello = types.KeyboardButton(text_for_btn_hello)
    btn_closest_bday = types.KeyboardButton(text_for_btn_closest_bday)
    btn_bdays_that_month = types.KeyboardButton(text_for_btn_that_month_bdays)
    btn_bdays_selected_month = types.KeyboardButton(text_for_btn_selected_month_bdays)
    btn_bday_closest_to_my_bday = types.KeyboardButton(text_for_btn_bday_closest_to_my_bday)
    btn_find_bday_of_char = types.KeyboardButton(text_for_btn_find_bday_of_char)
    main_keyboard.add(btn_hello, btn_closest_bday, btn_bdays_that_month, btn_bdays_selected_month,
                      btn_bday_closest_to_my_bday, btn_find_bday_of_char)
    return main_keyboard


def month_menu():
    month_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_jan = types.KeyboardButton("Январь")
    btn_feb = types.KeyboardButton("Февраль")
    btn_mar = types.KeyboardButton("Март")
    btn_apr = types.KeyboardButton("Апрель")
    btn_may = types.KeyboardButton("Май")
    btn_jun = types.KeyboardButton("Июнь")
    btn_jul = types.KeyboardButton("Июль")
    btn_aug = types.KeyboardButton("Август")
    btn_sep = types.KeyboardButton("Сентябрь")
    btn_oct = types.KeyboardButton("Октябрь")
    btn_nov = types.KeyboardButton("Ноябрь")
    btn_dec = types.KeyboardButton("Декабрь")
    btn_back = types.KeyboardButton("Вернуться в главное меню")
    month_keyboard.add(btn_jan, btn_feb, btn_mar, btn_apr, btn_may, btn_jun, btn_jul, btn_aug, btn_sep,
                       btn_oct, btn_nov, btn_dec, btn_back)
    return month_keyboard


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


thread_time = Thread(target=check_time)  # поток для проверки времени
thread_time.start()

bot.polling(none_stop=True, interval=0)  # поток для проверки сообщений, написанных боту в личку
