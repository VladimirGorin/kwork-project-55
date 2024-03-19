from telebot import types

auth_inline_keyboard = types.InlineKeyboardMarkup(keyboard=[
    [types.InlineKeyboardButton(text="Авторизоваться", callback_data="new_auth")]])

ad_control_keyboard = types.InlineKeyboardMarkup(keyboard=[
    [
        types.InlineKeyboardButton(text="Выключить", callback_data="ad_off")
    ],    [
        types.InlineKeyboardButton(text="Включить", callback_data="ad_on")
    ]

])
