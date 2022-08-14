from datetime import datetime, date, time
from decouple import config
from threading import Thread
import telebot
from telebot import types
import time as timer

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN)

time_of_msg = time(0, 10)  # 00:10:00 по МСК, время, после которого нужно публиковать сообщения

birthdays_and_names = {'01-06': ["Итто", "Паймон"], '24-07': ["Сиканоин Хэйдзо"], '15-08': ["Коллеи"]}


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, 'Привет, когда я вырасту, я буду сообщать про ДР персонажей геншина',
                     reply_markup=markup)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj6Zi-UrjcS6F5m3hXB44mFi_KPDn2wACdw0AAnDa8UsVqatk3kgIuSkE')


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "В этом канале https://t.me/birthdaysGenshin "
                                      "я буду тебе напоминать про дни рождения "
                                      "персонажей Genshin Impact. Переходи туда!")


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


def send_birthday_msg(name):
    bot.send_message("@birthdaysGenshin", "{name} сегодня празднует свой день рождения!".format(name=name))
    # когда будет пак картинок для сообщений, надо заменить send_message на send_photo
    # bot.send_photo("@birthdaysGenshin", photo, caption='желаемый текст')


def check_time():
    """
    Метод постоянно прокручивает массив дней рождений.
    Когда находит совпадение по дате, проверяет время.
    Если оно больше или равно заданного в переменной и сегодня он еще не публиковал ничего,
    тогда метод публикует сообщение на канале и делает отметку, что он это сделал.
    Отметка сбрасывается при наступлении следующего дня
    """
    day1 = ''
    is_msg_sent = False
    while True:
        today = date.today().strftime("%d-%m")
        if day1 != today:
            day1 = today
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
