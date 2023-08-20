from telebot import types

alphabet_name_list = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'И', 'К', 'Л', 'М',
                      'Н', 'П', 'Р', 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Э', 'Ю', 'Я']

text_for_btn_hello = "👋 Поздороваться"
text_for_btn_closest_bday = "🥳 Ближайший ДР"
text_for_btn_that_month_bdays = "🎉 Дни рождения в этом месяце"
text_for_btn_selected_month_bdays = "🎂 Дни рождения в заданном месяце"
text_for_btn_bday_closest_to_my_bday = "🤔 Узнать, чей ДР ближе всего к моему"
text_for_btn_find_bday_of_char = "🔍 Узнать ДР персонажа"


def main_menu():
    """ создает меню с кнопками-функциями бота """
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
    """ создает инлайн клавиатуру с месяцами """
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


def alphabet_menu():
    """ создает инлайн клавиатуру с алфавитом """
    button_list = []
    row = []
    """
    Для того, чтобы кнопки выстроились таблицей, они должны находиться в формате списка списков,
    где внутренние списки - ряд кнопок. 
    Если просто по одной кнопке добавлять, то каждая окажется в отдельном списке, 
    из-за чего всё выстраивается в 1 колонку. Поэтому надо самим создать список списков
    """
    for letter in alphabet_name_list:
        if (alphabet_name_list.index(letter)+1) % 4 != 0:
            row.append(types.InlineKeyboardButton(letter, callback_data=letter))
        else:
            row.append(types.InlineKeyboardButton(letter, callback_data=letter))
            button_list.append(row)
            row = []
    for letter in alphabet_name_list:
        row.append(types.InlineKeyboardButton(letter, callback_data=letter))
    alphabet_keyboard = types.InlineKeyboardMarkup(button_list)
    return alphabet_keyboard


def btn_back_to_start():
    """ создает инлайн клавиатуру с кнопкой "Вернуться в начало" """
    one_btn = types.InlineKeyboardMarkup()
    one_btn.add(types.InlineKeyboardButton("Вернуться в начало", callback_data="back"))
    return one_btn

# def create_alphabet_list():
#     """
#     перебирает все имена в словаре и составляет алфавитный список на их основе
#     В будущем этот метод будет использоваться после повторного парсинга,
#     чтобы, если что, в алфавит добавилась новая буква
#     """
#     alphabet_list = []
#     for names in birthdays_and_names.values():
#         for name in names:
#             first_letter = name[0]
#             if first_letter not in alphabet_list:
#                 alphabet_list.append(first_letter)
#     alphabet_list.sort()
#     # танцы с бубном, чтобы буква Ё встала куда надо...
#     yo = alphabet_list.pop(0)
#     E_pos = alphabet_list.index('Е')
#     change_list = alphabet_list[:E_pos+1]
#     change_list.append(yo)
#     change_list.extend(alphabet_list[E_pos+1:])
#     alphabet_list = change_list
#     print(alphabet_list)
