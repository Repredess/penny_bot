import telebot
from config import BOT_TOKEN

# создаем бота и указываем его токен
bot = telebot.TeleBot(BOT_TOKEN)

# создаем словарь с товарами
products = {'product1': 100, 'product2': 200}

# создаем словарь для хранения корзины пользователя
cart = {}


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    # отправляем приветственное сообщение
    bot.send_message(message.chat.id, 'Привет! Я бот для покупок. Чтобы посмотреть список товаров, нажми /products')


# обработчик команды /products
@bot.message_handler(commands=['products'])
def products_handler(message):
    # отправляем список товаров
    bot.send_message(message.chat.id,
                     'Список товаров:\n\n' + '\n'.join([f'{k}: {v} руб.' for k, v in products.items()]))


# обработчик кнопки "Добавить в корзину"
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
def add_handler(call):
    # получаем название товара и его цену из callback_data
    product = call.data.split('_')[1]
    price = products[product]

    # добавляем товар в корзину пользователя
    if product in cart:
        cart[product] += price
    else:
        cart[product] = price

    # отправляем сообщение об успешном добавлении товара
    bot.answer_callback_query(call.id, f'Товар "{product}" добавлен в корзину')


# обработчик кнопки "Убрать из корзины"
@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_'))
def remove_handler(call):
    # получаем название товара и его цену из callback_data
    product = call.data.split('_')[1]
    price = products[product]

    # убираем товар из корзины пользователя
    if product in cart:
        cart[product] -= price
        if cart[product] == 0:
            del cart[product]

    # отправляем сообщение об успешном удалении товара
    bot.answer_callback_query(call.id, f'Товар "{product}" удален из корзины')


# обработчик команды /cart
@bot.message_handler(commands=['cart'])
def cart_handler(message):
    # отправляем содержимое корзины пользователя
    if not cart:
        bot.send_message(message.chat.id, 'Корзина пуста')
    else:
        bot.send_message(message.chat.id,
                         'Содержимое корзины:\n\n' + '\n'.join([f'{k}: {v} руб.' for k, v in cart.items()]))


# обработчик команды /order
@bot.message_handler(commands=['order'])
def order_handler(message):
    # создаем inline клавиатуру с кнопкой "Оформить заказ"
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Оформить заказ', callback_data='order'))

    # отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, 'Чтобы оформить заказ, нажми на кнопку "Оформить заказ"', reply_markup=keyboard)


# обработчик кнопки "Оформить заказ"
@bot.callback_query_handler(func=lambda call: call.data == 'order')
def order_confirm_handler(call):
    # создаем inline клавиатуру с кнопками "Да" и "Нет"
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Да', callback_data='confirm_order'),
                 telebot.types.InlineKeyboardButton('Нет', callback_data='cancel_order'))

    # отправляем сообщение с клавиатурой
    bot.send_message(call.message.chat.id, 'Вы уверены, что хотите оформить заказ?', reply_markup=keyboard)


# обработчик кнопки "Да" при оформлении заказа
@bot.callback_query_handler(func=lambda call: call.data == 'confirm_order')
def confirm_order_handler(call):
    # отправляем сообщение с просьбой ввести номер телефона
    bot.send_message(call.message.chat.id, 'Нажмите кнопку "Поделиться контактом", что бы мы могли с тобой связаться')

    # добавляем callback_data для следующего шага
    bot.register_next_step_handler(call.message, phone_handler)


# обработчик ввода номера телефона
def phone_handler(message):
    # сохраняем номер телефона и отправляем сообщение с подтверждением заказа
    phone = message.text
    bot.send_message(message.chat.id, f'Ваш заказ:\n\n' + '\n'.join(
        [f'{k}: {v}руб.' for k, v in cart.items()]) + f'\n\nТелефон: {phone}\n\nСпасибо за заказ!')


# очищаем корзину пользователя
cart.clear()


# обработчик кнопки "Нет" при оформлении заказа
@bot.callback_query_handler(func=lambda call: call.data == 'cancel_order')
def cancel_order_handler(call):
    # отправляем сообщение об отмене заказа
    bot.send_message(call.message.chat.id, 'Заказ отменен')


# запускаем бота
bot.polling()
...
