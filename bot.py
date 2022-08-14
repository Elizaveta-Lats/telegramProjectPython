from datetime import datetime, date, time
from decouple import config
import telebot
import time as timer

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN)

time_of_msg = time(10)  # 10:00:00 по МСК, время публикации сообщений

birthdays_and_greetings = [[datetime.combine(date(2022, 8, 14), time_of_msg),
                            datetime.combine(date(2022, 8, 14), time(15, 22))
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


birthdays = birthdays_and_greetings[0]
while True:
    for birthday in birthdays:
        bday = str(birthday)[5:]
        now = str(datetime.now())[5:19]
        if bday == now:
            index = birthdays.index(birthday)
            send_birthday_msg(index)
            timer.sleep(60)  # отслеживать микросекунды у меня не вышло (видимо, не успевает поймать момент),
            # поэтому вот такое засыпание, чтобы он только 1 раз написал

bot.polling(none_stop=True, interval=0)  # не реагирует, поскольку цикл while занял весь поток.
# Надо разобраться, как сделать второй поток для этого метода
