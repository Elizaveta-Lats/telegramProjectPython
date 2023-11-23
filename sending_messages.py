import os
from datetime import date
import telebot
import sqlite3
import time as timer

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('/function/storage/tg-bot-account/database.db', check_same_thread=False)
cursor = conn.cursor()


def send_birthday_msg(name):
    """ публикует запись в канале о том, что некий персонаж празднует свой день рождения """
    bot.send_message('@birthdaysGenshin',
                     '<b>{name}</b> сегодня празднует свой день рождения!'.format(name=name), parse_mode='html')
    # когда будет пак картинок для сообщений, надо заменить send_message на send_photo
    # bot.send_photo('@birthdaysGenshin', photo, caption='желаемый текст')


def handler(event, _):
    today = date.today()
    if int(today.day) == 28 and int(today.month) == 2 and int(today.year) % 4 != 0:
        cursor.execute('SELECT name FROM birthdays WHERE bday = "2020-02-28" OR bday = "2020-02-29"')
    else:
        cursor.execute(f'SELECT name FROM birthdays WHERE bday = "{str(date(2020, int(today.month), int(today.day)))}"')
    characters = cursor.fetchall()  # лист кортежей
    if len(characters) > 0:
        names = []
        for char in characters:
            names.append(char[0])
        for name in names:
            send_birthday_msg(name)
            timer.sleep(5)
