import webbrowser
from telebot import types
import telebot
import random

"""
Команды для бота:
site - Открыть веб сайт
start - Вернуться к началу
help - Увидеть все команды
"""

pennij_bot = telebot.TeleBot('6860875409:AAE6Rtbw1xdbw-Uubnk_x1ZXP1q78Bj-CIM')

answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.']

final_order = []

announcment = "Советуем пропробовать наше новое пиво 'Заебатое'"


@pennij_bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🍻 Ассортимент 🐟')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Наши контакты')
    markup.row(btn1)
    markup.row(btn2, btn3)

    pennij_bot.send_message(message.chat.id,
                            f"Привет, <b>{message.from_user.first_name}</b>! Тут можно будет заказать пиво и рыбку ;) ",
                            parse_mode='html', reply_markup=markup)


@pennij_bot.message_handler()
def user_messages(message):
    if message.text == '🍻 Ассортимент 🐟':
        # if announcment:
        #     pennij_bot.send_message(message.chat.id, announcment)
        goodsChapter(message)
    elif message.text == 'Помощь':
        pennij_bot.send_message(message.chat.id, 'Держись, брат!')
    elif message.text == '📄 Контакты':
        pennij_bot.send_message(message.chat.id, '<i>+79155633989</i> - <b>Кирилл</b>', parse_mode='html')
    elif message.text == 'Пиво и сидры':
        choosePivo(message)
    elif message.text == 'Вайсберг':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Вайсберг"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/weisberg.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Нежное пиво с сливочным послевкусием. Алкоголь 4.7.',
                              reply_markup=markup)
    elif message.text == '🛒 Добавить "Вайсберг"':
        liters(message)
    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        welcome(message)
    elif message.text == '↩️ Назад к пиву':
        choosePivo(message)
    elif message.text == '↩️ Назад к ассортименту':
        goodsChapter(message)
    else:
        pennij_bot.reply_to(message, 'Я не понимаю о чем ты🙃 \n<b>Вернуться на главную</b>: <u>/start</u>',
                            parse_mode='html')


# @pennij_bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     if callback.data == "back":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 = types.KeyboardButton('Ассортимент')
#         btn2 = types.KeyboardButton('Помощь')
#         btn3 = types.KeyboardButton('Наши контакты')
#         markup.row(btn1)
#         markup.row(btn2, btn3)
#         pennij_bot.send_message(message.chat.id, 'Главная страница')


def liters(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1")
    btn2 = types.KeyboardButton("↩️ Назад к пиву")
    markup.row(btn1, btn2)
    markup.row(btn4, btn5, btn6)
    markup.row(btn8, btn7, btn9)

    pennij_bot.send_message(message.chat.id, 'Пиво на любой вкус:', reply_markup=markup)


def choosePivo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вайсберг")
    btn2 = types.KeyboardButton("Янтарное")
    btn3 = types.KeyboardButton("Стаут")
    btn4 = types.KeyboardButton("Домашнее")
    btn5 = types.KeyboardButton("82 Регион")
    btn6 = types.KeyboardButton("Чешское Элитное")
    btn7 = types.KeyboardButton("Чешское Нефильрованное")
    btn8 = types.KeyboardButton("↩️ Назад к ассортименту")
    btn9 = types.KeyboardButton("↩️ Назад в меню")
    markup.row(btn1, btn2, btn3)
    markup.row(btn4, btn5, btn6)
    markup.row(btn8, btn7, btn9)

    pennij_bot.send_message(message.chat.id, 'Пиво на любой вкус:', reply_markup=markup)


def goodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пиво и сидры")
    btn2 = types.KeyboardButton("Безалкогольное")
    btn3 = types.KeyboardButton("Рыбка")
    btn4 = types.KeyboardButton("Снеки")
    btn5 = types.KeyboardButton("↩️ Назад в меню")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5)

    if announcment:
        pennij_bot.send_message(message.chat.id, announcment)

    pennij_bot.send_message(message.chat.id, 'Всего лишь лучшее пиво в городе😉:',
                            reply_markup=markup)


pennij_bot.polling(none_stop=True)
