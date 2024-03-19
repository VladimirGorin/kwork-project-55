from telebot import types

from ...utils.stop_handlers import handler_stop_command
from ...keyboards.reply import main_reply_keyboard

from script.utils.db.models.ads import AdsModel

from loader import loader as l

from script.utils.config import get


def ask_link(message: types.Message):
    try:
        one_more_ads = True if get("TELEGRAM_BOT", "ONE_MORE_ADS") == "True" else False

        chat_id = message.chat.id
        text = message.text

        ads_controller = l.cr.database.ads_controller
        ads = AdsModel(owner_id=chat_id, link=text)

        user_ads = ads_controller.get_ads_status(chat_id)

        if handler_stop_command(message):
            return

        if not "https://" in text:
            l.bot.send_message(chat_id, "Не корректный ввод, введите ссылку.")
            l.bot.register_next_step_handler_by_chat_id(chat_id, ask_link)
            return

        if not one_more_ads:
            if user_ads:
                l.bot.send_message(chat_id, "У вас уже есть объявление", reply_markup=main_reply_keyboard)
                return

        ads_controller.add_ads(ads)
        l.bot.send_message(chat_id, "Добавлено новое объявление", reply_markup=main_reply_keyboard)


    except Exception as e:
        l.cr.info_message(f"Ошибка! {e}", chat_id)
