from telebot import types

text_for_btn_hello = "👋 Поздороваться"
text_for_btn_closest_bday = "🥳 Ближайший ДР"
text_for_btn_that_month_bdays = "🎉 Дни рождения в этом месяце"
text_for_btn_selected_month_bdays = "🎂 Дни рождения в заданном месяце"
text_for_btn_bday_closest_to_my_bday = "🤔 Узнать, чей ДР ближе всего к моему"
text_for_btn_find_bday_of_char = "🔍 Узнать ДР персонажа"


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


def char_menu():
    print("В разработке...")
