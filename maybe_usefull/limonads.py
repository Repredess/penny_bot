import telebot
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

lemonade_a = 1000
lemonade_b = 1000
lemonade_c = 3000
cart = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    lemonade_a_button = telebot.types.KeyboardButton('Лимонад A')
    lemonade_b_button = telebot.types.KeyboardButton('Лимонад B')
    lemonade_c_button = telebot.types.KeyboardButton('Лимонад C')
    cart_button = telebot.types.KeyboardButton('Корзина')
    markup.add(lemonade_a_button, lemonade_b_button, lemonade_c_button, cart_button)
    bot.send_message(message.chat.id, 'Выберите лимонад:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Корзина')
def show_cart(message):
    if not cart:
        bot.send_message(message.chat.id, 'Корзина пуста')
    else:
        total_price = 0
        cart_text = ''
        for item, quantity in cart.items():
            price = quantity * get_price(item)
            total_price += price
            cart_text += f'{item}: {quantity}л - {price}руб\n'
        cart_text += f'Итого: {total_price}руб'
        bot.send_message(message.chat.id, cart_text)

@bot.message_handler(func=lambda message: message.text in ['Лимонад A', 'Лимонад B', 'Лимонад C'])
def lemonade_menu(message):
    item = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    add_button = telebot.types.InlineKeyboardButton('+', callback_data=f'add_{item}')
    remove_button = telebot.types.InlineKeyboardButton('-', callback_data=f'remove_{item}')
    markup.add(add_button, remove_button)
    bot.send_message(message.chat.id, f'{item}: {get_quantity(item)}л', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def lemonade_callback(call):
    global cart
    item = call.data.split('_')[1]
    if call.data.startswith('add'):
        bot.answer_callback_query(call.id, f'Введите количество лимонада {item}:')
        bot.register_next_step_handler(call.message, lambda message: add_to_cart(message, item))
    elif call.data.startswith('remove'):
        if get_quantity(item) > 0:
            remove_from_cart(item)
            bot.answer_callback_query(call.id, f'Отнят 1л от лимонада {item}. Текущее количество: {get_quantity(item)}л')
        else:
            bot.answer_callback_query(call.id, f'Лимонад {item} уже закончился')

def add_to_cart(message, item):
    try:
        quantity = int(message.text)
        if quantity <= 0:
            raise ValueError
        if get_quantity(item) >= quantity:
            cart[item] = cart.get(item, 0) + quantity
            bot.send_message(message.chat.id, f'{quantity}л лимонада {item} добавлено в корзину')
        else:
            bot.send_message(message.chat.id, f'Недостаточно лимонада {item} на складе')
    except ValueError:
        bot.send_message(message.chat.id, 'Введите корректное количество (целое положительное число)')
        bot.register_next_step_handler(message, lambda message: add_to_cart(message, item))

def remove_from_cart(item):
    if item in cart:
        cart[item] -= 1
        if cart[item] == 0:
            del cart[item]

def get_quantity(item):
    if item == 'Лимонад A':
        return lemonade_a
    elif item == 'Лимонад B':
        return lemonade_b
    elif item == 'Лимонад C':
        return lemonade_c

def get_price(item):
    if item == 'Лимонад A':
        return 50
    elif item == 'Лимонад B':
        return 70
    elif item == 'Лимонад C':
        return 60

bot.polling()