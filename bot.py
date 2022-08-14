from datetime import datetime, date, time
from decouple import config
from threading import Thread
import telebot
import time as timer

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN)

time_of_msg = time(10)  # 10:00:00 по МСК, время публикации сообщений

birthdays_and_greetings = [[datetime.combine(date(2022, 8, 14), time_of_msg),
                            datetime.combine(date(2022, 8, 14), time(16, 48))
                            ],
                           ["ДР 1", "ДР 2"]]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Привет, в этом канале https://t.me/birthdaysGenshin "
                                               "я буду тебе напоминать про дни рождения "
                                               "персонажей Genshin Impact. Переходи туда!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


def send_birthday_msg(i):
    greeting = birthdays_and_greetings[1][i]
    bot.send_message("@birthdaysGenshin", str(greeting))
    # когда будет пак картинок для сообщений, надо заменить send_message на send_photo
    # bot.send_photo("@birthdaysGenshin", photo, caption='желаемый текст')


birthdays = birthdays_and_greetings[0]


def check_time():
    while True:
        for birthday in birthdays:
            bday = str(birthday)[5:16]
            now = str(datetime.now())[5:16]
            if bday == now:
                index = birthdays.index(birthday)
                send_birthday_msg(index)
                timer.sleep(60)  # сон на 1 минуту


thread_time = Thread(target=check_time)  # поток для проверки времени
thread_time.start()

bot.polling(none_stop=True, interval=0)  # поток для проверки сообщений, написанных боту в личку
