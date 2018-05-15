from flask import Flask, request
import time
import telebot
from googletrans import Translator
translator = Translator()


bot = telebot.TeleBot("586264599:AAGxZI69-kOoqj4B3rWtMxSGdVKrr59d4eU", threaded=False)
bot.remove_webhook()
time.sleep(1)

all_words = [['beat', 'beat', 'beaten'], ['become', 'became', 'become'], ['begin', 'began', 'begun'], ['bend', 'bent', 'bent'], ['bet', 'bet', 'bet'], ['bite', 'bit', 'bitten'], ['bleed', 'bled', 'bled'], ['blow', 'blew', 'blown'], ['break', 'broke', 'broken'], ['breed', 'bred', 'bred'], ['bring', 'brought', 'brought'], ['build', 'built', 'built'], ['burn', 'burnt/burned', 'burnt/burned'], ['buy', 'bought', 'bought'], ['catch', 'caught', 'caught'], ['choose', 'chose', 'chosen'], ['come', 'came', 'come'], ['cost', 'cost', 'cost'], ['cut', 'cut', 'cut'], ['do', 'did', 'done'], ['dig', 'dug', 'dug'], ['draw', 'drew', 'drawn'], ['dream', 'dreamt/dreamed', 'dreamt/dreamed'], ['drink', 'drank', 'drunk'], ['drive', 'drove', 'driven'], ['eat', 'ate', 'eaten'], ['fall', 'fell', 'fallen'], ['feed', 'fed', 'fed'], ['feel', 'felt', 'felt'], ['fight', 'fought', 'fought'], ['find', 'found', 'found'], ['fly', 'flew', 'flown'], ['forget', 'forgot', 'forgotten'], ['forgive', 'forgave', 'forgiven'], ['freeze', 'froze', 'frozen'], ['get', 'got', 'got'], ['give', 'gave', 'given'], ['go', 'went', 'gone'], ['grow', 'grew', 'grown'], ['have', 'had', 'had'], ['hear', 'heard', 'heard'], ['hide', 'hid', 'hidden'], ['hit', 'hit', 'hit'], ['hold', 'held', 'held'], ['hurt', 'hurt', 'hurt'], ['keep', 'kept', 'kept'], ['know', 'knew', 'known'], ['lay', 'laid', 'laid'], ['lead', 'led', 'led'], ['lean', 'leant/leaned', 'leant/leaned'], ['leave', 'left', 'left'], ['lend', 'lent', 'lent'], ['let', 'let', 'let'], ['lose', 'lost', 'lost'], ['make', 'made', 'made'], ['mean', 'meant', 'meant'], ['meet', 'met', 'met'], ['pay', 'paid', 'paid'], ['put', 'put', 'put'], ['quit', 'quit', 'quit'], ['read /ri:d/', 'read /red/', 'read /red/'], ['ride', 'rode', 'ridden'], ['ring', 'rang', 'rung'], ['rise', 'rose', 'risen'], ['run', 'ran', 'run'], ['say', 'said', 'said'], ['see', 'saw', 'seen'], ['sell', 'sold', 'sold'], ['send', 'sent', 'sent'], ['set', 'set', 'set'], ['shake', 'shook', 'shaken'], ['shine', 'shone', 'shone'], ['shoe', 'shod', 'shod'], ['shoot', 'shot', 'shot'], ['show', 'showed', 'shown'], ['shrink', 'shrank', 'shrunk'], ['shut', 'shut', 'shut'], ['sing', 'sang', 'sung'], ['sink', 'sank', 'sunk'], ['sit', 'sat', 'sat'], ['sleep', 'slept', 'slept'], ['speak', 'spoke', 'spoken'], ['spend', 'spent', 'spent'], ['spill', 'spilt/spilled', 'spilt/spilled'], ['spread', 'spread', 'spread'], ['speed', 'sped', 'sped'], ['stand', 'stood', 'stood'], ['steal', 'stole', 'stolen'], ['stick', 'stuck', 'stuck'], ['sting', 'stung', 'stung'], ['stink', 'stank', 'stunk'], ['swear', 'swore', 'sworn'], ['sweep', 'swept', 'swept'], ['swim', 'swam', 'swum'], ['swing', 'swung', 'swung'], ['take', 'took', 'taken'], ['teach', 'taught', 'taught'], ['tear', 'tore', 'torn'], ['tell', 'told', 'told'], ['think', 'thought', 'thought'], ['throw', 'threw', 'thrown'], ['understand', 'understood', 'understood'], ['wake', 'woke', 'woken'], ['wear', 'wore', 'worn'], ['win', 'won', 'won'], ['write', 'wrote', 'written']]
secret = "GUID"
bot.set_webhook(url="https://sergeymoroz.pythonanywheres.com/{}".format(secret))

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, message.json['from']['first_name']+". I can help you with English here!\n"
                                                                         "If you want check all forms of irregular verbs, write 'verb irregular_word'\n"
                                                                         "For example: verb become")
# Handle 'verb irregular_verb'
@bot.message_handler(regexp="verb*")
def handle_word(message):
    new_msg = message.text.replace('verb ','')
    for pair in all_words:
        if new_msg in pair:
            translate = 'to '+new_msg + ' - '+(translator.translate('to '+new_msg, dest='ru').text)
            bot.send_message(message.chat.id, translate)
            msg = ' '.join(pair)
            bot.send_message(message.chat.id, msg)


# Handle 'verb word_to_translate'
@bot.message_handler(regexp="trans*")
def handle_word(message):
    new_msg = message.text.replace('trans ','')
    language = translator.detect(new_msg)
    if language.lang == 'ru':
        bot.reply_to(message, translator.translate(new_msg, dest='en').text)
    elif language.lang == 'en':
        bot.reply_to(message, translator.translate(new_msg, dest='ru').text)
