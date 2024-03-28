from telebot import types

from ..keyboards.reply import main_reply_keyboard

from loader import loader as l

def handler_stop_command(message: types.Message):
    try:
        text = message.text
        chat_id = message.chat.id

        user_controller = l.cr.database.user_controller


        is_auth = user_controller.get_user(
                "SELECT is_auth FROM users WHERE chat_id = ?", (chat_id,))[0]


        if text == "Отменить":

            if is_auth:
                l.bot.clear_step_handler_by_chat_id(chat_id)
                l.bot.send_message(chat_id, "Отменено", reply_markup=types.ReplyKeyboardRemove())
                l.bot.send_message(chat_id, "Меню", reply_markup=main_reply_keyboard)
                return True
            else:
                l.bot.clear_step_handler_by_chat_id(chat_id)
                l.bot.send_message(chat_id, "Отменено", reply_markup=types.ReplyKeyboardRemove())
                return True

    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)
