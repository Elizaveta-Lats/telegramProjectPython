from methods import *

"""
Здесь методы, отвечающие непосредственно за реагирование бота на сообщения пользователей,
а также потоки, следящие за приходящими в личку бота сообщениями
и следящие за временем, чтобы опубликовать сообщение в канале
"""


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, с моей помощью ты легко сможешь узнать, '
                                      'когда день рождения у того или иного персонажа Genshin Impact 😊',
                     reply_markup=main_menu())
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEFj6Zi-UrjcS6F5m3hXB44mFi_KPDn2wACdw0AAnDa8UsVqatk3kgIuSkE')


@bot.message_handler(commands=['help', 'about'])
def about_handler(message):
    bot.send_message(message.chat.id, 'Привет!\nЗдесь ты можешь узнать, чей день рождения скоро наступит, '
                                      'у кого дни рождения в текущем (или выбранном тобой) месяце. '
                                      'Для этого тебе нужно всего лишь нажать на кнопки внизу!\n\n'
                                      'Кроме того, в этом канале https://t.me/birthdaysGenshin '
                                      'я буду тебе напоминать про дни рождения '
                                      'персонажей Genshin Impact. Переходи туда!', reply_markup=main_menu())


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
    bot.send_message(message.chat.id, text_input_bday)


@bot.message_handler(commands=['findbdayofchar'])
def find_bday_of_char_handler(message):
    send_alphabet(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == 'jan':
            send_bdays_of_selected_month(call, 'Январь')
        elif call.data == 'feb':
            send_bdays_of_selected_month(call, 'Февраль')
        elif call.data == 'mar':
            send_bdays_of_selected_month(call, 'Март')
        elif call.data == 'apr':
            send_bdays_of_selected_month(call, 'Апрель')
        elif call.data == 'may':
            send_bdays_of_selected_month(call, 'Май')
        elif call.data == 'jun':
            send_bdays_of_selected_month(call, 'Июнь')
        elif call.data == 'jul':
            send_bdays_of_selected_month(call, 'Июль')
        elif call.data == 'aug':
            send_bdays_of_selected_month(call, 'Август')
        elif call.data == 'sep':
            send_bdays_of_selected_month(call, 'Сентябрь')
        elif call.data == 'oct':
            send_bdays_of_selected_month(call, 'Октябрь')
        elif call.data == 'nov':
            send_bdays_of_selected_month(call, 'Ноябрь')
        elif call.data == 'dec':
            send_bdays_of_selected_month(call, 'Декабрь')
        # дальше блок проверок, охватывающих функционал поиска ДР персонажа
        elif len(call.data) == 1:
            send_list_of_chars(call)
        elif call.data == 'back':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Выберите первую букву имени персонажа', reply_markup=alphabet_menu())
        else:  # сюда улетит, когда выбрано имя
            send_bday_of_char(call)
    except telebot.apihelper.ApiTelegramException:
        # если человек 2 раза подряд нажмет на одну и ту же кнопку, бот выбрасывает исключение
        bot.answer_callback_query(call.id, 'Не нажимай дважды на одну и ту же кнопку, пожалуйста')
        pass


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == text_for_btn_hello or message.text.lower() == 'hello' or message.text.lower() == 'привет':
        send_hello_msg(message)
    elif message.text == text_for_btn_closest_bday:
        send_closest_bday(message)
    elif message.text == text_for_btn_that_month_bdays:
        send_that_month_bdays(message)
    elif message.text == text_for_btn_selected_month_bdays:
        send_month_menu(message)
    elif message.text == text_for_btn_bday_closest_to_my_bday:
        bot.send_message(message.chat.id, text_input_bday)
    elif message.text == text_for_btn_find_bday_of_char:
        send_alphabet(message)
    else:
        try:
            input_bday = message.text.split('.')
            send_bday_closest_to_my_bday(message, date(2020, int(input_bday[1]), int(input_bday[0])))
        except Exception:
            bot.send_message(message.chat.id, 'Я тебя не понимаю. Напиши /help или /about '
                                              '(либо введи корректно дату рождения в формате дд.мм (например, 01.03))')


def handler(event, _):
    message = telebot.types.Update.de_json(event['body'])
    bot.process_new_updates([message])
