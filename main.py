import telebot

from config import TOKEN, currency_list
from extensions import Converter, APIException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Как там с деньгами?"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in currency_list.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, "Неверное количество параметров!")

    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.send_message(message.chat.id, f"Цена {amount} {base} в {sym} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")


bot.polling(none_stop=True)