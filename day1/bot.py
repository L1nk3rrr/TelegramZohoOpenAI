import os

import openai  # noqa
import requests  # noqa
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters, Application,
                          CallbackQueryHandler)
from dotenv import load_dotenv

from keyboards import START_INLINE_KEYBOARD, create_inline_keyboard_from_leads
from zoho_tools import make_zoho_api_get_request, ZOHO_API_CRM_URL

load_dotenv()


async def start_reply(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup([["Key1", "Key2"], ["Key3"], ["Key4", "Key5", "Key6"]], resize_keyboard=True,
                                   one_time_keyboard=True)
    await update.message.reply_text('Hello! This is your bot.', reply_markup=keyboard)
    await update.message.reply_photo(photo='/Users/l1nk3r/projects/TelegramZohoOpenAI/hello_image.jpg')


async def start_inline(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Choose one button', reply_markup=START_INLINE_KEYBOARD)


async def button_handler(update: Update, context):
    query = update.callback_query
    if query.data == "get_leads":
        leads = make_zoho_api_get_request(ZOHO_API_CRM_URL)
        leads_keyboard = create_inline_keyboard_from_leads(leads['data'])
        await query.edit_message_text(text='Select Lead', reply_markup=leads_keyboard)
    else:
        await query.message.reply_text(text=f"You chose {query.data}", reply_markup=START_INLINE_KEYBOARD)


async def echo(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    await update.message.reply_text(f"Hello, I'v got your message: \n {message_text}")


async def post_init(application: Application):
    await application.bot.send_message(chat_id=os.getenv('ADMIN_CHAT_ID'), text='Bot has been started')


def main():
    app = (ApplicationBuilder()
           .token(os.getenv('TELEGRAM_TOKEN'))
           .post_init(post_init)
           .build())
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # app.add_handler(CommandHandler("start", start_reply))
    app.add_handler(CommandHandler("start", start_inline))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


if __name__ == '__main__':
    main()
