from telebot import types

stop_reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop_reply_keyboard.add(types.KeyboardButton("Отменить"))
