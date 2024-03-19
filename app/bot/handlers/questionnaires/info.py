from telebot import types

from ...utils.stop_handlers import handler_stop_command
from ...keyboards.reply import main_reply_keyboard

from script.utils.db.models.info import InfoModel

from loader import loader as l

import re


# 1, 7, 10-00 17-00, 5000

def check_input(text):
    params = text.split(', ')

    try:
        param_1 = int(params[0])
    except ValueError:
        return False

    try:
        param_2 = int(params[1])
        if param_2 < 0 or param_2 > 7:
            return False
    except ValueError:
        return False

    time_pattern = re.compile(r'^\d{2}-\d{2}$')
    if not time_pattern.match(params[2]) or not time_pattern.match(params[3]):
        return False

    try:
        param_5 = int(params[4])
    except ValueError:
        return False

    return params


def ask_info(message: types.Message):
    try:

        chat_id = message.chat.id
        text = message.text

        if handler_stop_command(message):
            return

        replaced_text = check_input(text)

        if not replaced_text:
            l.bot.send_message(
                chat_id, "Данные указаны не верно, попробуйте опять.")
            l.bot.register_next_step_handler_by_chat_id(chat_id, ask_info)
            return

        info_controller = l.cr.database.info_controller
        info = InfoModel(owner_id=chat_id, place=replaced_text[0], max_price=replaced_text[4],
                         max_days=replaced_text[1], from_time=replaced_text[2], to_time=replaced_text[3])


        info_controller.update_user_info(
            '''UPDATE users_info SET place = ?, max_price = ?, max_days = ?, from_time = ?, to_time = ? WHERE owner_id = ?;''',
            (info.place, info.max_price, info.max_days, info.from_time, info.to_time, info.owner_id,))

        l.bot.send_message(chat_id, "Информация успешно обновлена",
                           reply_markup=main_reply_keyboard)

    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)
