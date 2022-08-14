from datetime import datetime
import time

birthdays_and_greetings = [[datetime(2022, 8, 14, 13, 30, 0), datetime(2022, 8, 14, 13, 31, 0)],
                           ["ДР 1", "ДР 2"]]

birthdays = birthdays_and_greetings[0]
while True:
    for bday in birthdays:
        if datetime.now().month == bday.month and datetime.now().day == bday.day and datetime.now().hour == bday.hour\
                and datetime.now().minute == bday.minute and datetime.now().second == bday.second:
            print(1)
            time.sleep(60)  # отслеживать милисекунды у меня не вышло,
            # поэтому вот такое засыпание, чтобы он только 1 раз написал

# потом это всё надо внести в основной код
