from config import SENDER, PASS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

message = """~~~~~~~~~~~~~~~~~~~~~~~~~\n
1) Закуска <b>"Мясные кнуты"</b> 1шт: 228р\n
2) Закуска <b>"Палочки из тунца"</b> 1шт: 165р\n
3) Лимонад <b>"Классический"</b> 1шт: 85р\n
4) Лимонад <b>"Клубничный"</b> 1шт: 85р\n
5) Пиво <b>"Вайсберг"</b> 5.5л: 819р\n
6) Пиво <b>"Гагарин"</b> 3.0л: 378р\n
7) Пиво <b>"Домашнее"</b> 2.5л: 240р\n
8) Пиво <b>"Моряк"</b> 2.0л: 252р\n
9) Пиво <b>"Регион 82"</b> 1.5л: 151р\n
10) Пиво <b>"Стаут"</b> 1.5л: 189р\n
11) Пиво <b>"Хорватское"</b> 2.0л: 252р\n
12) Пиво <b>"Чешское Элитное"</b> 2.5л: 372р\n
13) Пиво <b>"Штормовое"</b> 2.5л: 310р\n
14) Полторашка <b>"CitrusHit Bochkari"</b> 1шт: 111р\n
15) Сидр <b>"Голубая лагуна"</b> 1.0л: 127р\n
16) Сидр <b>"Манго-маракуйя"</b> 3.0л: 381р\n
17) Сухарики <b>"Краб"</b> 100гр: 55р\n
18) Сухарики <b>"Тайский перец"</b> 200гр: 110р\n
19) Энергетик <b>"TARGET ACTIVE"</b> 1шт: 95р\n
20) 1.5л X 12 = 180р\n
21) 1л X 9 = 315р\n
~~~~~~~~~~~~~~~~~~~~~~~~~\n
Доставка: 200р\n
Тара: 315р\n
Итого: 4920р\n
Номер для связи: 79155633989
"""

# message = "~~~~~~~~~~~~~~~~~~~~~~~~~\n" \
#           "1) Закуска <b>'Мясные кнуты'</b> 1шт: 228р"

subject = "Заказ для Kirill оформлен\n"


def send_email(message, subject):
    message = message.replace('<b>', '').replace('</b>', '')
    clear_message = f"Subject: {subject}{message}".encode('UTF-8')

    sender = SENDER
    password = PASS

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        server.sendmail(sender, 'kruzkapennogo@gmail.com', clear_message)

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\n Check your login or password please!"


print(send_email(message, subject))
