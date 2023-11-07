# ANSWERS = ["Красивое фото😉",
#            "Хорошее фото",
#            "Ты во мне ценителя фотографии увидел!?",
#            "Будем считать что я этого не видел...",
#            "Горжусь тобой"]
#
# URL = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
#
# @pennij_bot.message_handler(commands=["start"])
# def main(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.KeyboardButton('/check')
#     btn2 = types.KeyboardButton('/site')
#     btn3 = types.KeyboardButton('/help')
#     markup.row(btn1)
#     markup.row(btn2, btn3)
#
#     pennij_bot.send_message(message.chat.id,
#                             f"Привет, <b>{message.from_user.first_name}</b>! Тут можно будет заказать пиво и рыбку ;) "
#                             f"\nУвидеть все команды: <u>/help</u>",
#                             parse_mode='html', reply_markup=markup)
#
#     # pennij_bot.register_next_step_handler(message, on_click)
#
#
# # def on_click(message):
# #     markup = types.InlineKeyboardMarkup()
# #     if message.text == 'Наш ассортимент':
# #         pennij_bot.send_message(message.chat.id, "Вот наш ассортимент")
# #         pennij_bot.register_next_step_handler(message, on_click)
# #     elif message.text == 'Наш сайт':
# #         markup.add(types.InlineKeyboardButton("Перейти на сайт", url=URL))
# #         pennij_bot.send_message(message.chat.id, "Наш сайт:", reply_markup=markup)
# #         pennij_bot.register_next_step_handler(message, on_click)
# #     elif message.text == 'Помощь':
# #         pennij_bot.send_message(message.chat.id, "<b>Нажми меня</b> >>> <i>/help</i>", parse_mode="html")
# #         pennij_bot.register_next_step_handler(message, on_click)
# #     else:
# #         pennij_bot.send_message(message.chat.id,
# #                                 "<b>Вернуться в начало</b>: <u>/start</u> \n<b>Выбрать ништячков</b>: <u>/check</u>",
# #                                 parse_mode='html')
#
# @pennij_bot.message_handler(commands=["check"])
# def check(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Пиво", callback_data='pivo'))
#     markup.add(types.InlineKeyboardButton("Безалкогольное", callback_data='bezalco'))
#     markup.add(types.InlineKeyboardButton("Рыбка", callback_data='ribka'))
#     markup.add(types.InlineKeyboardButton("Снеки", callback_data='snacs'))
#
#     pennij_bot.send_message(message.chat.id, "Вот наш ассортимент:")
#
#
# @pennij_bot.message_handler(commands=["site", "website"])
# def redirect_to_site(message):
#     markup = types.InlineKeyboardMarkup()
#     markup.add(types.InlineKeyboardButton("Перейти на сайт", url=URL))
#     pennij_bot.send_message(message.chat.id, "Ах да, вот ссылочка:", reply_markup=markup)
#     webbrowser.open(URL)
#
#
# @pennij_bot.message_handler(commands=["help"])
# def get_help(message):
#     pennij_bot.send_message(message.chat.id,
#                             "<b>Вернуться в начало</b>: <u>/start</u> \n<b>Выбрать ништячков</b>: <u>/check</u>",
#                             parse_mode='html')
#
#
# @pennij_bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
#     if callback.data == "delete":
#         pennij_bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
#     elif callback.data == "edit":
#         pennij_bot.edit_message_text('Сообщение изменено', callback.message.chat.id, callback.message.message_id)
#     elif callback.data == "Пиво":
#         pass
#
#
# @pennij_bot.message_handler(commands=["info"])
# def get_info(message):
#     pennij_bot.send_message(message.chat.id,
#                             message)
#
#
# @pennij_bot.message_handler(content_types=["photo"])
# def get_photo(message):
#     markup = types.InlineKeyboardMarkup(resize_keyboard=True)
#     btn1 = types.InlineKeyboardButton("Перейти на сайт", url=URL)
#     markup.row(btn1)
#     btn2 = types.InlineKeyboardButton("Удалить фото", callback_data='delete')
#     btn3 = types.InlineKeyboardButton("Изменить текст", callback_data='edit')
#     markup.row(btn2, btn3)
#     answer = random.choice(ANSWERS)
#     pennij_bot.reply_to(message, answer, reply_markup=markup)
#
#
# @pennij_bot.message_handler()
# def user_messages(message):
#     if message.text.lower() == 'id':
#         pennij_bot.reply_to(message, f'Твой ID: {message.from_user.id}')
#     elif message.text.lower() == 'баллы':
#         pennij_bot.send_message(message.chat.id, 'Пока 0')
#     else:
#         pennij_bot.reply_to(message, 'Я не понимаю о чем ты🙃 \n<b>Вернуться на главную</b>: <u>/start</u>',
#                             parse_mode='html')
#
# # pennij_bot.infinity_polling()