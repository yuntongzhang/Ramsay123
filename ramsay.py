#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Bot to recommend dishes according to dietary preference.

"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler

import logging
import food_dict
import random
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Calories', 'Protein/g'],
                  ['Fat/g', 'Sodium/mg'],
                  ['Analyze']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)



def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def start(bot, update):
    update.message.reply_text(
        "Hi! I am Ramsay123. Simply key in the how much of each nutrients you want. "
        "And you will see the desired diet to match the nutrients! "
        "Make sure you enter value for all 4 nutrients."
        "Format: lower bound-upper bound",
        reply_markup=markup)

    return CHOOSING

def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text(
        'The {}? Yes, that definitely helps me to make decision!'.format(text.lower()))

    return TYPING_REPLY

def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING

# The analysis step which calls the check method in food_dict
def analyze(bot, update, user_data):
    try:
        if 'choice' in user_data:
            del user_data['choice']
        temp = []
        temp.extend(user_data['Calories'].split("-"))
        temp.extend(user_data['Protein/g'].split("-"))
        temp.extend(user_data['Fat/g'].split("-"))
        temp.extend(user_data['Sodium/mg'].split("-"))
        
        ch = food_dict.check(temp)
        if ch==0:
            update.message.reply_text("No dish found T.T")
            
        else:
            index = random.randint(0, len(ch)-1)
            
            result = ch[index]
            url = 'http://www.google.com/search?q='+ result[0].replace(' ','+')
            printout = '\n'+result[0]+ '\nRating: '+result[1]+'/5'+ '\nCalories: '+result[2]+'\nProtein: '+result[3]+ 'g'+'\nFat: '+result[4]+'g'+'\nSodium: '+ result[5] +'mg' +'\nGoogle: '+url

            
            
            update.message.reply_text("The dish that suits you the most is:""{}".format(printout))
        user_data.clear()
        return ConversationHandler.END
    except:
        update.message.reply_text("Input Missing. Please Try Again")
        return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Set these variable to the appropriate values
    TOKEN = "612484245:AAGQ9eC9YbUzB6LYipES9OAe_nCUP6YaKQs"
    NAME = "ramsay123"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Calories|Protein/g|Fat/g|Sodium/mg)$',
                                    regular_choice,
                                    pass_user_data=True)
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Analyze$', analyze, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot with polling. This is not used when deploying on heroku
    # updater.start_polling()

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
