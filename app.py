#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
upload_passport = os.getenv("upload_password")

SECURITY, PHOTO = range(2)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi, I'm a bot for the picture of the day app! "
                              + "If you send me a photo and answer the security "
                              + "question correctly, I'll put the picture into the "
                              + "queue for you. How cool is that?!")
    update.message.reply_text("Here are commands you can use: /upload")


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Here are commands you can use: /upload")


def upload(update, context):
    update.message.reply_text(
        "All right, let's upload some picture...")

    update.message.reply_text(
        "You may cancel the upload process anytime by simply typing cancel."
    )

    update.message.reply_text(
        "Just to make sure you know Jirka, what is the secret code for uploading "
        "a photo?"
    )

    return SECURITY


def upload_password(update, context):
    if update.effective_message.text == upload_passport:
        update.message.reply_text("That's correct!")
        update.message.reply_text("Send me the picture")
        return PHOTO

    else:
        update.message.reply_text("That's not correct ...")
        return ConversationHandler.END


def photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('cache/photo.jpg')

    return ConversationHandler.END


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def end(update, context):
    update.message.reply_text("Never mind...")
    return ConversationHandler.END


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1348053801:AAGlXKdupJ2W7zPrrwnWSXA3teq6C6NHtRE", use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', upload)],
        states={
            SECURITY: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                               upload_password)],
            PHOTO: [
                MessageHandler(Filters.photo, photo),
            ]
        },
        fallbacks=[MessageHandler(Filters.regex('^cancel$'), end)]
    )

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
