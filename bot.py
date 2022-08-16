from datetime import datetime, date, time
from decouple import config
from threading import Thread
import telebot
from telebot import types
import time as timer
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# в 2:00 по МСК (в 0:00 по времени сервера Европы (GMT+1)) присылаются письма от персонажей
TOKEN = config('token', default='')
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

time_of_msg = time(23, 10)  # 23:10:00 по МСК, время, после которого нужно публиковать сообщения

birthdays_and_names = {'09.01': ["Тома"],
                       '14.02': ["Бэй Доу"],
                       '03.03': ["Ци Ци"],
                       '04.04': ["Элой"],
                       '21.05': ["Юнь Цзинь"],
                       '01.06': ["Итто", "Паймон"],
                       '09.06': ["Лиза"],
                       '14.07': ["Кудзё Сара"],
                       '24.07': ["Сиканоин Хэйдзо"],
                       '15.08': ["Коллеи", "Тигнари"],
                       '26.08': ["Нин Гуан"],
                       '09.09': ["Рэйзор"],
                       '25.10': ["Эола"],
                       '30.11': ["Кэйа"],
                       '02.12': ["Гань Юй"]}

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
    send_month_menu(message)


@bot.message_handler(commands=['bdayclosesttomybday'])
def bdays_closest_to_my_bday_handler(message):
    send_bday_closest_to_my_bday(message)


@bot.message_handler(commands=['findbdayofchar'])
def find_bday_of_char_handler(message):
    send_bday_of_char(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == "jan":
            send_bdays_of_selected_month(call, "Январь")
        elif call.data == "feb":
            send_bdays_of_selected_month(call, "Февраль")
        elif call.data == "mar":
            send_bdays_of_selected_month(call, "Март")
        elif call.data == "apr":
            send_bdays_of_selected_month(call, "Апрель")
        elif call.data == "may":
            send_bdays_of_selected_month(call, "Май")
        elif call.data == "jun":
            send_bdays_of_selected_month(call, "Июнь")
        elif call.data == "jul":
            send_bdays_of_selected_month(call, "Июль")
        elif call.data == "aug":
            send_bdays_of_selected_month(call, "Август")
        elif call.data == "sep":
            send_bdays_of_selected_month(call, "Сентябрь")
        elif call.data == "oct":
            send_bdays_of_selected_month(call, "Октябрь")
        elif call.data == "nov":
            send_bdays_of_selected_month(call, "Ноябрь")
        elif call.data == "dec":
            send_bdays_of_selected_month(call, "Декабрь")
    except telebot.apihelper.ApiTelegramException:
        # если человек 2 раза подряд нажмет на одну и ту же кнопку, бот выбрасывает исключение, вот и ловим его
        bot.answer_callback_query(call.id, "Не нажимай дважды на одну и ту же кнопку, пожалуйста")
        pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == text_for_btn_hello or message.text.lower() == "hello" or message.text.lower() == "привет":
        send_hello_msg(message)
    elif message.text == text_for_btn_closest_bday:
        send_closest_bday(message)
    elif message.text == text_for_btn_that_month_bdays:
        send_that_month_bdays(message)
    elif message.text == text_for_btn_selected_month_bdays:
        send_month_menu(message)
    elif message.text == text_for_btn_bday_closest_to_my_bday:
        send_bday_closest_to_my_bday(message)
    elif message.text == text_for_btn_find_bday_of_char:
        send_bday_of_char(message)
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
    current_month = str(date.today())[5:7]
    names_of_chars = "Дни рождения в этом месяце:\n\n"
    for key in birthdays_and_names.keys():
        month = key[3:]
        if current_month == month:
            names = birthdays_and_names[key]
            names_one_day = ""
            for name in names:
                if len(names) > 1:
                    names_one_day += name + ", "
            if names_one_day == "":
                names_of_chars += "{bday}: {name}\n".format(bday=key, name=names[0])
            else:
                names_one_day = names_one_day[:-2]
                names_of_chars += "{bday}: {name}\n".format(bday=key, name=names_one_day)
    bot.send_message(message.chat.id, names_of_chars)


def send_month_menu(message):
    bot.send_message(message.chat.id, text="Какой месяц интересует?", reply_markup=month_menu())


def send_bday_closest_to_my_bday(message):
    bot.send_message(message.chat.id, '⚙ Эта функция очень нескоро будет готова 😢️')


def send_bday_of_char(message):
    # для этой фичи надо тоже инлайн кнопки сделать (которые должны будут динамически формироваться на основе словаря)
    bot.send_message(message.chat.id, 'Я бы с радостью рассказал, но пока не умею 😢️')


def send_bdays_of_selected_month(call, month):
    # придумать, как перегонять текстовый формат месяца в числовой ("январь" -> "01"). Мб с помощью словаря
    month = morph.parse(month)[0]
    month_loct = month.inflect({'loct'})
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Дни рождения в {month}".format(month=month_loct.word),
                          reply_markup=month_menu())


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
    month_keyboard = types.InlineKeyboardMarkup()
    month_keyboard.row_width = 3
    btn_jan = types.InlineKeyboardButton("Январь", callback_data="jan")
    btn_feb = types.InlineKeyboardButton("Февраль", callback_data="feb")
    btn_mar = types.InlineKeyboardButton("Март", callback_data="mar")
    btn_apr = types.InlineKeyboardButton("Апрель", callback_data="apr")
    btn_may = types.InlineKeyboardButton("Май", callback_data="may")
    btn_jun = types.InlineKeyboardButton("Июнь", callback_data="jun")
    btn_jul = types.InlineKeyboardButton("Июль", callback_data="jul")
    btn_aug = types.InlineKeyboardButton("Август", callback_data="aug")
    btn_sep = types.InlineKeyboardButton("Сентябрь", callback_data="sep")
    btn_oct = types.InlineKeyboardButton("Октябрь", callback_data="oct")
    btn_nov = types.InlineKeyboardButton("Ноябрь", callback_data="nov")
    btn_dec = types.InlineKeyboardButton("Декабрь", callback_data="dec")
    month_keyboard.add(btn_jan, btn_feb, btn_mar, btn_apr, btn_may, btn_jun, btn_jul, btn_aug, btn_sep,
                       btn_oct, btn_nov, btn_dec)
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
