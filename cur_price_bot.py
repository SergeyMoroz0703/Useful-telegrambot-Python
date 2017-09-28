import logging
from time import sleep

import requests
import telebot
from learn_env.sergeyGit.pricetracker import Tracker
from telebot import types

from learn_env.sergeyGit.config import TOKEN

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
track = Tracker()


@bot.message_handler(func=lambda message: True)
def check_main_price(message):
    if message.text == 'price':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        button_main_prices = types.KeyboardButton(text="Check BTC, ETH, BTH")
        button_main_search = types.KeyboardButton(text="Search")
        keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        keyboard.add(button_main_prices)                                                                                 # this method added buttons in 2 rows
        #keyboard.row(button_main_prices,button_main_search)                                                             # this method added buttons in 1 rows like array
        bot.send_message(message.chat.id, "You can check price of main cryptocurrency, or just write me name of your currency", reply_markup=keyboard)

    if message.text == 'Check BTC, ETH, BTH':
        # button_main_search = types.KeyboardButton(text="Search")
        # keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
        # keyboard.add(button_main_search)
        # bot.send_message(message.chat.id, "Ok, one moment", reply_markup=keyboard)
        dict3 = track.main_price()
        try:
            btc_name = dict3[0]['name']
            btc_price = dict3[0]['price']
            eth_name = dict3[1]['name']
            eth_price = dict3[1]['price']
            hash_name = dict3[2]['name']
            hash_price = dict3[2]['price']
            btc_full_msg = str(btc_name + ' - ' + btc_price)
            eth_full_msg = str(eth_name + ' - ' + eth_price)
            hash_full_msg = str(hash_name + ' - ' + hash_price)
            msg = (btc_full_msg + '\n' + eth_full_msg + '\n' + hash_full_msg)
            bot.send_message(message.chat.id, msg)
            sleep(1)
        except Exception as e:
            bot.send_message(message.chat.id, e)

    if message.text is not None and message.text != 'price' and message.text != 'Check BTC, ETH, BTH':
        bot.send_message(message.chat.id, str('Wait please'))
        print(message.text)
        u_response = track.search_price(message.text)
        cur_name = u_response['name']
        cur_price = u_response['price']
        try:
            bot.send_message(message.chat.id, str(cur_name + ' - ' + cur_price))
        except Exception as e:
            bot.send_message(message.chat.id, e)

try:
    bot.polling(timeout=8)
except requests.exceptions.ConnectionError:
    print('Connection error, try again please')



