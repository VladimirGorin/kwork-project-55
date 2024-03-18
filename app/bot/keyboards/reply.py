from telebot import types

stop_reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
stop_reply_keyboard.add(types.KeyboardButton("Отменить"))

main_reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_reply_keyboard.add(types.KeyboardButton("Изминить настройки"))
main_reply_keyboard.add(types.KeyboardButton("Контроль"))
main_reply_keyboard.add(types.KeyboardButton("Информация"))
main_reply_keyboard.add(types.KeyboardButton("Добавить объяв."))
