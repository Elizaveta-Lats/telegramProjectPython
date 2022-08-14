from datetime import date

from decouple import config
import schedule
import telebot
import time

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
index = -1
bot = telebot.TeleBot(TOKEN)

# надо заполнить список датами и поздравлениями
birthdays_and_greetings = [[date(2023, 8, 13), date(2022, 8, 14)],
                           ["ДР 1", "ДР 2"]]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Привет, в этом канале https://t.me/birthdaysGenshin "
                                               "я буду тебе напоминать про дни рождения "
                                               "персонажей Genshin Impact. Переходи туда!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help")


def send_birthday_msg():
    greeting = birthdays_and_greetings[1][index]
    bot.send_message("@birthdaysGenshin", greeting)


schedule.every().day.at("21:32").do(send_birthday_msg)
birthdays = birthdays_and_greetings[0]
while True:  # этот цикл отсчитывает время. Он обязателен.
    for birthday in birthdays:
        if date.today().day == birthday.day and date.today().month == birthday.month:
            index = birthdays.index(birthday)
            schedule.run_pending()
    time.sleep(28)
bot.polling(none_stop=True, interval=0)  # не реагирует, поскольку цикл while занял весь поток.
# Надо разобраться, как сделать второй поток для этого метода