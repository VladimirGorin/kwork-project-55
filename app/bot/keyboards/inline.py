from telebot import types

auth_inline_keyboard = types.InlineKeyboardMarkup(keyboard=[
    [types.InlineKeyboardButton(text="Авторизоваться", callback_data="new_auth")]])
