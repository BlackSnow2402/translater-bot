import config
import telebot
import requests
import db

translate_url = config.yandex_translate_url
detect_url = config.yandex_detect_url
get_langs_url = config.yandex_get_langs_url
key = config.yandex_key

get_langs = requests.post(get_langs_url,
                              data={'key': key,
                                    'ui': 'en'})
langs_list = get_langs.json()['langs']
bot = telebot.TeleBot(config.bot_token)

@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = db.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_PHRASE.value:
        bot.send_message(message.chat.id, "Жду ввода фразы...")
    elif state == config.States.S_ENTER_LANG.value:
        bot.send_message(message.chat.id, "Жду ввода языка...")
    else:
        bot.send_message(message.chat.id, "Привет! Введи фразу, которую хочешь перевести")
        db.set_state(message.chat.id, config.States.S_ENTER_PHRASE.value)
        

@bot.message_handler(commands=["restart"])
def cmd_restart(message):
    bot.send_message(message.chat.id, "Привет! Введи фразу, которую хочешь перевести")
    db.set_state(message.chat.id, config.States.S_ENTER_PHRASE.value)
    

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id).decode("utf-8") == config.States.S_ENTER_PHRASE.value)
def get_phrase(message):
    message_phrase = message.text
    detect_lang = requests.post(detect_url,
                            data={'key': key,
                                  'text': message.text})
    bot.send_message(message.chat.id,
                     "Введите название языка, на который хотите перевести фразу "
                     + "\"" + message_phrase + "\"")
    db.set_state(message.chat.id, config.States.S_ENTER_LANG.value)
    db.set_phrase(message.chat.id, message.text)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id).decode("utf-8") == config.States.S_ENTER_LANG.value)
def translate(message):
    language = requests.post(translate_url, data={'key': key,
                                                  'text': message.text,
                                                  'lang': "en"})
    lang = ''
    index = 0
    for i in range(len(list(langs_list.values()))):
        if ''.join(language.json()['text']) == list(langs_list.values())[i]:
            lang = list(langs_list.keys())[i]
            index = i
    if lang == '':
        bot.send_message(message.chat.id, "Не знаю такого языка, попробуй снова")
    else:
        translate = requests.post(translate_url, data={'key': key,
                                                       'text': db.get_phrase(message.chat.id).decode("utf-8"),
                                                       'lang': list(langs_list.keys())[index]})
        bot.send_message(message.chat.id, translate.json()['text'])
        bot.send_message(message.chat.id, "Введи фразу, которую хочешь перевести")
        db.set_state(message.chat.id, config.States.S_ENTER_PHRASE.value)
        db.set_phrase(message.chat.id, '')       
    
    

if __name__ == '__main__':
    bot.polling(none_stop=True)
