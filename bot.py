#! /usr/bin/python

"""
PremiumBot - Find premoum users in a chat, and export their info to a CSV
Authored by Shinanygans (shinanygans@proton.me)

"""
import logging 
from logging.handlers import TimedRotatingFileHandler
import sys
import csv
import asyncio

from config import (
API_ID,
API_HASH,
BOT_TOKEN,
AUTHORIZED_ADMINS
)

from telegram import Update, Message
from telegram.constants import ChatType, ParseMode
from telegram.error import RetryAfter, Forbidden, TimedOut, BadRequest, NetworkError
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Application
)

from telethon.sync import TelegramClient



# ******** Configure logging **********
when = 'midnight'  # Rotate logs at midnight (other options include 'H', 'D', 'W0' - 'W6', 'MIDNIGHT', or a custom time)
interval = 1  # Rotate daily
backup_count = 7  # Retain logs for 7 days
log_handler = TimedRotatingFileHandler('app.log', when=when, interval=interval, backupCount=backup_count)
log_handler.suffix = "%Y-%m-%d"  # Suffix for log files (e.g., 'my_log.log.2023-10-22')

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        log_handler,
    ]
)

# Create a separate handler for console output with a higher level (WARNING)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Set the level to WARNING or higher
console_formatter = logging.Formatter("KICKBOT: %(message)s")
console_handler.setFormatter(console_formatter)

# Attach the console handler to the root logger
logging.getLogger().addHandler(console_handler)

app = None

async def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message with information about the bot's available commands."""
    chat_id = update.effective_chat.id
    message=("""
    Welcome to PremiumBot, locator of Premium users in your chats.\n
To get started, make this bot an admin in a chat, and then type: \n/premium \nin that chat.\n
Keep this chat open. Status messages and command responses from the bot will be sent here.\n
"""
)
    await context.bot.send_message(chat_id=chat_id, text=message)
    return


async def premium(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    message = update.effective_message
    if user_id not in AUTHORIZED_ADMINS:
        return
    try:
        await delete_message_after_delay(message, 1)
        if chat_type is not ChatType.PRIVATE:
            response = await context.bot.send_message(
                chat_id=chat_id,
                text="<i style='color:#808080;'> Response will be sent privately.</i>",
                parse_mode=ParseMode.HTML
            )
            asyncio.create_task(delete_message_after_delay(response))

        else:
            response= await context.bot.send_message(
                chat_id=chat_id,
                text="<i style='color:#808080;'> Command must be used in the chat with the users you wish to evaluate.</i>",
                parse_mode=ParseMode.HTML
            )
            asyncio.create_task(delete_message_after_delay(response))           
        
        

        csv_filename = "premium.csv"

        with open(csv_filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["PREMIUM USER ID", "FULL NAME", "USERNAME"])


        premium_list = {}
        async for participant in telethon.iter_participants(chat_id):
            if participant and participant.premium:
                fullname = f"{participant.first_name}{' ' + participant.last_name if participant.last_name else ''}"
                username = f"@{participant.username if participant.username else 'None'}"
                premium_list[participant.id] = (fullname, username)


        for premium_user_id, premium_user_names in premium_list.items():
            premium_user_fullname = premium_user_names[0]
            premium_user_username = premium_user_names[1]

            with open(csv_filename, mode='a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write data for the current user
                csv_writer.writerow([premium_user_id, premium_user_fullname, premium_user_username])

        with open(csv_filename, 'rb') as csv_file:
            await context.bot.send_document(chat_id=user_id, document=csv_file, filename="premium.csv")

        

    except Forbidden as e:
        logging.error(f"{e}")
        message = await context.bot.send_message(
            chat_id=chat_id,
            text="<i style='color:#808080;'> Please open a chat with the bot to see responses.</i>",
            parse_mode=ParseMode.HTML
        )
        asyncio.create_task(delete_message_after_delay(message))
    

    except Exception as e:
        exc_type, _, exc_traceback = sys.exc_info()
        logging.error(f"{e} - Type = {exc_type} Line: {exc_traceback.tb_lineno}")

    return


async def delete_message_after_delay(message:Message, delay=3):
    try:
        await asyncio.sleep(delay)  # Wait for 'delay' seconds
        await app.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
    except Exception as e:
        logging.warning("Error deleting message.")
    return


async def premium_loop(update: Update, context: CallbackContext):
    asyncio.create_task(premium(update, context))
    return


def main() -> None:
    """Run bot."""
    global app

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("premium", premium_loop))

    # Run the bot until the user presses Ctrl-C
    try:
        app = application
        if API_ID and API_HASH:
            global telethon
            telethon = TelegramClient('memberlist_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

        application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
  
        
    except Exception as e:
            print(e)
        
    finally:
        try:
            if telethon.is_connected():
                telethon.disconnect()
        except Exception as e:
            print(e)



if __name__ == "__main__":
    main()