from emoji import emojize
from ast import alias
import logging
from glob import glob
from random import choice, randint

import settings

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(filename='bot.log', level=logging.INFO)

# PROXY = {'proxy_url': settings.PROXY_URL,
#     'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    smile = choice(settings.USER_EMOJI)
    smile = emojize(smile, language='alias')
    print('Called /start')    
    update.message.reply_text(f"Hello, user! You called the /start command! {smile}")
    # print(update)

def talk_to_me(update, context):
    user_text = "Hello, {}! You send: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)
    #text=update.message.text
    #print(text)
    #update.message.reply_text(text)

def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"You guessed {user_number}, I'm guessed {bot_number}, You won!"
    elif user_number == bot_number:
        message = f"You guessed {user_number}, I'm guessed {bot_number}, Draw!"
    else:
        message = f"You guessed {user_number}, I'm guessed {bot_number}, You lost!"
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Enter an integer number'
    else:
        message = 'Enter a number'
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photos_list = glob('images/z*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id = chat_id, photo = open(cat_pic_filename, 'rb'))
    print('Cat image sent') 

# rb - read binary

def main():
    mybot=Updater(settings.API_KEY, use_context=True)

    dp=mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Bot has started')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()