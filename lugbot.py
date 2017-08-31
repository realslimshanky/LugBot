# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import configparser
import logging
import requests
import re
import ast
from datetime import datetime, timedelta
from pytz import timezone, utc
from time import sleep
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('bot.ini')

meetupApi={'sign':'true','key':'Meetup-Api-Key'}

updater = Updater(token=config['BOT']['TOKEN'])
dispatcher = updater.dispatcher
help_text="""
[ x ] /invitelink  --> Prints the invite link to this group
[ x ] /twitter     --> Link to the ILUG-D Twitter
[ x ] /facebook    --> Facebook page of ILUG-D
[ x ] /mailinglist --> Link to the mailing list for ILUG-D
[ x ] /nextmeetup  --> Next/Current meetup page link
"""

def newMembers(bot, update):
    if update.message.new_chat_member != None:
        keyboard = [[InlineKeyboardButton("Guidelines", url='https://github.com/ILUGD/ILUGD.github.io/blob/master/CONTRIBUTORS.txt')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "Welcome, "+ update.message.new_chat_member.first_name + " @" + update.message.new_chat_member.username +". Please go through our guidelines."
        bot.sendChatAction(chat_id=update.message.chat_id,
                        action=ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id, text=text, reply_markup=reply_markup, one_time_keyboard=True)

def nextmeetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/ILUGDelhi/events', params=meetupApi)
        event_link=r.json()[0]['link']
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Event Page : %s
'''%(event_link))

def invitelink(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text=config['BOT']['invite_link'])

def twitter(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text=config['BOT']['twitter'])

def facebook(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text=config['BOT']['facebook'])

def mailinglist(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text=config['BOT']['mailing_list'])

def help(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text=help_text,parse_mode='Markdown')
    

dispatcher.add_handler(CommandHandler('nextmeetup', nextmeetup))
dispatcher.add_handler(CommandHandler('twitter',twitter))
dispatcher.add_handler(CommandHandler('invitelink',invitelink))
dispatcher.add_handler(CommandHandler('facebook',facebook))
dispatcher.add_handler(CommandHandler('mailinglist',mailinglist))
dispatcher.add_handler(CommandHandler('help',help))
dispatcher.add_handler(MessageHandler(Filters.all, newMembers))


updater.start_polling()
updater.idle()
