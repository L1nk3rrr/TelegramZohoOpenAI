from telegram import InlineKeyboardMarkup, InlineKeyboardButton

START_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Submit Feedback", callback_data="submit_feedback"), ]
    ]
)
