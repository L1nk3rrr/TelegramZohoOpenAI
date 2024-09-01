import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from keyboards import START_KEYBOARD

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This is customer support bot. Please choose an option:",
        reply_markup=START_KEYBOARD,
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "submit_feedback":
        context.user_data["awaiting_feedback"] = True
        await query.edit_message_text(text="Please send your feedback:")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_feedback"):
        feedback = update.message.text
        await update.message.reply_text(f"Thank you for your feedback: {feedback}")
        del context.user_data["awaiting_feedback"]
        # create_lead(feedback, context)
    await update.message.reply_text(
        "Please choose an option:", reply_markup=START_KEYBOARD
    )


def main():
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()


if __name__ == "__main__":
    main()
