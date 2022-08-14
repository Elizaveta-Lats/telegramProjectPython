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

birthdays_and_names = {'01.06': ["Итто", "Паймон"], '24.07': ["Сиканоин Хэйдзо"], '15.08': ["Коллеи"]}


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_hello = types.KeyboardButton("👋 Поздороваться")
    btn_closest_bday = types.KeyboardButton("❓ Ближайший день рождения")
    btn_bdays_that_month = types.KeyboardButton("🎉 Дни рождения в этом месяце")
    btn_bdays_selected_month = types.KeyboardButton("🎂 Дни рождения в заданном месяце")
    markup.add(btn_hello, btn_closest_bday, btn_bdays_that_month, btn_bdays_selected_month)

    bot.send_message(message.chat.id, 'Привет, когда я вырасту, я буду сообщать про ДР персонажей геншина',
                     reply_markup=markup)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj6Zi-UrjcS6F5m3hXB44mFi_KPDn2wACdw0AAnDa8UsVqatk3kgIuSkE')


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "В этом канале https://t.me/birthdaysGenshin "
                                      "я буду тебе напоминать про дни рождения "
                                      "персонажей Genshin Impact. Переходи туда!")


@bot.message_handler(content_types=['text'])
# потом, наверное, распихаю по отдельным хэндлерам и создам команды для всех этих функций
# а мб заменю потом на inline кнопки, хотя бы часть из них
def get_text_messages(message):
    if message.text == "👋 Поздороваться":
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj9pi-XwJ6DuPzfFzrNhgFAo74cNd6gACPw8AAnqS-EtUlG9v__OqzSkE')
    elif message.text == "❓ Ближайший день рождения":
        bot.send_message(message.chat.id, 'Эта функция в процессе разработки ⚙️')
    elif message.text == "🎉 Дни рождения в этом месяце":
        bot.send_message(message.chat.id, '⚙ Эта функция в процессе разработки ⚙️')
    elif message.text == "🎂 Дни рождения в заданном месяце":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
        markup.add(btn_jan, btn_feb, btn_mar, btn_apr, btn_may, btn_jun, btn_jul, btn_aug, btn_sep,
                   btn_oct, btn_nov, btn_dec, btn_back)
        bot.send_message(message.chat.id, text="Какой месяц интересует?", reply_markup=markup)
    elif message.text == "Январь" or message.text == "Февраль" or message.text == "Март" or message.text == "Апрель"\
            or message.text == "Май" or message.text == "Июнь" or message.text == "Июль" or message.text == "Август"\
            or message.text == "Сентябрь" or message.text == "Октябрь" or message.text == "Ноябрь"\
            or message.text == "Декабрь":
        bot.send_message(message.chat.id, 'Да, это тоже в процессе разработки ⚙️')
    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_hello = types.KeyboardButton("👋 Поздороваться")
        btn_closest_bday = types.KeyboardButton("❓ Ближайший день рождения")
        btn_bdays_that_month = types.KeyboardButton("🎉 Дни рождения в этом месяце")
        btn_bdays_selected_month = types.KeyboardButton("🎂 Дни рождения в заданном месяце")
        markup.add(btn_hello, btn_closest_bday, btn_bdays_that_month, btn_bdays_selected_month)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help")


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
