import random
import telebot
import webbrowser
from telebot import types

mytoken = "6860875409:AAE6Rtbw1xdbw-Uubnk_x1ZXP1q78Bj-CIM"
bot = telebot.TeleBot(mytoken)
answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.',
           'Мой разработчик не говорил, что отвечать в такой ситуации... >_<']


# Обработка команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    # Добавляем кнопки, которые будут появляться после ввода команды /start
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🍻 Ассортимент 🐟')
    button2 = types.KeyboardButton('⚙️ Настройки')
    button3 = types.KeyboardButton('📄 Справка')
    # Разделяю кнопки по строкам так, чтобы товары были отдельно от остальных кнопок
    markup.row(button1)
    markup.row(button2, button3)

    if message.text == '/start':
        # Отправляю приветственный текст
        bot.send_message(message.chat.id,
                         f"Привет, <b>{message.from_user.first_name}</b>! Тут можно будет заказать пиво и рыбку ;) ",
                         reply_markup=markup, parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Перекинул тебя в главное меню!', reply_markup=markup)


# Обработка фото. Если пользователь пришлет фото, то бот отреагирует на него. Можно реализовать свой функционал
@bot.message_handler(content_types='photo')
def get_photo(message):
    bot.send_message(message.chat.id, 'У меня нет возможности просматривать фото :(')


# Обработка обычных текстовых команд, описанных в кнопках
@bot.message_handler()
def info(message):
    if message.text == '🍻 Ассортимент 🐟':
        goodsChapter(message)
    elif message.text == '⚙️ Настройки':
        settingsChapter(message)
    elif message.text == '📄 Справка':
        infoChapter(message)
    elif message.text == '🔹 Товар #1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о первом товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #2':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о втором товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о третьем товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #4':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о четвертом товаре...', reply_markup=markup)
    elif message.text == '⚙️ Настройки #1':
        # Функционал не придумал
        bot.send_message(message.chat.id, 'Настройки номер 1...')
    elif message.text == '⚙️ Настройки #2':
        # Функционал не придумал
        bot.send_message(message.chat.id, 'Настройки номер 2...')
    elif message.text == '💳 Купить' or message.text == '✏️ Написать разработчику':
        # Сюда можете ввести свою ссылку на Телеграмм, тогда пользователя будет перекидывать к вам в личку
        webbrowser.open('https://t.me/repredess')
    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        welcome(message)
    # Если пользователь написал свое сообщение, то бот рандомно генерирует один из возможных вариантов ответа
    # Добавлять и редактировать варианты ответов можно в списке answers
    else:
        bot.send_message(message.chat.id, answers[random.randint(0, 3)])


# Функция, отвечающая за раздел товаров
def goodsChapter(message):
    # Кнопки для товаров
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Товар #1')
    button2 = types.KeyboardButton('🔹 Товар #2')
    button3 = types.KeyboardButton('🔹 Товар #3')
    button4 = types.KeyboardButton('🔹 Товар #4')
    button5 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)

    # Отправляем сообщение с прикрепленными к нему кнопками товаров
    bot.send_message(message.chat.id, 'Вот все товары, которые сейчас находятся в продаже:', reply_markup=markup)


# Функция, отвечающая за раздел настроек
def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('⚙️ Настройки #1')
    button2 = types.KeyboardButton('⚙️ Настройки #2')
    button3 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3)
    bot.send_message(message.chat.id, 'Раздел настроек.\nВыбери один из вариантов:', reply_markup=markup)


# Функция, отвечающая за раздел помощи
def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику')
    button2 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, 'Раздел справки.\nЗдесь ты можешь написать моему разработчику.',
                     reply_markup=markup)


# Строчка, чтобы программа не останавливалась
bot.polling(none_stop=True)
