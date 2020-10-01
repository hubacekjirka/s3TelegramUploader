"""
S3 telegram uploader bot inspired by python-telegram-bot examples.
Creadit: https://github.com/python-telegram-bot/python-telegram-bot

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

Commands for BotFather:
start - Show welcome message
upload - Initiate upload conversation
cancel - Resets ongoing conversation
help - Displays bot's manual
"""

import logging
import os

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from s3 import upload_file_to_s3, list_s3_files

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

bot_token = os.getenv("bot_token")
upload_passport = os.getenv("upload_password")

SECURITY, PHOTO = range(2)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi, I'm a bot for the picture of the day app! "
        + "If you send me a photo and answer the security "
        + "question correctly, I'll put the picture into the "
        + "queue for you. How cool is that?!"
    )
    update.message.reply_text("Here are commands you can use: /upload")


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Here are commands you can use: /start /upload")


def upload(update, context):
    """ Start upload conversation when /upload is issued."""
    update.message.reply_text("All right, let's upload some picture...")
    update.message.reply_text(
        "You may cancel the upload process anytime by simply typing cancel."
    )
    update.message.reply_text(
        "Just to make sure you know Jirka and he wants you to contribute "
        " to the photo of the day. What is the secret code for uploading "
        "a photo?"
    )
    return SECURITY


def upload_password(update, context):
    """
    Asks for upload passport. On success, proceeds to photo upload,
    otherwise ends the conversation
    """
    if update.effective_message.text == upload_passport:
        update.message.reply_text("That's correct!")
        update.message.reply_text("Send me the picture you would like to upload")
        return PHOTO

    else:
        update.message.reply_text("You chose poorly.")
        return ConversationHandler.END


def photo(update, context):
    """
    Store photo in the cache folder under the update's unique number, then
    attempt upload to the S3 bucket.
    """
    #TODO:
    photo_file = update.message.document.get_file()
    #photo_file = update.message.photo[-1].get_file()

    file_path = f"cache/{update.update_id}.jpg"
    photo_file.download(file_path)

    try:
        update.message.reply_text("Got it, uploading ...")
        upload_file_to_s3(file_path)
        update.message.reply_text("Finished uploading")

    except Exception as e:
        logger.error(f"Error occured during uploading to S3: {e}")

    finally:
        return ConversationHandler.END


def list(update, context):
    """
    List files present in the upload folder
    """
    output = ""
    try:
        files = list_s3_files()
        for f in files:
            output += f"{f}\n"

    except Exception as e:
        logger.error(f"Error occured during listing S3 folder: {e}")
        output = "Something blew up when listing S3 folder."

    finally:
        update.message.reply_text(output)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(f"I don't know what you mean by {update.message.text}")
    update.message.reply_text("If you're stuck, type /cancel and start over.")


def end(update, context):
    update.message.reply_text("Never mind...")
    return ConversationHandler.END


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("upload", upload)],
        states={
            SECURITY: [
                MessageHandler(
                    Filters.text & ~Filters.regex("^[cC]ancel$"),
                    upload_password,
                )
            ],
            PHOTO: [
                MessageHandler(
                    # Filters.document ~ accepts message with photo as a document
                    # Using document upload, telegram doesn't automaticially resize
                    # the image
                    #
                    # Filters.photo ~ standard photo upload when images get resized
                    # to around 200 KB
                    Filters.document | Filters.photo,
                    photo),
            ],
        },
        fallbacks=[MessageHandler(Filters.regex("^[cC]ancel$"), end)],
    )

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("list", list))

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
