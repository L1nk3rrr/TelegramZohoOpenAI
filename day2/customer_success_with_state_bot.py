import os
from enum import Enum

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, \
    ContextTypes, ConversationHandler

from keyboards import START_KEYBOARD
from zoho_tools import create_lead
from ai_tools import analyze_sentiment

load_dotenv()


class LeadInfo(Enum):
    ASK_FEEDBACK = 0
    ASK_NAME = 1
    ASK_EMAIL = 2
    ASK_CITY = 3
    ASK_FEEDBACK_TEXT = 4


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This is customer support bot. Please choose an option:",
        reply_markup=START_KEYBOARD,
    )
    return LeadInfo.ASK_FEEDBACK


async def feedback_decision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("What is your name?")
    return LeadInfo.ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data['name'] = name
    await update.message.reply_text("What is your email?")
    return LeadInfo.ASK_EMAIL


async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    context.user_data['email'] = email
    await update.message.reply_text("Which city are you from?")
    return LeadInfo.ASK_CITY


async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    context.user_data['city'] = city
    await update.message.reply_text("Please, leave your feedback:")
    return LeadInfo.ASK_FEEDBACK_TEXT


async def ask_feedback_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback = update.message.text
    context.user_data['feedback'] = feedback
    context.user_data['sentiment'] = await analyze_sentiment(feedback)
    await create_lead(context.user_data)
    await update.message.reply_text("Thank you!")
    return ConversationHandler.END


def main():
    lead_info_conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LeadInfo.ASK_FEEDBACK: [CallbackQueryHandler(feedback_decision)],
            LeadInfo.ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            LeadInfo.ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
            LeadInfo.ASK_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_city)],
            LeadInfo.ASK_FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_feedback_text)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(lead_info_conversation)
    application.run_polling()


if __name__ == "__main__":
    main()
