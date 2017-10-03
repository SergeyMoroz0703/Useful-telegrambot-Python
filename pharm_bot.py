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
u_choices = []



@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Привет! Введите название лекарства, я постараюсь найти его  для Вас!')
    bot.register_next_step_handler(msg, check_pharm)



def check_pharm(message):
    global msg
    u_choice = message.text
    if tracker.check_is_exist(u_choice) == True:
        msg1 = bot.send_message(message.chat.id, 'Нашел препарат! Выберите, что конкретно хотите узнать?')
        button_subustance = types.KeyboardButton(text="Состав")
        button_indications = types.KeyboardButton(text="Показания")
        button_anti_indications = types.KeyboardButton(text="Противопоказания")
        button_method_eat = types.KeyboardButton(text="Дозировки")
        button_affects = types.KeyboardButton(text="Побочные эффекты")
        keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        keyboard.row(button_subustance, button_method_eat)
        keyboard.row(button_indications, button_anti_indications)
        keyboard.add(button_affects)
        msg = tracker.get_msg_bot(u_choice)
        bot.send_photo(message.chat.id, msg['imagelink'])
        bot.register_next_step_handler(msg1, make_choice)
    else:
        bot.send_message(message.chat.id, 'К сожалению, я не знаю такого препарата. Попробуйте найти здесь: https://tabletki.ua')
        sleep(1)
        abort_msg = bot.send_message(message.chat.id, 'Либо введите верное название препарата')
        bot.register_next_step_handler(abort_msg, check_pharm)

def make_choice(message):
    if message.text == 'Состав':
        answer = bot.send_message(message.chat.id, msg['substance'][:4096])
        bot.register_next_step_handler(answer, make_choice)
    elif message.text == 'Показания':
        answer = bot.send_message(message.chat.id, msg['indications'][:4096])
        bot.register_next_step_handler(answer, make_choice)
    elif message.text == 'Противопоказания':
        answer = bot.send_message(message.chat.id, msg['anti_indications'][:4096])
        bot.register_next_step_handler(answer, make_choice)
    elif message.text == 'Дозировки':
        answer = bot.send_message(message.chat.id, msg['method_eat'][:4096])
        bot.register_next_step_handler(answer, make_choice)
    elif message.text == 'Побочные эффекты':
        answer = bot.send_message(message.chat.id, msg['affects'][:4096])
        bot.register_next_step_handler(answer, make_choice)



try:
    bot.polling(timeout=15)
except requests.exceptions.ConnectionError:
    print('Connection error, try again please')







