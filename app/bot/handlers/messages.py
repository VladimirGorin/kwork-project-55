from telebot import types
from ..keyboards.inline import auth_inline_keyboard
from ..keyboards.reply import main_reply_keyboard

from .questionnaires.ads import ask_link
from .questionnaires.info import ask_info

from ..keyboards.reply import stop_reply_keyboard

from script.utils.db.models.user import UserModel
from script.utils.db.models.ads import AdsModel
from script.utils.db.models.info import InfoModel

from ..utils.get_user_info import get
from ..utils.control import generate_keyabord, generate_text

from loader import loader as l


def setup_messages_handlers():
    @l.bot.message_handler(["start"])
    def handler_start_command(message: types.Message) -> None:
        try:

            chat_id = message.chat.id

            user = UserModel(chat_id)
            user_info = InfoModel(chat_id)

            user_controller = l.cr.database.user_controller
            info_controller = l.cr.database.info_controller

            get_user_status = user_controller.get_user_status(chat_id)
            get_user_info_status = info_controller.get_user_info_status(chat_id)

            not_auth_message = "Привет, это бот для битвы за место\nНажми на кнопку что бы авторизоватся"

            if not get_user_info_status:
                info_controller.add_user_info(user_info)


            if not get_user_status:
                user_controller.add_user(user)

                l.bot.send_message(chat_id, not_auth_message,
                                   reply_markup=auth_inline_keyboard)
            else:
                is_auth = user_controller.get_user(
                    "SELECT is_auth FROM users WHERE chat_id = ?", (chat_id,))[0]

                if is_auth:
                    l.bot.send_message(chat_id, "Меню", reply_markup=main_reply_keyboard)
                else:
                    l.bot.send_message(
                        chat_id, not_auth_message, reply_markup=auth_inline_keyboard)

        except Exception as e:
            l.cr.info_message(f"Ошибка! {e}", chat_id)

    @l.bot.message_handler(func=lambda message: True)
    def handler_text_messages(message: types.Message):
        try:
            text = message.text
            chat_id = message.chat.id

            user_info = InfoModel(chat_id)

            info_controller = l.cr.database.info_controller
            ads_controller = l.cr.database.ads_controller

            if text == "Информация":
                info_str = get(user_info, ads_controller, info_controller)

                if not info_str:
                    l.bot.send_message(chat_id, "Ошибка! При попытке получения информации с базы данных.")
                    return

                l.bot.send_message(chat_id, info_str)

            elif text == "Добавить объяв.":
                l.bot.send_message(chat_id, "Введите ссылку на объявление", reply_markup=stop_reply_keyboard)
                l.bot.register_next_step_handler_by_chat_id(chat_id, ask_link)

            elif text == "Изминить настройки":
                l.bot.send_message(chat_id, "Введите данные через запятую в таком формате :\n\nМесто (1) , Дни (7), Время (10-00, 17-00), Цена (5000)\n\nИтог:\n1, 7, 10-00, 17-00, 5000", reply_markup=stop_reply_keyboard)
                l.bot.register_next_step_handler_by_chat_id(chat_id, ask_info)

            elif text == "Контроль":
                get_ads = ads_controller.get_ads('''SELECT id, link FROM ads WHERE owner_id = ?;''', (chat_id,), fetchmethod="all")
                ads_inline_keyboard = generate_keyabord(get_ads)
                ads_text = generate_text(get_ads)

                l.bot.send_message(chat_id, f"Выберете объявление:\n\n{ads_text}", reply_markup=ads_inline_keyboard)

        except Exception as e:
            l.cr.info_message(f"Ошибка! {e}", chat_id)
