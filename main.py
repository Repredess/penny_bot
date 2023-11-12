import datetime
import sqlite3
import smtplib
from telebot import types
import telebot
import time
import os
import random
from config import BOT_TOKEN, URL, ANSWERS, ADMIN_ID, ANNOUNCEMENT, SAY, DELIVERY, INTRODUCE, SENDER, PASS, ADMINS, \
    BAN_LIST
from assortiment import beer, cidre, crackers, knuts, fish, cheese, lemonade, energize, sodie_pop, bottle_price
from nick_names import NICK

"""
Что бы бот заработал - следует создать файл config.py в корневой папке проекта и задать там переменную BOT_TOKEN
содержащую токен Вашего бота. Так же можно создать переменную URL в которой указывается нужный Вам сайт.
В переменной ANNOUNCEMENT можно включать и отключать извещения.

Что бы добавить или изменить кнопку надо добавить товар связанный с ней в нужный раздел словаря в assortiment.py,
а затем изменить функцию chooseНУЖНЫЙ_ТОВАР так, что бы у кнопки было такое же название что и у в словаре. 
Так же рекомендуется загрузить фотографию по соответствующему разделу. Название фотографии должно соответствовать
названию кнопки.

Команды для бота:
start - Вернуться к началу
help - Увидеть все команды
site - Перейти на сайт
generate -  Сгенерировать рофл
write - Записать общую корзину в КЭШ (перед отключением или рестартом сервера)
read - Записать КЭШ в корзину (после включения сервера)
zakaz - Оформление заказа

Нужно добавить:

Рассылка акций и новинок пользователям

Рассылку новых предложений пользователям - через кнопку настройки которая будет отображаться только у админов. 
Нужно будет отправить фотку для рассылки, сообщение для рассылки посмотреть как это будет выглядеть и разослать
всем пользователям из таблицы login_id

Загрузить бота на сервер
"""

pennij_bot = telebot.TeleBot(BOT_TOKEN)

# cart = {1626668178: {'Пиво Вайсберг': 5.5, 'Пиво Гагарин': 3.0, 'Пиво Стаут': 1.5, 'Пиво Регион 82': 1.5,
#                      'Пиво Хорватское': 2.0, 'Пиво Штормовое': 2.5, 'Пиво Домашнее': 2.5, 'Пиво Чешское Элитное': 2.5,
#                      'Пиво Моряк': 2.0, 'Сидр Голубая лагуна': 1.0, 'Сидр Манго-маракуйя': 3.0,
#                      'Сухарики Тайский перец': 0.2, 'Сухарики Краб': 0.1, 'Закуска Палочки из тунца': 1,
#                      'Закуска Мясные кнуты': 1, 'Лимонад Клубничный': 1, 'Лимонад Классический': 1,
#                      'Энергетик TARGET ACTIVE': 1, 'Полторашка CitrusHit Bochkari': 1},
#         1626668178: {'Пиво Вайсберг': 5.5, 'Полторашка CitrusHit Bochkari': 1}
#         }

cart = {}

DIR = "memes"

"""Раздел с командами"""


