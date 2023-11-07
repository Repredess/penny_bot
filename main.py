import datetime
import sqlite3
from telebot import types
import telebot
import time
import os
import random
from config import BOT_TOKEN, URL, ANSWERS, ADMIN_ID, ANNOUNCEMENT, SAY, DELIVERY, INTRODUCE
from assortiment import beer, cidre, crackers, knuts, fish, cheese, all_goods
from nick_names import NICK

"""
Что бы бот заработал - следует создать файл config.py в корневой папке проекта и задать там переменную BOT_TOKEN
содержащую токен Вашего бота. Так же можно создать переменную URL в которой указывается нужный Вам сайт.
В переменной ANNOUNCEMENT можно включать и отключать извещения.

Что бы добавить или изменить кнопку надо доавить ее в нужный раздел словаря в assortiment.py, а затем изменить функцию 
chooseНУЖНЫЙ_ТОВАР так, что бы у кнопки было такое же название что и у в словаре. Так же рекомендуется загрузить фотку
по разделу. Название фотки должно соответствовать названию кнопки

Команды для бота:
start - Вернуться к началу
help - Увидеть все команды
site - Перейти на сайт

ИРЛ:
Прописать сколько грамм рыбы пробивать через кассу что бы било чек





Нужно добавить:
Рассылку новых предложений пользователям - через кнопку настройки которая будет отображаться только у админов. 
Нужно будет отправить фотку для рассылки, сообщение для рассылки посмотреть как это будет выглядеть и разослать
всем пользователям из таблицы login_id

Фотки и описание для всех айтемов

Добавление заказа в текстовый документ

Отправка заказа админам в ТГ
Отправка заказа на рабочую почту


Загрузить бота на сервер

Работа бота в рабочее время (с 10 до 9)

расчет суммы пива и сидров вместе с тарой

Сохранение телефона пользователя, его фамилии и ника в бд(таблица login_id)

"""

pennij_bot = telebot.TeleBot(BOT_TOKEN)

cart = {}

DIR = "memes"

"""Commands"""


