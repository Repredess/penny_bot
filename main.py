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

PIVO = {'85 region': 101,
        'Shtormovoe': 124}

final_order = []

announcment = False


@pennij_bot.message_handler(commands=["start"])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Ассортимент')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Наши контакты')
    markup.row(btn1)
    markup.row(btn2, btn3)

    pennij_bot.send_message(message.chat.id,
                            f"Привет, <b>{message.from_user.first_name}</b>! Тут можно будет заказать пиво и рыбку ;) ",
                            parse_mode='html', reply_markup=markup)


@pennij_bot.message_handler()
def user_messages(message):
    if message.text == 'Ассортимент':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Пиво и сидры")
        btn2 = types.KeyboardButton("Безалкогольное")
        markup.row(btn1, btn2)
        btn3 = types.KeyboardButton("Рыбка")
        btn4 = types.KeyboardButton("Снеки")
        markup.row(btn3, btn4)
        pennij_bot.reply_to(message, 'Вот наш ассортимент:', reply_markup=markup)
        if announcment:
            pennij_bot.send_message(message.chat.id, announcment)
    elif message.text == 'Помощь':
        pennij_bot.send_message(message.chat.id, 'Держись, брат!')
    elif message.text == 'Наши контакты':
        pennij_bot.send_message(message.chat.id, '<i>+79155633989</i> - <b>Кирилл</b>', parse_mode='html')
    else:
        pennij_bot.reply_to(message, 'Я не понимаю о чем ты🙃 \n<b>Вернуться на главную</b>: <u>/start</u>',
                            parse_mode='html')

pennij_bot.polling(none_stop=True)
