from telebot import types
from ..keyboards.inline import auth_inline_keyboard
from ..keyboards.reply import stop_reply_keyboard

from script.utils.db.models import UserModel

from loader import loader as l


def setup_messages_handlers():
    @l.bot.message_handler(["start"])
    def handler_start_command(message: types.Message) -> None:
        try:
            chat_id = message.chat.id

            user = UserModel(chat_id)
            user_controller = l.cr.database.user_controller

            get_user_status = user_controller.get_user_status(chat_id)

            not_auth_message = "Привет, это бот для битвы за место\nНажми на кнопку что бы авторизоватся"

            if not get_user_status:
                user_controller.add_user(user)

                l.bot.send_message(chat_id, not_auth_message,
                                   reply_markup=auth_inline_keyboard)
            else:
                is_auth = user_controller.get_user(
                    "SELECT is_auth FROM users WHERE chat_id = ?", (chat_id,))[0]

                if is_auth:
                    l.bot.send_message(chat_id, "Меню")
                else:
                    l.bot.send_message(
                        chat_id, not_auth_message, reply_markup=auth_inline_keyboard)

        except Exception as e:
            l.cr.info_message(f"Ошибка! {e}", chat_id)

    # @l.bot.message_handler(func=lambda message: True)
    # def handler_text_messages(message: types.Message):
    #     try:
    #         text = message.text
    #         chat_id = message.chat.id

    #         if text == "Отменить":
    #             l.bot.clear_step_handler_by_chat_id(chat_id)
    #             l.bot.send_message(chat_id, "Отменено")

    #     except Exception as e:
    #         l.cr.info_message(f"Ошибка! {e}", chat_id)

def handler_stop_command(message: types.Message):
    try:
        text = message.text
        chat_id = message.chat.id

        if text == "Отменить":

            l.bot.clear_step_handler_by_chat_id(chat_id)
            l.bot.send_message(chat_id, "Отменено", reply_markup=types.ReplyKeyboardRemove())

            return True

    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)
