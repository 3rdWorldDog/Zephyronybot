import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot1.log', level=logging.INFO)

# PROXY = {'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')    
    update.message.reply_text('Hello, user! You called the /start command!')
    # print(update)

def talk_to_me(update, context):
    text=update.message.text
    print(text)
    update.message.reply_text(text)

def main():
    mybot=Updater(settings.API_KEY, use_context=True)

    dp=mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot has started')
    mybot.start_polling()
    mybot.idle()

main()
