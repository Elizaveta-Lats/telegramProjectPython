from telebot import types

birthdays_and_names = {'09.01': ["Тома"],
                       '18.01': ["Диона"],
                       '24.01': ["Розария"],
                       '14.02': ["Бэй Доу"],
                       '22.02': ["Кокоми"],
                       '29.02': ["Беннет"],
                       '03.03': ["Ци Ци"],
                       '10.03': ["Шэнь Хэ"],
                       '14.03': ["Джинн"],
                       '21.03': ["Ноэлль"],
                       '26.03': ["Аято"],
                       '04.04': ["Элой"],
                       '17.04': ["Сяо"],
                       '20.04': ["Е Лань"],
                       '30.04': ["Дилюк"],
                       '03.05': ["Кандакия"],
                       '08.05': ["Коллеи"],
                       '18.05': ["Горо"],
                       '21.05': ["Юнь Цзинь"],
                       '27.05': ["Фишль"],
                       '01.06': ["Итто", "Паймон"],
                       '09.06': ["Лиза"],
                       '16.06': ["Венти"],
                       '21.06': ["Ёимия"],
                       '23.06': ["Сайно"],
                       '26.06': ["Райдэн"],
                       '27.06': ["Яэ Мико"],
                       '05.07': ["Барбара"],
                       '14.07': ["Сара"],
                       '15.07': ["Ху Тао"],
                       '20.07': ["Тарталья"],
                       '24.07': ["Хэйдзо"],
                       '27.07': ["Кли", "Куки Синобу"],
                       '28.07': ["Янь Фэй"],
                       '10.08': ["Эмбер"],
                       '26.08': ["Нин Гуан"],
                       '31.08': ["Мона"],
                       '07.09': ["Чун Юнь"],
                       '09.09': ["Рэйзор"],
                       '13.09': ["Альбедо"],
                       '28.09': ["Аяка"],
                       '09.10': ["Син Цю"],
                       '16.10': ["Синь Янь"],
                       '19.10': ["Саю"],
                       '25.10': ["Эола"],
                       '29.10': ["Кадзуха"],
                       '02.11': ["Сян Лин"],
                       '20.11': ["Кэ Цин"],
                       '26.11': ["Сахароза"],
                       '30.11': ["Кэйа"],
                       '02.12': ["Гань Юй"],
                       '21.12': ["Дори"],
                       '29.12': ["Тигнари"],
                       '31.12': ["Чжун Ли"],
                       # '15.08': ["Барабашка"]  # строчка исключительно для тестов текущего дня
                       }

alphabet_name_list = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'И', 'К', 'Л', 'М',
                      'Н', 'П', 'Р', 'С', 'Т', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Э', 'Ю', 'Я']

text_for_btn_hello = "👋 Поздороваться"
text_for_btn_closest_bday = "🥳 Ближайший ДР"
text_for_btn_that_month_bdays = "🎉 Дни рождения в этом месяце"
text_for_btn_selected_month_bdays = "🎂 Дни рождения в заданном месяце"
text_for_btn_bday_closest_to_my_bday = "🤔 Узнать, чей ДР ближе всего к моему"
text_for_btn_find_bday_of_char = "🔍 Узнать ДР персонажа"


def create_alphabet_list():
    """
    перебирает все имена в словаре и составляет алфавитный список на их основе
    В будущем этот метод будет использоваться после повторного парсинга,
    чтобы, если что, в алфавит добавилась новая буква
    """
    alphabet_list = []
    for names in birthdays_and_names.values():
        for name in names:
            first_letter = name[0]
            if first_letter not in alphabet_list:
                alphabet_list.append(first_letter)
    alphabet_list.sort()
    # танцы с бубном, чтобы буква Ё встала куда надо...
    yo = alphabet_list.pop(0)
    E_pos = alphabet_list.index('Е')
    change_list = alphabet_list[:E_pos+1]
    change_list.append(yo)
    change_list.extend(alphabet_list[E_pos+1:])
    alphabet_list = change_list
    print(alphabet_list)


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


def alphabet_menu():
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


def char_menu(letter):
    """
    Метод получает букву из алфавита, а затем в словаре ищет все имена, начинающиеся на эту букву,
    и добавляет их в список. После этого на основе списка формируется набор кнопок
    """
    char_keyboard = types.InlineKeyboardMarkup()

    names_list = []
    for names in birthdays_and_names.values():
        for name in names:
            first_letter = name[0]
            if first_letter == letter:
                names_list.append(name)

    names_list.sort()

    for name in names_list:
        char_keyboard.add(types.InlineKeyboardButton(name, callback_data=name))

    char_keyboard.add(types.InlineKeyboardButton("Вернуться назад", callback_data="back"))

    return char_keyboard


def btn_back_to_start():
    one_btn = types.InlineKeyboardMarkup()
    one_btn.add(types.InlineKeyboardButton("Вернуться в начало", callback_data="back"))
    return one_btn
