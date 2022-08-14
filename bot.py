from datetime import datetime
from decouple import config
import telebot
import time

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN)

# надо заполнить список датами и поздравлениями
birthdays_and_greetings = [[datetime(2022, 8, 14, 14, 18), datetime(2022, 8, 14, 14, 15)],
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
    bot.send_message("@birthdaysGenshin", greeting)


birthdays = birthdays_and_greetings[0]
while True:
    for bday in birthdays:
        if datetime.now().month == bday.month and datetime.now().day == bday.day and datetime.now().hour == bday.hour\
                and datetime.now().minute == bday.minute and datetime.now().second == bday.second:
            index = birthdays.index(bday)
            send_birthday_msg(index)
            time.sleep(60)  # отслеживать микросекунды у меня не вышло (видимо, не успевает поймать момент),
            # поэтому вот такое засыпание, чтобы он только 1 раз написал

bot.polling(none_stop=True, interval=0)  # не реагирует, поскольку цикл while занял весь поток.
# Надо разобраться, как сделать второй поток для этого метода
