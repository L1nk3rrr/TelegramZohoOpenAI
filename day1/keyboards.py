from telegram import InlineKeyboardMarkup, InlineKeyboardButton

START_INLINE_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('Get Leads', callback_data='get_leads')],
        [InlineKeyboardButton('Button 2', callback_data='button_2')],
        [InlineKeyboardButton('Button 3', callback_data='button_3')],
    ]
)


def create_inline_keyboard_from_leads(leads_data: dict) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{lead['First_Name']} {lead['Last_Name']}: {lead['Email']}", callback_data=f"lead_{lead['id']}"
                )
            ]
            for lead in leads_data
        ]

    )
