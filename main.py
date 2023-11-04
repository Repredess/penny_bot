from telebot import types
import telebot
import webbrowser
import random
from config import BOT_TOKEN

"""
Команды для бота:
start - Вернуться к началу
help - Увидеть все команды
site - Перейти на сайт
"""

pennij_bot = telebot.TeleBot(BOT_TOKEN)
URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

answers = ['Я не понял, что ты хочешь сказать😲', 'Извини, я тебя не понимаю😅', 'Я не знаю такой команды🤔',
           'Я не понимаю о чем ты🙃']

final_order = []

announcment = False


# announcment = "Советуем пропробовать наше новое пиво 'Новое пиво'"


@pennij_bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🍻 Ассортимент 🐟')
    btn2 = types.KeyboardButton('🛟 Помощь')
    btn3 = types.KeyboardButton('📄 Контакты')
    markup.row(btn1)
    markup.row(btn2, btn3)

    pennij_bot.send_message(message.chat.id,
                            f"Привет, <b>{message.from_user.first_name}</b>! "
                            f"Скоро тут можно будет заказать пиво и рыбку ;)"
                            f"\nА пока можно посмотреть ассортимент и заказать по телефону",
                            parse_mode='html', reply_markup=markup)


@pennij_bot.message_handler(commands=["site", "website"])
def redirect_to_site(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти на сайт", url=URL))
    pennij_bot.send_message(message.chat.id, "Ах да, вот ссылочка:", reply_markup=markup)
    webbrowser.open(URL)


@pennij_bot.message_handler(commands=["help"])
def get_help(message):
    pennij_bot.send_message(message.chat.id,
                            "<b>Вернуться в начало</b>: <u>/start</u> "
                            "\n<b>По вопросам неисправностей или сотрудничества:</b> <u>@repredess</u>",
                            parse_mode='html')

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

    # Кнопка "ПИВО"
    elif message.text == 'Пиво':
        chooseBeer(message)
    elif message.text == 'Вайсберг':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup_inline = telebot.types.InlineKeyboardMarkup()
        btn1 = types.KeyboardButton('🛒 Добавить "Вайсберг"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Нежное пиво с сливочным послевкусием. Алкоголь 4.7.',
                              reply_markup=markup)
    elif message.text == 'Янтарное':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Янтарное"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Янтарное',
                              reply_markup=markup)
    elif message.text == 'Штормовое':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Штормовое"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Штормовое',
                              reply_markup=markup)
    elif message.text == 'Стаут':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Стаут"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Стаут',
                              reply_markup=markup)
    elif message.text == 'Домашнее':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Домашнее"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Домашнее',
                              reply_markup=markup)
    elif message.text == 'Регион 82':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Регион 82"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Регион 82',
                              reply_markup=markup)
    elif message.text == 'Чешское Элитное':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Чешское Элитное"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Чешское Элитное',
                              reply_markup=markup)
    elif message.text == 'Чешское Нефильтр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Чешское Нефильтр"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Чешское Нефильтр',
                              reply_markup=markup)
    elif message.text == 'Хорватское':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Хорватское"')
        btn2 = types.KeyboardButton('↩️ Назад к пиву')
        markup.row(btn1, btn2)
        pic = open("goods/pivo/Вайсберг.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Хорватское',
                              reply_markup=markup)

    # Кнопка "СИДРЫ"
    elif message.text == 'Сидры':
        chooseSidre(message)
    elif message.text == 'Голубая лагуна':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Голубая лагуна"')
        btn2 = types.KeyboardButton('↩️ Назад к сидрам')
        markup.row(btn1, btn2)
        pic = open("goods/ciders/laguna.png", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Вкуснятина голубого цвета. Райское наслаждение',
                              reply_markup=markup)
    elif message.text == 'Шампань':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Шампань"')
        btn2 = types.KeyboardButton('↩️ Назад к сидрам')
        markup.row(btn1, btn2)
        pic = open("goods/ciders/laguna.png", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Шампань',
                              reply_markup=markup)
    elif message.text == 'Сицилийский апельсин':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Сицилийский апельсин"')
        btn2 = types.KeyboardButton('↩️ Назад к сидрам')
        markup.row(btn1, btn2)
        pic = open("goods/ciders/laguna.png", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сицилийский апельсин',
                              reply_markup=markup)

    # Кнопка "БЕЗАЛКОГОЛЬНОЕ"
    elif message.text == 'Безалкогольное':
        pennij_bot.send_message(message.chat.id, 'Безалкогольного пока нет \nМало того - ты еще не выпил штрафную')

    # Кнопка "СНЕКИ"
    elif message.text == 'Снеки':
        chooseSnacs(message)
    # Виды снеков
    elif message.text == 'Сухарики':
        chooseCrackers(message)
    elif message.text == 'Сыр косичка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить косичку')
        btn2 = types.KeyboardButton('↩️ Назад к снекам')
        markup.row(btn1, btn2)
        pennij_bot.send_message(message.chat.id, 'Упругая и соленая', reply_markup=markup)
    elif message.text == 'Кнуты и палочки':
        chooseSticks(message)
    # Виды сухариков
    elif message.text == 'Деревенские':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Деревенские"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом сало-горчица. \nОстрота: [*][*][*]',
                              reply_markup=markup)
    elif message.text == 'Тайский перец':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Тайский перец"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом тайский перец. \nОстрота: [*][][]',
                              reply_markup=markup)
    elif message.text == 'Сливочный сыр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Сливочный сыр"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом вкусом сливочный сыр. \nОстрота: не острые',
                              reply_markup=markup)
    elif message.text == 'Ветчина-сыр':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Ветчина-сыр"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом ветчина-сыр. \nОстрота: не острые',
                              reply_markup=markup)
    elif message.text == 'Аджика':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Аджика"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом аджики. \nОстрота: не острые',
                              reply_markup=markup)
    elif message.text == 'Чесночный микс':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Чесночный микс"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом чесночка. \nОстрота: не острые',
                              reply_markup=markup)
    elif message.text == 'Краб':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Краб"')
        btn2 = types.KeyboardButton('↩️ Назад к сухарикам')
        markup.row(btn1, btn2)
        pic = open("goods/crackers/crackers.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Сухарики со вкусом краба. \nОстрота: не острые',
                              reply_markup=markup)
    # Виды рыбных палочек
    elif message.text == 'Мясные кнуты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Мясные кнуты"')
        btn2 = types.KeyboardButton('↩️ Назад к палочкам')
        markup.row(btn1, btn2)
        pennij_bot.send_message(message.chat.id, 'Мясные кнуты из говядины', reply_markup=markup)
    elif message.text == 'Палочки из щуки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Палочки из щуки""')
        btn2 = types.KeyboardButton('↩️ Назад к палочкам')
        markup.row(btn1, btn2)
        pennij_bot.send_message(message.chat.id, 'Рыбные палочки из щуки', reply_markup=markup)
    elif message.text == 'Палочки из тунца':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Палочки из тунца"')
        btn2 = types.KeyboardButton('↩️ Назад к палочкам')
        markup.row(btn1, btn2)
        pennij_bot.send_message(message.chat.id, 'Рыбные палочки из тунца', reply_markup=markup)
    elif message.text == 'Палочки из лосося':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить "Палочки из лосося"')
        btn2 = types.KeyboardButton('↩️ Назад к палочкам')
        markup.row(btn1, btn2)
        pennij_bot.send_message(message.chat.id, 'Рыбные палочки из лосося', reply_markup=markup)

    # Кнопка "РЫБКА"
    elif message.text == 'Рыбка':
        chooseFish(message)
    # Виды рыбки
    elif message.text == 'Корюшка':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить корюшки')
        btn2 = types.KeyboardButton('↩️ Назад к рыбке')
        markup.row(btn1, btn2)
        pic = open("goods/riba/koryushka.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Нежная слабо-соленая рыбка без косточек.',
                              reply_markup=markup)
    elif message.text == 'Тарань':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить тараньки')
        btn2 = types.KeyboardButton('↩️ Назад к рыбке')
        markup.row(btn1, btn2)
        pic = open("goods/riba/koryushka.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Рыба рыба рыба',
                              reply_markup=markup)
    elif message.text == 'Горбуша (копченая)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить горбуши')
        btn2 = types.KeyboardButton('↩️ Назад к рыбке')
        markup.row(btn1, btn2)
        pic = open("goods/riba/koryushka.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Рыба рыба рыба',
                              reply_markup=markup)
    elif message.text == 'Густера':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить густеры')
        btn2 = types.KeyboardButton('↩️ Назад к рыбке')
        markup.row(btn1, btn2)
        pic = open("goods/riba/koryushka.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Рыба рыба рыба.',
                              reply_markup=markup)
    elif message.text == 'Лещ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить леща')
        btn2 = types.KeyboardButton('↩️ Назад к рыбке')
        markup.row(btn1, btn2)
        pic = open("goods/riba/koryushka.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Рыба рыба рыба',
                              reply_markup=markup)
    elif message.text == 'Бычки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('🛒 Добавить бычков')
        btn2 = types.KeyboardButton('↩️ Назад к рыбке')
        markup.row(btn1, btn2)
        pic = open("goods/riba/koryushka.jpg", 'rb')
        pennij_bot.send_photo(message.chat.id, pic, 'Рыба рыба рыба',
                              reply_markup=markup)

    # Кнопки возврата
    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад к ассортименту':
        goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        welcome(message)
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
        pennij_bot.reply_to(message, f'{random.choice(answers)} \n<b>Вернуться на главную</b>: <u>/start</u>',
                            parse_mode='html')


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
    btn2 = types.KeyboardButton("Сыр косичка")
    btn3 = types.KeyboardButton("Кнуты и палочки")
    btn4 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    pennij_bot.send_message(message.chat.id, 'Каждый месяц что-то новое😋', reply_markup=markup)


