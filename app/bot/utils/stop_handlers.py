from telebot import types

from ..keyboards.reply import main_reply_keyboard

from loader import loader as l

def handler_stop_command(message: types.Message):
    try:
        text = message.text
        chat_id = message.chat.id

        if text == "Отменить":

            l.bot.clear_step_handler_by_chat_id(chat_id)
            l.bot.send_message(chat_id, "Отменено", reply_markup=types.ReplyKeyboardRemove())
            l.bot.send_message(chat_id, "Меню", reply_markup=main_reply_keyboard)
            return True

    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)