@pennij_bot.message_handler(commands=["start"])
def welcome(message):
    connect = sqlite3.connect('shop.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    chat_id INTEGER,
    user_name TEXT,
    user_id INTEGER);
    """)

    connect.commit()

    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    cursor.execute(f"SELECT chat_id FROM login_id WHERE chat_id = {chat_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO login_id VALUES(?,?,?);", (chat_id,
                                                               user_name,
                                                               user_id))
        connect.commit()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🍻 Ассортимент 🐟')
    btn2 = types.KeyboardButton('🛟 Помощь')
    btn3 = types.KeyboardButton('📄 Контакты')
    markup.row(btn1)
    markup.row(btn2, btn3)

    pennij_bot.send_message(message.chat.id,
                            f"Привет, <b>{message.from_user.first_name}</b>! "
                            f"Ты можешь заказать пиво и рыбку через приложение или по телефону;)"
                            f"\nНомер телефона для связи находится в разделе: 📄 Контакты",
                            parse_mode='html', reply_markup=markup)


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


"""Order"""


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
    pennij_bot.answer_callback_query(callback.id, 'Заказ отменен')
    goodsChapter(callback.message)


@pennij_bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        order, money = stashCheck(cart[message.chat.id])
        pennij_bot.send_message(ADMIN_ID, f"Заказ для {message.from_user.first_name} оформлен: {order}\n"
                                          f"Номер для связи: {message.contact.phone_number}")
        pennij_bot.send_message(message.chat.id, f'Спасибо за заказ, {message.from_user.first_name}.',
                                parse_mode='html')
        del cart[message.chat.id]
        main_page(message, order=True)
    except KeyError:
        pennij_bot.send_message(message.chat.id, f'Упс, кажется с нашим сервером что то случилось.\n'
                                                 f'Попробуйте заполнить корзину еще раз.')
        main_page(message)


"""Cart and etc"""


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
    """ПИВО СИДР СЫР СУХАРИКИ ЗАКУСКА РЫБКА БЕЗАЛКОГОЛЬНОЕ"""
    print(query)
    sorted_query = dict(sorted(query.items(), key=lambda x: x[0]))
    check = f'{"~" * 25}\n'
    total_ammount = 0 + DELIVERY
    check_id = 0
    for key, value in sorted_query.items():
        # print(f'{key}, {value}')
        item_type, item_name = key.split(maxsplit=1)
        print(item_name)
        if item_type == "Пиво":
            check_id += 1
            ammount = int(beer[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} "{item_name}" {value}л: {ammount}р\n'
            total_ammount += ammount

        elif item_type == "Сидр":
            check_id += 1
            ammount = int(cidre[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} "{item_name}" {value}л: {ammount}р\n'
            total_ammount += ammount
        elif item_type == "Безалкогольное":
            pass
        elif item_type == "Сухарики":
            check_id += 1
            ammount = int(crackers[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} "{item_name}" {int(value * 1000)}гр: {ammount}р\n'
            total_ammount += ammount
        elif item_type == "Закуска":
            check_id += 1
            ammount = int(knuts[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} "{item_name}" {value}шт: {ammount}р\n'
            total_ammount += ammount
        elif item_type == "Рыбка":
            check_id += 1
            if fish[item_name]['Фасовка'] == "Наразвес":
                print(f"{item_name} - наразвес")
                ammount = int(fish[item_name]['Цена'] * value)
                check += f'{check_id}) {item_type} "{item_name}" {int(value * 1000)}гр: {ammount}р\n'
                total_ammount += ammount
            elif fish[item_name]['Фасовка'] == "Поштучно":
                print(f"{item_name} - наразвес")
                ammount = int(fish[item_name]['Цена'] * value)
                check += f'{check_id}) {item_type} "{item_name}" {value}шт: {ammount}р\n'
                total_ammount += ammount
        elif item_type == "Сыр":
            check_id += 1
            ammount = int(cheese[item_name]['Цена'] * value)
            check += f'{check_id}) {item_type} "{item_name}" {value}шт: {ammount}р\n'
            total_ammount += ammount

    check += f'{"~" * 25}\n' \
             f'Доставка: {DELIVERY}р\n' \
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
        print(f'{item} for {callback.from_user.first_name}')
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
        print(f'{item} for {callback.from_user.first_name}')
        if serving_option != "гр":
            pennij_bot.answer_callback_query(callback.id,
                                             f'{item} в корзине: {cart[callback.message.chat.id][item]}'
                                             f'{serving_option}')
        else:
            pennij_bot.answer_callback_query(callback.id,
                                             f'{item} в корзине: {int(cart[callback.message.chat.id][item] * 1000)}'
                                             f'{serving_option}')
        print(cart)


def remove_from_cart(callback, item, option, serving_option):
    try:
        rqst = cart[callback.message.chat.id].get(item)
        print(f'{item} for {callback.from_user.first_name}')
        if rqst - option <= 0:
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
        print(cart)
    except TypeError:
        pennij_bot.answer_callback_query(callback.id,
                                         f'{item} - нет в корзине')


"""Chapters"""


@pennij_bot.message_handler()
def user_messages(message):
    # Кнопки главного меню
    if message.text == '🍻 Ассортимент 🐟':
        goodsChapter(message)
    elif message.text == '🛟 Помощь':
        pennij_bot.send_message(message.chat.id, 'Держись, брат!')
    elif message.text == '📄 Контакты':
        pennij_bot.send_message(message.chat.id,
                                'Заказать пиво по телефону:'
                                '\n<i>+79155633989</i> - <b>Кирилл</b>'
                                '\n'
                                '\n<b>Разаработчик</b> - <u>@repredess</u>',
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

    elif message.text == 'Безалкогольное':
        pennij_bot.send_message(message.chat.id, 'Безалкогольного пока нет \nМало того - ты еще не выпил штрафную')

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
    elif message.text == '↩️ Назад к палочкам':
        chooseSticks(message)
    else:
        pennij_bot.reply_to(message, f'{random.choice(ANSWERS)} \n<b>Вернуться на главную</b>: <u>/start</u>',
                            parse_mode='html')


def cartChapter(message=None, callback=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✅ Оформить заказ")
    btn2 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)

    if message:
        stash, total_ammount = stashCheck(cart[message.chat.id])
        pennij_bot.send_message(message.chat.id, f'Твоя корзина, {message.from_user.first_name}:'
                                                 f'\n{stash}', reply_markup=markup)
    elif callback:
        stash, total_ammount = stashCheck(cart[callback.message.chat.id])
        pennij_bot.send_message(callback.message.chat.id, f'Твоя корзина, {callback.from_user.first_name}:'
                                                          f'\n{stash}', reply_markup=markup)

    return total_ammount


def goodsChapter(message, talk=True):
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
                                f"Ты можешь заказать пиво и рыбку через приложение или по телефону;)"
                                f"\nНомер телефона для связи находится в разделе контакы",
                                parse_mode='html', reply_markup=markup)
        announcment(message=message, say=SAY)
    else:
        pennij_bot.send_message(message.chat.id,
                                f"Скоро тебе презвонят что бы уточнить детали. Будь на связи😉",
                                parse_mode='html', reply_markup=markup)
        announcment(message=message, say=SAY)


"""Choose and add"""


def chooseSnacs(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Сухарики")
    btn2 = types.KeyboardButton("Сыры")
    btn3 = types.KeyboardButton("Кнуты и палочки")
    btn4 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    pennij_bot.send_message(message.chat.id, 'Каждый месяц что-то новое😋', reply_markup=markup)


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
                                                    f'\nЦена: {knuts[item]["Цена"]}р/упаковка',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/knuts/Палочки.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{knuts[item]["Описание"]}'
                                                    f'\nЦена: {knuts[item]["Цена"]}р/упаковка',
                              reply_markup=markup_inline,
                              parse_mode='html')


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
                              f'\nЦена: {crackers[item]["Цена"]}р/100гр',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/crackers/crackers.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{crackers[item]["Описание"]}'
                                                    f'\nОстрота: {crackers[item]["Острота"]}'
                                                    f'\nЦена: {crackers[item]["Цена"]}р/100гр',
                              reply_markup=markup_inline,
                              parse_mode='html')


def chooseCheese(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Косичка")
    btn2 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)

    pennij_bot.send_message(message.chat.id, 'Упругие и вкусные😋 \nВыбирай:', reply_markup=markup)


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
                                                    f'\nЦена: <i>{cheese[item]["Цена"]}р</i>/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/cheese/Косичка.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                    f'\n{cheese[item]["Описание"]}'
                                                    f'\nЦена: <i>{cheese[item]["Цена"]}р</i>/<b>1шт</b>',
                              reply_markup=markup_inline,
                              parse_mode='html')


def chooseSidre(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Голубая лагуна")
    btn2 = types.KeyboardButton("Глинтвейн")
    btn3 = types.KeyboardButton("Манго-маракуйя")
    btn4 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    pennij_bot.send_message(message.chat.id, 'Каждый месяц что-то новое😋 \nВыбирай:', reply_markup=markup)


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
        pic = open(f'goods/pivo/Пиво.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b></i>'
                                                    f'\n{cidre[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {cidre[item]["Цена"]}р/литр | '
                                                    f'Алкоголь: {cidre[item]["Алкоголь"]}',
                              reply_markup=markup_inline,
                              parse_mode='html')


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

    pennij_bot.send_message(message.chat.id, 'Всегда свежая рыбка', reply_markup=markup)


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
                                                        f'\nЦена: <i>{int(fish[item]["Цена"] / 10)}р</i>/'
                                                        f'<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')
        except FileNotFoundError:
            pic = open(f'goods/riba/рыба.jpg', 'rb')
            pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                        f'\n{fish[item]["Описание"]}'
                                                        f'\nЦена: <i>{int(fish[item]["Цена"] / 10)}р</i>/'
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
                                                        f'\nЦена: <i>{fish[item]["Цена"]}р</i>/<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')
        except FileNotFoundError:
            pic = open(f'goods/riba/рыба.jpg', 'rb')
            pennij_bot.send_photo(message.chat.id, pic, f'<b><i>{item}</i></b>'
                                                        f'\n{fish[item]["Описание"]}'
                                                        f'\nЦена: <i>{fish[item]["Цена"]}р</i>/<b>{serving_option}</b>',
                                  reply_markup=markup_inline,
                                  parse_mode='html')


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
                                                    f'\nЦена: {beer[item]["Цена"]}р/литр | '
                                                    f'Алкоголь: {beer[item]["Алкоголь"]}',
                              reply_markup=markup_inline,
                              parse_mode='html')
    except FileNotFoundError:
        pic = open(f'goods/pivo/Пиво.jpg', 'rb')
        pennij_bot.send_photo(message.chat.id, pic, f'<i><b>{item}</b> | {beer[item]["Фильтрация"]}</i>'
                                                    f'\n{beer[item]["Описание"]}'
                                                    f'\n'
                                                    f'\nЦена: {beer[item]["Цена"]}р/литр | '
                                                    f'Алкоголь: {beer[item]["Алкоголь"]}',
                              reply_markup=markup_inline,
                              parse_mode='html')


"""Other functions"""


def smartBottles(liters, price):
    # Если литров не 0
    if liters > 0:
        liters_price = price * liters
        print(f'{liters}л = {liters_price}р')
        big_bottles = liters // 1.5
        small_bottles = False
        extrasmall_bottles = False
        remainder = liters % 1.5
        if remainder.is_integer():
            small_bottles = remainder
        else:
            extrasmall_bottles = remainder

        if (liters / 1.5).is_integer():
            bottles_price = int(big_bottles) * 15
            return f"1.5L x {int(big_bottles)} = {bottles_price}р" \
                   f"\ntotal ammount: {bottles_price + liters_price}р"
        elif small_bottles:
            if big_bottles:
                bottles_price = (int(big_bottles) + int(small_bottles)) * 15
                return f"1.5L x {int(big_bottles)} \n1L x {int(small_bottles)} = {bottles_price}р" \
                       f"\ntotal ammount: {bottles_price + liters_price}р"
            else:
                bottles_price = int(small_bottles) * 15
                return f"1L x {int(small_bottles)} = {bottles_price}р" \
                       f"\ntotal ammount: {bottles_price + liters_price}р"
        elif extrasmall_bottles:
            bottles_price = int(big_bottles) * 15 + 13
            return f"1.5L x {int(big_bottles)} \n0.5L x 1 = {bottles_price}р" \
                   f"\ntotal ammount: {bottles_price + liters_price}р"
    # Если литров 0
    else:
        return 'Литров не может быть 0'


def announcment(message, say, percent=None):
    if percent:
        random_number = random.randint(0, 100)
        if random_number <= percent:
            print(random_number, percent)
            tell = random.choice(say)
            pennij_bot.send_message(message.chat.id, f'{tell}', parse_mode='html')
            print(f'Огласил "{tell}" для {message.from_user.first_name}')
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
