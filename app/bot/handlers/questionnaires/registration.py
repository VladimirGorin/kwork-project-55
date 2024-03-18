from telebot import types

from bot.states import registration_state
from script.utils.db.models import UserModel

from ..messages import handler_stop_command

from loader import loader as l
from script.utils.user import UserBrowse

control = UserBrowse()

def ask_phone_number(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text

        if handler_stop_command(message):
            return

        registration_state.set_state(chat_id, "phone_number", text)
        l.bot.send_message(chat_id, "Теперь, отправьте пароль от аккаунта")

        l.bot.register_next_step_handler_by_chat_id(chat_id, ask_password)

    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)

def ask_password(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        user_controller = l.cr.database.user_controller

        if handler_stop_command(message):
            return

        registration_state.set_state(chat_id, "password", text)

        registration_password = registration_state.get_state(chat_id, "password")
        registration_phone_number = registration_state.get_state(chat_id, "phone_number")

        if not (registration_password and registration_phone_number):
            raise ValueError("Не удалось получить пароль и номер телефона из состояния")

        user_controller.update_user('''UPDATE users SET password = ?, phone_number = ? WHERE chat_id = ?;''', (
            registration_password, registration_phone_number, chat_id,))

        l.bot.send_message(chat_id, "Данные записаны. Пробуем зайти в аккаунт", reply_markup=types.ReplyKeyboardRemove())
        l.bot.send_message(chat_id, "Пожалуйста, подождите")

        UserBrowse.control = l.cr.get_user(chat_id)
        UserBrowse.control.create_user(registration_phone_number, registration_password)

        if UserBrowse.control.login_status:
            l.bot.clear_step_handler_by_chat_id(chat_id)
            l.bot.register_next_step_handler_by_chat_id(chat_id, ask_code)


    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)


def ask_code(message: types.Message):
    try:
        chat_id = message.chat.id
        text = message.text
        user_controller = l.cr.database.user_controller

        l.bot.send_message(chat_id, "Код получен, пробуем вставить")
        l.bot.send_message(chat_id, "Подождите")

        UserBrowse.control.set_code(text)

        if UserBrowse.control.login_status:
            user_controller.update_user('''UPDATE users SET session_file = ?, is_auth = ? WHERE chat_id = ?;''', (f"./assets/sessions/{chat_id}", True, chat_id,))

    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)
