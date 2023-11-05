import telebot
from config import BOT_TOKEN

# создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# создаем корзину
cart = {'Лимонад': 0, 'Сухарики': 0}

# описание товаров
lemonade_description = 'Охлажденный лимонад в стеклянной бутылке объемом 1 литр.'
cookies_description = 'Сухарики из пшеничной муки, упаковка весом 100 грамм.'


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я бот для заказа лимонада и сухариков. Выбери, что тебе нужно:',
                     reply_markup=get_main_menu())


# функция для получения главного меню
def get_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    lemonade_button = telebot.types.KeyboardButton('Лимонад')
    cookies_button = telebot.types.KeyboardButton('Сухарики')
    markup.add(lemonade_button, cookies_button)
    return markup


# функция для получения меню товара
def get_product_menu(product_name):
    markup = telebot.types.InlineKeyboardMarkup()
    add_button = telebot.types.InlineKeyboardButton('+', callback_data=f'add_{product_name}')
    remove_button = telebot.types.InlineKeyboardButton('-', callback_data=f'remove_{product_name}')
    cart_button = telebot.types.InlineKeyboardButton('Корзина', callback_data='cart')
    markup.add(add_button, remove_button, cart_button)
    return markup


# обработчик кнопок в меню товара
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    global cart
    if call.data.startswith('add'):
        product_name = call.data.split('_')[1]
        cart[product_name] += 1
    elif call.data.startswith('remove'):
        product_name = call.data.split('_')[1]
        if cart[product_name] > 0:
            cart[product_name] -= 1
        else:
            bot.answer_callback_query(call.id, text=f'{product_name} уже закончились.')
    elif call.data == 'cart':
        cart_text = '\n'.join([f'{product_name}: {quantity}' for product_name, quantity in cart.items()])
        bot.send_message(call.message.chat.id, f'Корзина:\n{cart_text}',
                         reply_markup=get_main_menu())  # добавляем кнопку "Назад" в меню корзины
        return
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=get_product_menu(product_name))


# обработчик команды Лимонад
@bot.message_handler(func=lambda message: message.text == 'Лимонад')
def lemonade_message(message):
    bot.send_message(message.chat.id, lemonade_description, reply_markup=get_product_menu('Лимонад'))


# обработчик команды Сухарики
@bot.message_handler(func=lambda message: message.text == 'Сухарики')
def cookies_message(message):
    bot.send_message(message.chat.id, cookies_description, reply_markup=get_product_menu('Сухарики'))


# запускаем бота
bot.polling()
