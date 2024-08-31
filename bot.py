import os

import openai  # noqa
import requests  # noqa
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! This is your bot.')


def main():
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == '__main__':
    main()
