import telebot

import config

# замените 'YOUR_BOT_TOKEN' на ваш токен бота
bot = telebot.TeleBot(config.BOT_TOKEN)


# обработчик команды для отправки сообщения администратором
@bot.message_handler(commands=['to_all'])
def send_to_all(message):
    if message.from_user.id == config.ADMIN_ID:
        bot.send_message(message.chat.id, "Введите текст оповещения:")
        bot.register_next_step_handler(message, get_message)


def get_message(message):
    text = message.text
    bot.send_message(message.chat.id, f"Рассылаем? [да/нет]:\n{text}")

    @bot.message_handler(func=lambda message: message.text.lower() == 'да')
    def send_message_to_users(message):
        counter = 0
        user_ids = [5039223467, 1626668178]
        for user_id in user_ids:
            bot.send_message(user_id, text)
            counter += 1
            print(f'Sended to {user_id}')

        bot.send_message(message.chat.id, f'"{text}"\n\nSended to {counter} users!')


    @bot.message_handler(func=lambda message: message.text.lower() == 'нет')
    def cancel_announce(message):
        bot.send_message(message.chat.id, 'Cancel')

# запуск бота
bot.polling()
