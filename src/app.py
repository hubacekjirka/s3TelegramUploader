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
from urllib.request import HTTPRedirectHandler
import requests
import json
import subprocess

from uuid import uuid4

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

from s3 import upload_file_to_s3, list_s3_files
from quote import random_quote

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

bot_token = os.getenv("bot_token")
upload_passport = os.getenv("upload_password")
root_folder = os.path.dirname(os.path.realpath(__file__))

SECURITY, PHOTO = range(2)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info("Start command invoked")

    update.message.reply_text(
        "Hi, I'm a bot for the picture of the day app! "
        + "If you send me a photo and answer the security "
        + "question correctly, I'll put the picture into the "
        + "queue for you. How cool is that?! ]\n\n"
        + "Due to API limitation, I can only accept a single photo at a time. "
        + "Telegram heavily compresses photos, you better send them as documents."
    )
    update.message.reply_text("Here are commands you can use: /upload")


def help_command(update, context):
    """Send a message when the command /help is issued."""
    logger.info("Help command invoked")

    update.message.reply_text("Here are commands you can use: /start /upload")


def upload(update, context):
    """ Start upload conversation when /upload is issued."""
    logger.info("Upload conversation initiated")

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
    logger.info("Asking for upload password invoked")

    if update.effective_message.text == upload_passport:
        update.message.reply_text("That's correct!")
        update.message.reply_text(f"Random movie quote: {random_quote()}")
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
    logger.info("Photo command invoked")
    file_type = None

    if update.message.document:
        # Get photo uploaded as a document ~ full uncompressed size
        photo_file = update.message.document.get_file()

        if update.message.document.mime_type == "image/heic":
            file_type = "heic"
        elif update.message.document.mime_type == "image/jpeg":
            file_type = "jpg"
        else:
            raise Exception("Unrecognized file format")

        logger.info(f"Document update received of file type {file_type}")
    else:
        # The api doesn't support multiple photos uploaded within a single message.
        # Simply taking the last photo in the sequence, first two are thumbnails,
        # third is the highly compressed photo.
        photo_file = update.message.photo[-1].get_file()
        file_type = "jpg"
        logger.info("Photo update received")

    try:
        local_raw_file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "cache", f"{uuid4()}"
        )
        local_jpg_file_path = f"{local_raw_file_path}.jpg"

        # Download from Telegram API
        photo_file.download(local_raw_file_path)

        # Convert to jpg if HEIC is recfeived
        if file_type == "heic":
            logger.info("Converting from HEIC to jpg")
            subprocess.call(["convert", local_raw_file_path, local_jpg_file_path])
        elif file_type == "jpg":
            os.rename(local_raw_file_path, local_jpg_file_path)

        logger.info(f"Uploading photo: {local_raw_file_path}")
        update.message.reply_text("Got it, uploading ...")

        upload_file_to_s3(local_jpg_file_path)

        logger.info(f"Upload successful: {local_jpg_file_path}")
        update.message.reply_text("Finished uploading")

    except Exception as e:
        update.message.reply_text(f"Something  blew up when uploading to S3. {e}")
        logger.error(f"Error occured during uploading {local_raw_file_path} to S3: {e}")

    finally:
        # Cleanup, enclosed in try-except just in case we blew up on download already
        try:
            os.remove(local_raw_file_path)
            os.remove(local_jpg_file_path)
        except Exception:
            pass

        return ConversationHandler.END


def list(update, context):
    """
    List files present in the upload folder
    """
    logger.info("Listing files invoked")

    output = ""
    try:
        files = list_s3_files()
        logger.info("Listing files successful")

        # Format output as a file per line
        for f in files:
            output += f"{f}\n\n"

    except Exception as e:
        logger.error(f"Error occured during listing S3 folder: {e}")
        output = "Something blew up when listing S3 folder."

    finally:
        update.message.reply_text(output)


def diag(update, context):
    """
    Returns diagnostic information to user
    """
    logger.info("Diagnostic command invoked")

    update.message.reply_text(_get_diag())
    update.message.reply_text(f"Quote: {random_quote()}")


def _get_diag():
    """
    Retrieves diagnostic information from the underlying operating system
    """
    reply = ""

    # Linux system info
    linux_system_info = subprocess.check_output(["uname", "-v"]).decode("utf-8")
    reply += f"{linux_system_info}"

    # System info
    hostname = subprocess.check_output("hostname").decode("utf-8")
    reply += f"Hostname: {hostname}"

    uptime = subprocess.check_output("uptime").decode("utf-8")
    reply += f"Uptime: {uptime}"

    current_date = subprocess.check_output("date").decode("utf-8")
    reply += f"Date: {current_date}"

    try:
        # Public IP
        r = requests.get("http://ipinfo.io")
        ipinfo = json.loads(r.text)
        reply += f"Public IP: {ipinfo['ip']}\n"
    except Exception as e:
        logger.error(f"Failed getting public ip from ipinfo.io: {e}")
        reply += "Couldn't get public ip information from the web service."

    return reply


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(f"I don't know what you mean by {update.message.text}")
    update.message.reply_text("If you're stuck, type /cancel and start over.")


def end(update, context):
    logger.info("Cancel command invoked")
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
                    photo,
                ),
            ],
        },
        fallbacks=[MessageHandler(Filters.regex("^[cC]ancel$"), end)],
    )

    # add conversation handler
    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("list", list))
    dp.add_handler(CommandHandler("diag", diag))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    logger.info("S3 Telegram uploade started")
    main()