@pennij_bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🍻 Ассортимент 🐟')
    btn2 = types.KeyboardButton('🛟 Помощь')
    btn3 = types.KeyboardButton('📄 Контакты')
    markup.row(btn1)
    markup.row(btn2, btn3)

    connect = sqlite3.connect('shop.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    chat_id INTEGER,
    user_name TEXT,
    user_id INTEGER,
    reg_date TEXT,
    last_date TEXT);
    """)

    connect.commit()

    chat_id = message.chat.id
    user_name = message.from_user.first_name
    reg_date = " ".join(str(datetime.datetime.now()).split('.')[0:-1])
    if message.from_user.username:
        user_name += f' "{message.from_user.username}"'
    if message.from_user.last_name:
        user_name += f' {message.from_user.last_name}'
    user_id = message.from_user.id
    last_date = " ".join(str(datetime.datetime.now()).split('.')[0:-1])
    cursor.execute(f"SELECT chat_id FROM login_id WHERE chat_id = {chat_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO login_id VALUES(?,?,?,?,?);", (chat_id,
                                                                   user_name,
                                                                   user_id,
                                                                   reg_date,
                                                                   last_date))
        connect.commit()

        pennij_bot.send_message(message.chat.id,
                                f"Приветствуем вас, {message.from_user.first_name} в онлайн магазине — Кружка Пенного!"
                                f"\nЗаказы принимаем с 10:00 до 21:00 ежедневно!"
                                f"\nЗаказы оформленные в после 21:00 — обрабатываются на следующий день."
                                f"\nКак получить заказ:"
                                f"\n— Заказ оформляется по телефону из раздела 'Контакты' в главном меню "
                                f"или с помощью бота;"
                                f"\n— Процесс заказа через бота: добавляем все нужные товары и оформляем заказ "
                                f"в разделе 'Корзина';"
                                "\n— Доставка по Керчи 200р.",
                                parse_mode='html', reply_markup=markup)
    else:
        cursor.execute("UPDATE login_id SET last_date = ? WHERE chat_id = ?", (reg_date, chat_id))
        connect.commit()

        pennij_bot.send_message(message.chat.id,
                                f"Привет, <b>{message.from_user.first_name}</b>! "
                                f"Здесь можно заказать <b>пиво и рыбку</b> через приложение или по телефону ;)"
                                f"\nНомер для связи находится в разделе: 📄 Контакты",
                                parse_mode='html', reply_markup=markup)


@pennij_bot.message_handler(commands=["to_all"])
def to_all(message):
    if message.chat.id == ADMIN_ID:
        pass


@pennij_bot.message_handler(commands=["write"])
def write(message):
    global cart
    try:
        if message.from_user.id == ADMIN_ID:
            with open('cache.txt', 'w') as file:
                for key, value in cart.items():
                    file.write(f"{key}:{value}\n")
            pennij_bot.send_message(message.chat.id, 'Кэш успешно создан!')
        else:
            raise ValueError
    except ValueError:
        user_name = "EMPTY_USERNAME"
        if message.from_user.username:
            user_name = message.from_user.username
        pennij_bot.send_message(message.chat.id, f'{message.from_user.first_name}:{message.chat.id} пытался '
                                                 f'использовать команду /write! @{user_name}')
        pennij_bot.send_message(message.chat.id, 'У Вас нет доступа к этой команде!')


@pennij_bot.message_handler(commands=["read"])
def read(message):
    global cart
    if message.from_user.id == ADMIN_ID:
        try:
            with open('cache.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, value = line.strip().split(':', maxsplit=1)
                    if int(key) not in cart:
                        cart[int(key)] = eval(value)
            pennij_bot.send_message(message.chat.id, 'Корзина успешно обновлена из кэша!')
        except FileNotFoundError:
            pennij_bot.send_message(message.chat.id, 'Корзина НЕ обновлена из кэша!')
    else:
        user_name = "EMPTY_USERNAME"
        if message.from_user.username:
            user_name = message.from_user.username
        pennij_bot.send_message(message.chat.id, f'{message.from_user.first_name}:{message.chat.id} пытался '
                                                 f'использовать команду /read! @{user_name}')
        pennij_bot.send_message(message.chat.id, 'У Вас нет доступа к этой команде!')


@pennij_bot.message_handler(commands=["zakaz"])
def commandOrder(message):
    if message.chat.id in cart:
        if cart[message.chat.id]:
            placing_an_order(message)
    else:
        pennij_bot.send_message(message.chat.id, 'Корзина пуста')


@pennij_bot.message_handler(commands=["generate"])
def generateNickname(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/generate')
    btn2 = types.KeyboardButton('/start')
    markup.row(btn1, btn2)
    nm_p = os.path.join(DIR, random.choice(os.listdir(DIR)))
    random.shuffle(NICK)
    nick = random.choice(NICK)
    pic = open(nm_p, 'rb')
    print(message.from_user.first_name, nm_p, nick, datetime.datetime.now())
    pennij_bot.send_photo(message.chat.id, pic, f'<b>{nick}</b>', parse_mode='html', reply_markup=markup)


@pennij_bot.message_handler(commands=["site", "website"])
def redirect_to_site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти на сайт", url=URL))
    pennij_bot.send_message(message.chat.id, "Ах да, вот ссылочка:", reply_markup=markup)


@pennij_bot.message_handler(commands=["help"])
def get_help(message):
    pennij_bot.send_message(message.chat.id,
                            "<b>Вернуться в начало</b>: <u>/start</u> "
                            "\n<b>По вопросам неисправностей или сотрудничества:</b> <u>@repredess</u>",
                            parse_mode='html')


"""Раздел с оформлением заказа"""


def placing_an_order(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Да', callback_data='confirm_order'),
               telebot.types.InlineKeyboardButton('Нет', callback_data='cancel_order'))

    pennij_bot.send_message(message.chat.id,
                            'Вы уверены что хотите оформить заказ?', reply_markup=markup)


@pennij_bot.callback_query_handler(func=lambda callback: callback.data == 'confirm_order')
def confirm_order_handler(callback):
    if callback.message.chat.id in cart:
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton('Оставить контакт', request_contact=True)
        btn2 = telebot.types.KeyboardButton('↩️ Назад в меню')
        markup.add(btn1, btn2)

        pennij_bot.answer_callback_query(callback.id, 'Подтверждение заказа')
        pennij_bot.send_message(callback.message.chat.id,
                                'Нажмите кнопку "Оставить контакт" что бы мы могли с тобой связаться',
                                reply_markup=markup)
    else:
        pennij_bot.answer_callback_query(callback.id, 'Корзина пуста')


@pennij_bot.callback_query_handler(func=lambda callback: callback.data == 'cancel_order')
def cancel_order_handler(callback):
    if callback.message.chat.id in cart:
        pennij_bot.answer_callback_query(callback.id, 'Заказ отменен')
        goodsChapter(callback.message)
    else:
        pennij_bot.answer_callback_query(callback.id, 'Корзина пуста')


@pennij_bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.chat.id not in BAN_LIST:
        try:
            order, money = stashCheck(cart[message.chat.id])
            phone = message.contact.phone_number
            write_order(message, phone=phone, order=order, total=money)

            for id in ADMINS:
                pennij_bot.send_message(id, f"Заказ для {message.from_user.first_name} оформлен:\n{order}\n"
                                            f"Номер для связи: {message.contact.phone_number}", parse_mode='html')

            on_email = f"{order}\nНомер для связи: {message.contact.phone_number}\nID чата: {message.chat.id}"
            pennij_bot.send_message(message.chat.id, f'Спасибо за заказ, {message.from_user.first_name}.',
                                    parse_mode='html')
            print(send_email(on_email, subject=f"Заказ для {message.from_user.first_name} оформлен\n"))
            del cart[message.chat.id]
            main_page(message, order=True)
        except KeyError:
            pennij_bot.send_message(message.chat.id, f'Упс, кажется с нашим сервером что то случилось.\n'
                                                     f'Попробуйте заполнить корзину еще раз.')
            main_page(message)
    else:
        pennij_bot.send_message(message.chat.id, f'Вы находитесь в бане. Заказ невозможен', parse_mode='html')


"""Раздел с добавлением товара"""


@pennij_bot.message_handler(func=lambda message: message.text in beer)
def beer_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_liter = telebot.types.InlineKeyboardButton('+1л', callback_data=f'+1.0 Пиво {item}')
    add_poltora = telebot.types.InlineKeyboardButton('+1.5л', callback_data=f'+1.5 Пиво {item}')
    remove_liter = telebot.types.InlineKeyboardButton('-1л', callback_data=f'-1.0 Пиво {item}')
    remove_poltora = telebot.types.InlineKeyboardButton('-1.5л', callback_data=f'-1.5 Пиво {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_liter, add_liter)
    markup_inline.add(remove_poltora, add_poltora)
    if beer[item]["Подробнее"]:
        adress = telebot.types.InlineKeyboardButton('📖 Подробнее', url=beer[item]["Подробнее"])
        markup_inline.add(adress, cart)
    else:
        markup_inline.add(cart)
    try:
        pic = open(f"goods/pivo/{item}.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b> | {beer[item]["Фильтрация"]}</i>'
                                                    f'\n{beer[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nПлостность: {beer[item]["Плотность"]}'
                                                    f'\nАлкоголь: {beer[item]["Алкоголь"]}'
                                                    f'\nЦена: {beer[item]["Цена"]}р/литр',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/pivo/Пиво.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b> | {beer[item]["Фильтрация"]}</i>'
                                                    f'\n{beer[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nПлостность: {beer[item]["Плотность"]}'
                                                    f'\nАлкоголь: {beer[item]["Алкоголь"]}'
                                                    f'\nЦена: {beer[item]["Цена"]}р/литр',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in cidre)
def cidre_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_liter = telebot.types.InlineKeyboardButton('+1л', callback_data=f'+1.0 Сидр {item}')
    add_poltora = telebot.types.InlineKeyboardButton('+1.5л', callback_data=f'+1.5 Сидр {item}')
    remove_liter = telebot.types.InlineKeyboardButton('-1л', callback_data=f'-1.0 Сидр {item}')
    remove_poltora = telebot.types.InlineKeyboardButton('-1.5л', callback_data=f'-1.5 Сидр {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_liter, add_liter)
    markup_inline.add(remove_poltora, add_poltora)
    markup_inline.add(cart)

    try:
        pic = open(f"goods/ciders/{item}.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{cidre[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {cidre[item]["Цена"]}р/литр | '
                                                    f'Алкоголь: {cidre[item]["Алкоголь"]}',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/ciders/Сидры.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{cidre[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {cidre[item]["Цена"]}р/литр | '
                                                    f'Алкоголь: {cidre[item]["Алкоголь"]}',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in knuts)
def knuts_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_one = telebot.types.InlineKeyboardButton('+1шт', callback_data=f'+1 Закуска {item}')
    remove_one = telebot.types.InlineKeyboardButton('-1шт', callback_data=f'-1 Закуска {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_one, add_one)
    markup_inline.add(cart)

    try:
        pic = open(f"goods/knuts/{item}.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{knuts[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {knuts[item]["Цена"]}р/упаковка',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/knuts/Палочки.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{knuts[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {knuts[item]["Цена"]}р/упаковка',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in crackers)
def crackers_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_one = telebot.types.InlineKeyboardButton('+100гр', callback_data=f'+100 Сухарики {item}')
    remove_one = telebot.types.InlineKeyboardButton('-100гр', callback_data=f'-100 Сухарики {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_one, add_one)
    markup_inline.add(cart)

    try:
        pic = open(f"goods/crackers/{item}.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{crackers[item]["Описание"]}'
                                                    f'\nОстрота: {crackers[item]["Острота"]}',
                              f'\n'
                              f'\nЦена: {int(crackers[item]["Цена"] / 10)}р/100гр',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/crackers/crackers.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{crackers[item]["Описание"]}'
                                                    f'\nОстрота: {crackers[item]["Острота"]}'
                                                    f'\n'
                                                    f'\nЦена: {int(crackers[item]["Цена"] / 10)}р/100гр',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in fish)
def fish_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    if fish[item]["Фасовка"] == "Наразвес":
        serving_option = "100гр"
        add_gramms = telebot.types.InlineKeyboardButton('+100гр', callback_data=f'+100 Рыбка {item}')
        remove_gramms = telebot.types.InlineKeyboardButton('-100гр', callback_data=f'-100 Рыбка {item}')
        cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
        markup_inline.add(remove_gramms, add_gramms)
        markup_inline.add(cart)

        try:
            pic = open(f"goods/riba/{item}.jpg", 'rb')
            pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                        f'\n{fish[item]["Описание"]}'
                                                        f'\n'
                                                        f'\nЦена: {int(fish[item]["Цена"] / 10)}р/'
                                                        f'<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')
        except FileNotFoundError:
            pic = open(f'goods/riba/рыба.jpg', 'rb')
            pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                        f'\n{fish[item]["Описание"]}'
                                                        f'\n'
                                                        f'\nЦена: {int(fish[item]["Цена"] / 10)}р/'
                                                        f'<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')
    elif fish[item]["Фасовка"] == "Поштучно":
        serving_option = "1шт"
        if item == "Бычки":
            serving_option = "10шт(фасованый)"
        add_gramms = telebot.types.InlineKeyboardButton('+1шт', callback_data=f'+1 Рыбка {item}')
        remove_gramms = telebot.types.InlineKeyboardButton('-1шт', callback_data=f'-1 Рыбка {item}')
        cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
        markup_inline.add(remove_gramms, add_gramms)
        markup_inline.add(cart)

        try:
            pic = open(f"goods/riba/{item}.jpg", 'rb')
            pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                        f'\n{fish[item]["Описание"]}'
                                                        f'\n'
                                                        f'\nЦена: {fish[item]["Цена"]}р/<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')
        except FileNotFoundError:
            pic = open(f'goods/riba/рыба.jpg', 'rb')
            pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                        f'\n{fish[item]["Описание"]}'
                                                        f'\n'
                                                        f'\nЦена: {fish[item]["Цена"]}р/<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in cheese)
def cheese_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_one = telebot.types.InlineKeyboardButton('+1шт', callback_data=f'+1 Сыр {item}')
    remove_one = telebot.types.InlineKeyboardButton('-1шт', callback_data=f'-1 Сыр {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_one, add_one)
    markup_inline.add(cart)

    try:
        pic = open(f"goods/cheese/{item}.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{cheese[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {cheese[item]["Цена"]}р/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/cheese/Косичка.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{cheese[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {cheese[item]["Цена"]}р/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in lemonade)
def lemonade_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_one = telebot.types.InlineKeyboardButton('+1шт', callback_data=f'+1 Лимонад {item}')
    remove_one = telebot.types.InlineKeyboardButton('-1шт', callback_data=f'-1 Лимонад {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_one, add_one)
    if lemonade[item]["Подробнее"]:
        adress = telebot.types.InlineKeyboardButton('📖 Подробнее', url=lemonade[item]["Подробнее"])
        markup_inline.add(adress, cart)
    else:
        markup_inline.add(cart)

    try:
        pic = open(f"goods/lemonade/{item}.png", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{lemonade[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {lemonade[item]["Цена"]}р/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/lemonade/Лимонад.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{lemonade[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {lemonade[item]["Цена"]}р/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in energize)
def energize_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_one = telebot.types.InlineKeyboardButton('+1шт', callback_data=f'+1 Энергетик {item}')
    remove_one = telebot.types.InlineKeyboardButton('-1шт', callback_data=f'-1 Энергетик {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_one, add_one)
    if energize[item]["Подробнее"]:
        adress = telebot.types.InlineKeyboardButton('📖 Подробнее', url=energize[item]["Подробнее"])
        markup_inline.add(adress, cart)
    else:
        markup_inline.add(cart)

    try:
        pic = open(f"goods/energize/{item}.png", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{energize[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {energize[item]["Цена"]}р/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/lemonade/Лимонад.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{energize[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {energize[item]["Цена"]}р/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')


@pennij_bot.message_handler(func=lambda message: message.text in sodie_pop)
def sodie_pop_add(message):
    item = message.text
    markup_inline = telebot.types.InlineKeyboardMarkup()
    add_one = telebot.types.InlineKeyboardButton('+1шт', callback_data=f'+1 Полторашка {item}')
    remove_one = telebot.types.InlineKeyboardButton('-1шт', callback_data=f'-1 Полторашка {item}')
    cart = telebot.types.InlineKeyboardButton('🛒 Корзина', callback_data=f'shoppingCart')
    markup_inline.add(remove_one, add_one)
    if sodie_pop[item]["Подробнее"]:
        adress = telebot.types.InlineKeyboardButton('📖 Подробнее', url=sodie_pop[item]["Подробнее"])
        markup_inline.add(adress, cart)
    else:
        markup_inline.add(cart)

    try:
        pic = open(f"goods/sodie_pop/{item}.png", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{sodie_pop[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {sodie_pop[item]["Цена"]}р/<b>1.5л</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/lemonade/Лимонад.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{sodie_pop[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {sodie_pop[item]["Цена"]}р/1.5л</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')


"""Работа с корзиной"""


@pennij_bot.callback_query_handler(func=lambda callback: callback.data == "shoppingCart")
def show_cart_callback(callback):
    if callback.message.chat.id in cart:
        if cart[callback.message.chat.id]:
            total_ammount = cartChapter(callback=callback)
            pennij_bot.answer_callback_query(callback.id, f'Итого: {total_ammount}р')
        else:
            pennij_bot.answer_callback_query(callback.id, f'Корзина пуста')
    else:
        pennij_bot.answer_callback_query(callback.id, f'Корзина пуста')


def show_cart_button(message):
    cartID = message.chat.id
    if cartID in cart:
        if cart[cartID]:
            cartChapter(message=message)
        else:
            pennij_bot.send_message(message.chat.id, f"Корзина пуста")
    else:
        pennij_bot.send_message(message.chat.id, f"Корзина пуста")


def stashCheck(query):
    print(cart)
    sorted_query = dict(sorted(query.items(), key=lambda x: x[0]))
    check = f'{"~" * 25}\n'
    total_ammount = 0 + DELIVERY
    bottles_query = {'1.5': 0,
                     '1': 0}
    bottles_ammount = 0
    check_id = 0
    for key, value in sorted_query.items():
        item_type, item_name = key.split(maxsplit=1)

        if item_type == "Пиво":
            check_id += 1
            ammount = int(beer[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}л: {ammount}р\n'
            get_bottles = smartBottles(value)
            for key, value in get_bottles.items():
                bottles_query[key] += value
            total_ammount += ammount

        elif item_type == "Сидр":
            check_id += 1
            ammount = int(cidre[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}л: {ammount}р\n'
            get_bottles = smartBottles(value)
            for key, value in get_bottles.items():
                bottles_query[key] += value
            total_ammount += ammount

        elif item_type == "Лимонад":
            check_id += 1
            ammount = int(lemonade[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}шт: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Энергетик":
            check_id += 1
            ammount = int(energize[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}шт: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Полторашка":
            check_id += 1
            ammount = int(sodie_pop[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}шт: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Сухарики":
            check_id += 1
            ammount = int(crackers[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {int(value * 1000)}гр: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Закуска":
            check_id += 1
            ammount = int(knuts[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}шт: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Сыр":
            check_id += 1
            ammount = int(cheese[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}шт: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Рыбка":
            check_id += 1
            if fish[item_name]['Фасовка'] == "Наразвес":
                ammount = int(fish[item_name]['Цена'] * value)
                check += f'{check_id}) {item_type} <b>"{item_name}"</b> {int(value * 1000)}гр: {ammount}р\n'
                total_ammount += ammount
            elif fish[item_name]['Фасовка'] == "Поштучно":
                ammount = int(fish[item_name]['Цена'] * value)
                if item_name == "Бычки":
                    check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}уп({value * 10}шт): {ammount}р\n'
                else:
                    check += f'{check_id}) {item_type} <b>"{item_name}"</b> {value}шт: {ammount}р\n'
                total_ammount += ammount

    for key, value in bottles_query.items():
        if value:
            bottles_ammount += value * bottle_price
            check_id += 1
            check += f'{check_id}) {key}л X {value} = {value * bottle_price}р\n'
    total_ammount += bottles_ammount

    check += f'{"~" * 25}\n' \
             f'Доставка: {DELIVERY}р\n' \
             f'Тара: {bottles_ammount}р\n' \
             f'Итого: {total_ammount}р'

    return [check, total_ammount]


@pennij_bot.callback_query_handler(func=lambda callback: True)
def purchase_callback(callback):
    global cart
    callback_request = callback.data.split()[0]
    print(f"{callback.data} для {callback.from_user.first_name}  - callback_request")
    if callback_request == "+1":
        option = 1
        item = " ".join(callback.data.split()[1:])
        serving_option = "шт"
        add_to_cart(callback, item, option, serving_option)

    elif callback_request == "-1":
        if callback.message.chat.id in cart:
            option = 1
            item = " ".join(callback.data.split()[1:])
            serving_option = "шт"
            try:
                remove_from_cart(callback, item, option, serving_option)
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} удален из корзины: {cart[callback.message.chat.id][item]}')
            except KeyError:
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} отсутствует в корзине')
        else:
            pennij_bot.answer_callback_query(callback.id, f'Корзина пуста')

    if callback_request == "+1.0":
        option = 1.0
        item = " ".join(callback.data.split()[1:])
        serving_option = "л"
        add_to_cart(callback, item, option, serving_option)

    elif callback_request == "-1.0":
        if callback.message.chat.id in cart:
            option = 1.0
            item = " ".join(callback.data.split()[1:])
            serving_option = "л"
            try:
                remove_from_cart(callback, item, option, serving_option)
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} удален из корзины: {cart[callback.message.chat.id][item]}')
            except KeyError:
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} отсутствует в корзине')
        else:
            pennij_bot.answer_callback_query(callback.id, f'Корзина пуста')

    elif callback_request == "+1.5":
        option = 1.5
        item = " ".join(callback.data.split()[1:])
        serving_option = "л"
        add_to_cart(callback, item, option, serving_option)

    elif callback_request == "-1.5":
        if callback.message.chat.id in cart:
            option = 1.5
            item = " ".join(callback.data.split()[1:])
            serving_option = "л"
            try:
                remove_from_cart(callback, item, option, serving_option)
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} удален из корзины: {cart[callback.message.chat.id][item]}')
            except KeyError:
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} отсутствует в корзине')
        else:
            pennij_bot.answer_callback_query(callback.id, f'Корзина пуста')

    elif callback_request == "+100":
        option = 0.1
        item = " ".join(callback.data.split()[1:])
        serving_option = "гр"
        add_to_cart(callback, item, option, serving_option)

    elif callback_request == "-100":
        if callback.message.chat.id in cart:
            option = 0.1
            item = " ".join(callback.data.split()[1:])
            serving_option = "гр"
            try:
                remove_from_cart(callback, item, option, serving_option)
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} удален из корзины: {cart[callback.message.chat.id][item]}')
            except KeyError:
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} отсутствует в корзине')
        else:
            pennij_bot.answer_callback_query(callback.id, f'Корзина пуста')


def add_to_cart(callback, item, option, serving_option):
    if callback.message.chat.id not in cart:
        cart.update({callback.message.chat.id: {}})
        cart[callback.message.chat.id][item] = round(cart[callback.message.chat.id].get(item, 0) + option, 1)
        if serving_option != "гр":
            pennij_bot.answer_callback_query(callback.id,
                                             f'{item} в корзине: {cart[callback.message.chat.id][item]}'
                                             f'{serving_option}')
        else:
            pennij_bot.answer_callback_query(callback.id,
                                             f'{item} в корзине: {int(cart[callback.message.chat.id][item] * 1000)}'
                                             f'{serving_option}')
    else:
        cart[callback.message.chat.id][item] = round(cart[callback.message.chat.id].get(item, 0) + option, 1)
        if serving_option != "гр":
            pennij_bot.answer_callback_query(callback.id,
                                             f'{item} в корзине: {cart[callback.message.chat.id][item]}'
                                             f'{serving_option}')
        else:
            pennij_bot.answer_callback_query(callback.id,
                                             f'{item} в корзине: {int(cart[callback.message.chat.id][item] * 1000)}'
                                             f'{serving_option}')


def remove_from_cart(callback, item, option, serving_option):
    try:
        rqst = cart[callback.message.chat.id].get(item)
        print(f'{item} for {callback.from_user.first_name}')
        if rqst - option <= 0.5:
            del cart[callback.message.chat.id][item]
            pennij_bot.answer_callback_query(callback.id, f'{item} - удалено из корзины')
        else:
            cart[callback.message.chat.id][item] = round(cart[callback.message.chat.id].get(item) - option, 1)
            if serving_option != "гр":
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} остаток в корзине: '
                                                 f'{cart[callback.message.chat.id][item]}{serving_option}')
            else:
                pennij_bot.answer_callback_query(callback.id,
                                                 f'{item} остаток в корзине: '
                                                 f'{int(cart[callback.message.chat.id][item] * 1000)}'
                                                 f'{serving_option}')
    except TypeError:
        pennij_bot.answer_callback_query(callback.id,
                                         f'{item} - нет в корзине')


def cartChapter(message=None, callback=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✅ Оформить заказ")
    btn2 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)

    if message:
        stash, total_ammount = stashCheck(cart[message.chat.id])
        pennij_bot.send_message(message.chat.id, f'Твоя корзина, {message.from_user.first_name}:'
                                                 f'\n{stash}', reply_markup=markup, parse_mode='html')
    elif callback:
        stash, total_ammount = stashCheck(cart[callback.message.chat.id])
        pennij_bot.send_message(callback.message.chat.id, f'Твоя корзина, {callback.from_user.first_name}:'
                                                          f'\n{stash}', reply_markup=markup, parse_mode='html')

    return total_ammount


"""Пользовательские сообщения"""


@pennij_bot.message_handler()
def user_messages(message):
    # Кнопки главного меню
    if message.text == '🍻 Ассортимент 🐟':
        goodsChapter(message)
    elif message.text == '🛟 Помощь':
        if message.chat.id != ADMIN_ID:
            pennij_bot.send_message(message.chat.id, 'Держись, брат!')
        else:
            admins_menu(message)
    elif message.text == '📄 Контакты':
        pennij_bot.send_message(message.chat.id,
                                'Заказать пиво по телефону:'
                                '\n<i>+79155633989</i> - <b>Кирилл</b>'
                                '\n'
                                '\n<b>Разработчик</b> - <u>@repredess</u>',
                                parse_mode='html')
    elif message.text == '🛒 Корзина':
        show_cart_button(message)

    elif message.text == '✅ Оформить заказ':
        placing_an_order(message)

    # Кнопка "ПИВО"
    elif message.text == 'Пиво':
        chooseBeer(message)
    # elif message.text == 'Вайсберг':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton('🛒 Добавить "Вайсберг"')
    #     btn2 = types.KeyboardButton('↩️ Назад к пиву')
    #     markup.row(btn1, btn2)
    #     pic = open("goods/pivo/Вайсберг.jpg", 'rb')
    #     pennij_bot.send_photo(message.chat.id, pic, 'Нежное пиво с сливочным послевкусием. Алкоголь 4.7.',
    #                           reply_markup=markup)
    elif message.text == 'Сидры':
        chooseSidre(message)

    # Кнопка "БЕЗАЛКОГОЛЬНОЕ"
    elif message.text == 'Безалкогольное':
        chooseNotAlco(message)
    # Виды безалкогольного
    elif message.text == 'Лимонады':
        chooseLemonade(message)
    elif message.text == 'Энергетики':
        chooseEnergize(message)
    elif message.text == 'Сладкая вода':
        chooseSodiePop(message)

    # Кнопка "СНЕКИ"
    elif message.text == 'Снеки':
        chooseSnacs(message)
    # Виды снеков
    elif message.text == 'Сухарики':
        chooseCrackers(message)
    elif message.text == 'Кнуты и палочки':
        chooseSticks(message)
    elif message.text == 'Рыбка':
        chooseFish(message)
    elif message.text == 'Сыры':
        chooseCheese(message)

    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад к ассортименту':
        goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        main_page(message)
    elif message.text == '↩️ Назад к пиву':
        chooseBeer(message)
    elif message.text == '↩️ Назад к сидрам':
        chooseSidre(message)
    elif message.text == '↩️ Назад к рыбке':
        chooseFish(message)
    elif message.text == '↩️ Назад к сухарикам':
        chooseCrackers(message)
    elif message.text == '↩️ Назад к снекам':
        chooseSnacs(message)
    elif message.text == '↩️ Назад к безалкогольному':
        chooseNotAlco(message)
    elif message.text == '↩️ Назад к палочкам':
        chooseSticks(message)
    else:
        pennij_bot.reply_to(message, f'{random.choice(ANSWERS)} \n<b>Вернуться на главную</b>: <u>/start</u>',
                            parse_mode='html')


"""Подраздел и раздел с выбором продукции"""


def admins_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/write")
    btn2 = types.KeyboardButton("/read")
    btn3 = types.KeyboardButton("↩️ Назад в меню")
    markup.row(btn1, btn2)
    markup.row(btn3)

    pennij_bot.send_message(message.chat.id, 'Админ-панель:', reply_markup=markup)


def main_page(message, order=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🍻 Ассортимент 🐟')
    btn2 = types.KeyboardButton('🛟 Помощь')
    btn3 = types.KeyboardButton('📄 Контакты')
    markup.row(btn1)
    markup.row(btn2, btn3)

    if not order:
        pennij_bot.send_message(message.chat.id,
                                f"Уверен тебе здесь нравится, <b>{message.from_user.first_name}</b>! "
                                f"\nТы можешь заказать <b>пиво и рыбку</b> через приложение или по телефону ;)"
                                f"\nНомер для связи находится в разделе: 📄 Контакты",
                                parse_mode='html', reply_markup=markup)
        announcment(message=message, say=SAY)
    else:
        pennij_bot.send_message(message.chat.id,
                                f"Скоро тебе презвонят что бы уточнить детали. Будь на связи😉",
                                parse_mode='html', reply_markup=markup)
        announcment(message=message, say=SAY)


def goodsChapter(message, talk=True):
    connect = sqlite3.connect('shop.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    chat_id INTEGER,
    user_name TEXT,
    user_id INTEGER,
    reg_date TEXT,
    last_date TEXT);
    """)

    connect.commit()

    chat_id = message.chat.id
    user_name = message.from_user.first_name
    reg_date = " ".join(str(datetime.datetime.now()).split('.')[0:-1])
    if message.from_user.username:
        user_name += f' "{message.from_user.username}"'
    if message.from_user.last_name:
        user_name += f' {message.from_user.last_name}'
    user_id = message.from_user.id
    cursor.execute(f"SELECT chat_id FROM login_id WHERE chat_id = {chat_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO login_id VALUES(?,?,?,?,?);", (chat_id,
                                                                   user_name,
                                                                   user_id,
                                                                   reg_date,
                                                                   last_date))
        connect.commit()
    else:
        cursor.execute("UPDATE login_id SET last_date = ? WHERE chat_id = ?", (reg_date, chat_id))
        connect.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пиво")
    btn2 = types.KeyboardButton("Сидры")
    btn3 = types.KeyboardButton("Безалкогольное")
    btn4 = types.KeyboardButton("Рыбка")
    btn5 = types.KeyboardButton("Снеки")
    btn6 = types.KeyboardButton("↩️ Назад в меню")
    btn7 = types.KeyboardButton("🛒 Корзина")
    markup.row(btn1, btn2)
    markup.row(btn3, btn5)
    markup.row(btn7, btn4, btn6)
    intro = random.choice(INTRODUCE)

    if talk:
        pennij_bot.send_message(message.chat.id, f'{intro}', reply_markup=markup)

        if ANNOUNCEMENT:
            announcment(message, SAY, percent=20)