def chooseSidre(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Голубая лагуна")
    btn2 = types.KeyboardButton("Шампань")
    btn3 = types.KeyboardButton("Сицилийский апельсин")
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

    pennij_bot.send_message(message.chat.id, 'Всегда свежая рыбка', reply_markup=markup)


def chooseBeer(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вайсберг")
    btn2 = types.KeyboardButton("Янтарное")
    btn3 = types.KeyboardButton("Штормовое")
    btn4 = types.KeyboardButton("Стаут")
    btn5 = types.KeyboardButton("Домашнее")
    btn6 = types.KeyboardButton("Регион 82")
    btn7 = types.KeyboardButton("Чешское Элитное")
    btn8 = types.KeyboardButton("Чешское Нефильтр")
    btn9 = types.KeyboardButton("Хорватское")
    btn10 = types.KeyboardButton("↩️ Назад к ассортименту")
    markup.row(btn1, btn2, btn4, btn6)
    markup.row(btn9, btn3, btn5)
    markup.row(btn7, btn8, btn10)

    pennij_bot.send_message(message.chat.id, 'Пиво на любой вкус😉 \nВыбирай любое:', reply_markup=markup)


def goodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пиво")
    btn2 = types.KeyboardButton("Сидры")
    btn3 = types.KeyboardButton("Безалкогольное")
    btn4 = types.KeyboardButton("Рыбка")
    btn5 = types.KeyboardButton("Снеки")
    btn6 = types.KeyboardButton("↩️ Назад в меню")
    markup.row(btn1, btn2)
    markup.row(btn3)
    markup.row(btn5, btn4, btn6)

    if announcment:
        pennij_bot.send_message(message.chat.id, announcment)

    pennij_bot.send_message(message.chat.id, 'Всего лишь лучшее пиво в городе😉',
                            reply_markup=markup)


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

pennij_bot.polling(none_stop=True)
