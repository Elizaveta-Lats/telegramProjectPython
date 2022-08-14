from datetime import datetime
import time
bday = datetime(2022, 8, 13, 22, 5, 0)
while True:
    if datetime.now().month == bday.month and datetime.now().day == bday.day and datetime.now().hour == bday.hour\
            and datetime.now().minute == bday.minute and datetime.now().second == bday.second:
        print(1)
        time.sleep(70)

# потом это всё надо внести в основной код
