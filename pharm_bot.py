import logging
from time import sleep, time

import requests
import telebot
from learn_env.sergeyGit.medical_checker import Tracker
from telebot import types

from learn_env.sergeyGit.config import TOKEN_SERGEY


tracker = Tracker()
bot = telebot.TeleBot(TOKEN_SERGEY)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Введите название лекарства, я постараюсь найти его  для Вас!')



@bot.message_handler(func=lambda message: True)
def check_pharm(message):

    u_choice = message.text
    if tracker.check_is_exist(u_choice) == True:
        msg = tracker.get_msg_bot(u_choice)
        button_subustance = types.KeyboardButton(text="Состав")
        button_indications = types.KeyboardButton(text="Показания")
        button_anti_indications = types.KeyboardButton(text="Противопоказания")
        button_method_eat = types.KeyboardButton(text="Дозировки")
        button_affects = types.KeyboardButton(text="Побочные эффекты")
        keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        #keyboard.add(button_subustance,button_indications,button_anti_indications,button_method_eat,button_affects,button_affects)
        keyboard.row(button_subustance, button_method_eat)
        keyboard.row(button_indications,button_anti_indications)
        keyboard.add(button_affects)
        bot.send_message(message.chat.id, 'Несколько секунд, готовлю ответ...', reply_markup=keyboard)
        msg = tracker.get_msg_bot(u_choice)
        print(msg['substance'])
        if message.text == 'Состав' and message.text != u_choice:
            bot.send_message(message.chat.id, msg['substance'])
        elif message.text == 'Показания' and message.text != u_choice:
            bot.send_message(message.chat.id, msg['indications'])



  #  else:
        bot.send_message(message.chat.id, 'К сожалению, я не знаю такого препарата. Попробуйте найти здесь: https://tabletki.ua')
        sleep(1)
        bot.send_message(message.chat.id,
                         'Либо введите верное название препарата')






# def send_substance(message = u_choice):
#     msg = tracker.get_msg_bot(u_choice)['substance']
#     bot.send_message(message.chat.id, msg)

try:
    bot.polling(timeout=15)
except requests.exceptions.ConnectionError:
    print('Connection error, try again please')