def chooseNotAlco(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Лимонады")
    btn2 = types.KeyboardButton("Энергетики")
    btn3 = types.KeyboardButton("Сладкая вода")
    btn4 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    pennij_bot.send_message(message.chat.id, 'Попробуй все ;) \nВыбирай:', reply_markup=markup)


def chooseLemonade(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Клубничный")
    btn2 = types.KeyboardButton("Мохито")
    btn3 = types.KeyboardButton("Имбирный")
    btn4 = types.KeyboardButton("Классический")
    btn5 = types.KeyboardButton("↩️ Назад к безалкогольному")
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5)

    pennij_bot.send_message(message.chat.id, 'Лучшие в городе😉\nВыбирай:', reply_markup=markup)


def chooseEnergize(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("TARGET ZERO")
    btn2 = types.KeyboardButton("TARGET ACTIVE")
    btn3 = types.KeyboardButton("TARGET ORIGINAL")
    btn4 = types.KeyboardButton("TARGET MAXIMUM")
    btn5 = types.KeyboardButton("TARGET MANGO")
    btn6 = types.KeyboardButton("↩️ Назад к безалкогольному")
    markup.row(btn2, btn3, btn4)
    markup.row(btn1, btn5, btn6)

    pennij_bot.send_message(message.chat.id, 'Бодрят как надо😏\nВыбирай:', reply_markup=markup)


def chooseSodiePop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Cola Bochkari")
    btn2 = types.KeyboardButton("CitrusHit Bochkari")
    btn3 = types.KeyboardButton("Orange Bochkari")
    btn4 = types.KeyboardButton('Квас "Андреич"')
    btn5 = types.KeyboardButton("↩️ Назад к безалкогольному")
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5)

    pennij_bot.send_message(message.chat.id, 'Сладкая вода, а что еще надо😌 \nВыбирай:', reply_markup=markup)


def chooseSticks(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Мясные кнуты")
    btn2 = types.KeyboardButton("Палочки из щуки")
    btn3 = types.KeyboardButton("Палочки из тунца")
    btn4 = types.KeyboardButton("Палочки из лосося")
    btn5 = types.KeyboardButton("↩️ Назад к снекам")
    markup.row(btn2, btn3, btn4)
    markup.row(btn1, btn5)

    pennij_bot.send_message(message.chat.id, 'То что надо к пиву🤤\nВыбирай:', reply_markup=markup)


def chooseCrackers(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Деревенские")
    btn2 = types.KeyboardButton("Тайский перец")
    btn3 = types.KeyboardButton("Сливочный сыр")
    btn4 = types.KeyboardButton("Ветчина-сыр")
    btn5 = types.KeyboardButton("Аджика")
    btn6 = types.KeyboardButton("Чесночный микс")
    btn7 = types.KeyboardButton("Краб")
    btn8 = types.KeyboardButton("↩️ Назад к снекам")
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5, btn6)
    markup.row(btn7, btn8)

    pennij_bot.send_message(message.chat.id, 'Всегда вкусные и хрустящие', reply_markup=markup)


def chooseSnacs(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сухарики")
    btn2 = types.KeyboardButton("Сыры")
    btn3 = types.KeyboardButton("Кнуты и палочки")
    btn4 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    pennij_bot.send_message(message.chat.id, 'Каждый месяц что-то новое😋', reply_markup=markup)


def chooseCheese(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Косичка")
    btn2 = types.KeyboardButton("↩️ Назад к снекам")
    markup.row(btn1, btn2)

    pennij_bot.send_message(message.chat.id, 'Упругие и вкусные😋 \nВыбирай:', reply_markup=markup)


def chooseSidre(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Голубая лагуна")
    btn2 = types.KeyboardButton("Ламбрусско")
    btn3 = types.KeyboardButton("Манго-маракуйя")
    btn4 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    pennij_bot.send_message(message.chat.id, 'Каждый месяц что-то новое😋 \nВыбирай:', reply_markup=markup)


def chooseFish(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Корюшка")
    btn2 = types.KeyboardButton("Тарань")
    btn3 = types.KeyboardButton("Горбуша (копченая)")
    btn4 = types.KeyboardButton("Густера")
    btn5 = types.KeyboardButton("Лещ")
    btn6 = types.KeyboardButton("Бычки")
    btn7 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2, btn4, btn5)
    markup.row(btn3, btn6, btn7)

    pennij_bot.send_message(message.chat.id, 'Всегда свежая рыбка🐟\nВыбирай:', reply_markup=markup)


def chooseBeer(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вайсберг")
    btn2 = types.KeyboardButton("Гагарин")
    btn3 = types.KeyboardButton("Штормовое")
    btn4 = types.KeyboardButton("Стаут")
    btn5 = types.KeyboardButton("Домашнее")
    btn6 = types.KeyboardButton("Регион 82")
    btn7 = types.KeyboardButton("Чешское Элитное")
    btn8 = types.KeyboardButton("Моряк")
    btn9 = types.KeyboardButton("Хорватское")
    btn10 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2, btn4, btn6)
    markup.row(btn9, btn3, btn5)
    markup.row(btn7, btn8, btn10)

    pennij_bot.send_message(message.chat.id, 'Пиво на любой вкус😉 \nВыбирай любое:', reply_markup=markup)


"""Полезные функции"""


def write_order(message, phone, order, total):
    connect = sqlite3.connect('shop.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
        chat_id INTEGER,
        user_name TEXT,
        user_id INTEGER,
        user_phone INTEGER,
        user_order TEXT,
        order_date TEXT,
        order_ammount INTEGER);
        """)

    connect.commit()

    chat_id = message.chat.id
    user_phone = phone
    order_date = " ".join(str(datetime.datetime.now()).split('.')[0:-1])
    user_id = message.from_user.id
    user_order = order
    order_ammount = total
    user_name = message.from_user.first_name
    if message.from_user.username:
        user_name += f' "{message.from_user.username}"'
    if message.from_user.last_name:
        user_name += f' {message.from_user.last_name}'

    cursor.execute("INSERT INTO orders VALUES(?,?,?,?,?,?,?);", (chat_id,
                                                                 user_name,
                                                                 user_id,
                                                                 user_phone,
                                                                 user_order,
                                                                 order_date,
                                                                 order_ammount))
    connect.commit()


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


def smartBottles(liters):
    is_good = liters / 1.5
    if is_good.is_integer():
        bottles_1_5 = is_good
        return {'1.5': int(bottles_1_5)}
    else:
        bottles_1 = 1
        while True:
            is_good = (liters - bottles_1) / 1.5
            if is_good.is_integer():
                bottles_1_5 = is_good
                if int(bottles_1_5) > 0:
                    return {'1.5': int(bottles_1_5), '1': int(bottles_1)}
                else:
                    return {'1': int(bottles_1)}
            else:
                bottles_1 += 1


def announcment(message, say, percent=None):
    if percent:
        random_number = random.randint(0, 101)
        if random_number <= percent:
            tell = random.choice(say)
            pennij_bot.send_message(message.chat.id, f'{tell}', parse_mode='html')
            print(f'Огласил "{tell}" для {message.from_user.first_name}'
                  f'Выпало число {random_number} с шансом {percent}% из 100')
    else:
        tell = random.choice(say)
        pennij_bot.send_message(message.chat.id, f'{tell}', parse_mode='html')
        print(f'Огласил "{tell}" для {message.from_user.first_name}')


def send_to_admin(message, in_app=False):
    id = message.from_user.id
    print(message)
    if id == ADMIN_ID:
        print(f"Admin is HEREEE🫡. Name {message.from_user.first_name}")
        # pennij_bot.send_message(ADMIN_ID, "Its Admin's ID")
    elif id != ADMIN_ID:
        if in_app:
            pennij_bot.send_message(ADMIN_ID, f'Somebody come to find for some beer. His name/ID ='
                                              f' {message.from_user.first_name}{id}')
        print(f'Somebody wanna find some. His ID = {id}. Name {message.from_user.first_name}')


def into_translit(text):
    d = {
        'а': 'a', 'к': 'k', 'х': 'h', 'б': 'b', 'л': 'l', 'ц': 'c', 'в': 'v', 'м': 'm', 'ч': 'ch',
        'г': 'g', 'н': 'n', 'ш': 'sh', 'д': 'd', 'о': 'o', 'щ': 'shh', 'е': 'e', 'п': 'p', 'ъ': '*',
        'ё': 'jo', 'р': 'r', 'ы': 'y', 'ж': 'zh', 'с': 's', 'ь': "'", 'з': 'z', 'т': 't', 'э': 'je',
        'и': 'i', 'у': 'u', 'ю': 'ju', 'й': 'j', 'ф': 'f', 'я': 'ya'
    }

    main_fin = ''

    for i in text:
        if i.lower() in d:
            if i.islower():
                main_fin += d.get(i)
            elif i.isupper():
                main_fin += d.get(i.lower()).title()
        else:
            main_fin += i

    return main_fin


def go_infinity():
    print("some troubles with network")
    try:
        # https://stackoverflow.com/questions/68739567/socket-timeout-on-telegram-bot-polling
        pennij_bot.infinity_polling(timeout=10, long_polling_timeout=5)
        pennij_bot.send_message(message_chat.id, "Проблемы с сервером... Подождите минутку")
        # pennij_bot.polling(none_stop=True)
    except requests.exceptions.ConnectionError:
        pennij_bot.infinity_polling(timeout=10, long_polling_timeout=5)
    time.sleep(5)


try:
    # https://stackoverflow.com/questions/68739567/socket-timeout-on-telegram-bot-polling
    pennij_bot.infinity_polling(timeout=10, long_polling_timeout=5)
except requests.exceptions.ConnectionError:
    print("Траблы ConnectionError")
    pennij_bot.infinity_polling(timeout=10, long_polling_timeout=5)
except requests.exceptions.ReadTimeout:
    print("Траблы ReadTimeout")
    pennij_bot.infinity_polling(timeout=10, long_polling_timeout=5)
except telebot.apihelper.ApiTelegramException:
    print("Траблы ReadTimeout")
    pennij_bot.infinity_polling(timeout=10, long_polling_timeout=5)

# Стандарт который у меня был:
# pennij_bot.polling(none_stop=True)
