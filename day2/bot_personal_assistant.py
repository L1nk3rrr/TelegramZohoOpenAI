import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from ai_tools import openai_client, get_assistant_response

load_dotenv()

user_dialog_context = {}
user_threads = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'am a personal assistant base on GPT-4o-min. How can I help U?")


# With chat.completions.create we must save and send a story with previous messages
async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    SYSTEM_PROMPT = (
        "You are personal assistant. "
    )
    user_id = update.effective_user.id
    if user_id not in user_dialog_context:
        user_dialog_context[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    user_dialog_context[user_id].append({"role": "user", "content": update.message.text})
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=user_dialog_context[user_id]
    )
    response_text = response.choices[0].message.content
    await update.message.reply_text(response_text)


async def chat_with_gpt_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    if user_id not in user_dialog_context:
        thread = await openai_client.beta.threads.create()
        user_threads[user_id] = thread.id
    response_text = await get_assistant_response(thread.id, message)
    await update.message.reply_text(response_text)


def main():
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt_assistant))
    application.run_polling()


if __name__ == "__main__":
    main()
