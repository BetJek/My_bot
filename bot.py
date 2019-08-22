from glob import glob
from random import choice
import logging

from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings #импорт настроек

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def greet_user(bot, update):
    emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    text = 'привет {}'.format(emo)
    update.message.reply_text(text) #отправка сообщения пользователю


def talk_to_me(bot, update):
    user_text = update.message.text
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)  #Логирование бота
    update.message.reply_text(user_text)  #отправка сообщений


def send_cat_picture(bot, update):
    cat_list = glob('images/*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))


def main():
    mybot =Updater(settings.APY_KEY, request_kwargs=settings.PROXY)  #обьект класса Updater

    logging.info('Бот запускается')

    dp = mybot.dispatcher #обработчик событий
    dp.add_handler(CommandHandler('start', greet_user))  #вызов функции по команде
    dp.add_handler(CommandHandler('cat', send_cat_picture))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) #при вводе текста вызывать функцию talk_to_me


    mybot.start_polling()  #бот начинает поверять сообщения
    mybot.idle()  #бот будет работать до принудительной остановки

main()
#if __name__ = "__main__"