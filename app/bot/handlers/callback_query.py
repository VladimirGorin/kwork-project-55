from .questionnaires.registration import ask_phone_number
from ..keyboards.reply import stop_reply_keyboard
from ..keyboards.inline import ad_control_keyboard, auth_inline_keyboard

from telebot import types

from script.utils.user.ad import RunAd
from threading import Thread

from ..states import ads_state
from .messages import not_auth_text, start_text

from loader import loader as l


def setup_query_handlers():
    @l.bot.callback_query_handler(func=lambda query: True)
    def callback_query(query):

        try:
            chat_id = query.message.chat.id
            ads_controller = l.cr.database.ads_controller
            user_controller = l.cr.database.user_controller
            info_controller = l.cr.database.info_controller


            ad_id = ads_state.get_state(chat_id, "control_selected_ad")
            ad_status = ads_controller.get_ads(
                '''SELECT status FROM ads WHERE owner_id = ? AND id = ?;''', (chat_id, ad_id, ))

            is_auth = user_controller.get_user(
                "SELECT is_auth FROM users WHERE chat_id = ?", (chat_id,))[0]

            if not is_auth:
                l.bot.send_message(chat_id, not_auth_text,
                                   reply_markup=types.ReplyKeyboardRemove())
                l.bot.send_message(chat_id, start_text,
                                   reply_markup=auth_inline_keyboard)

                return

            callback_data = query.data

            if callback_data == "new_auth":
                l.bot.send_message(
                    chat_id, "Введите номер телефона", reply_markup=stop_reply_keyboard)
                l.bot.register_next_step_handler_by_chat_id(
                    chat_id, ask_phone_number)

            elif "control" in callback_data:
                ad_id = callback_data.split(":")[1]
                ad_link = ads_controller.get_ads(
                    '''SELECT link FROM ads WHERE owner_id = ? AND id = ?;''', (chat_id, ad_id,))

                ads_state.set_state(chat_id, "control_selected_ad", ad_id)

                l.bot.send_message(
                    chat_id, f"Объявление номер ({ad_id})\nСсылка: {ad_link[0]}\n\nЧто бы вы хотели сделать?", reply_markup=ad_control_keyboard)

            elif callback_data == "ad_on":

                if not ad_id:
                    raise Exception("Вы ещё не выбрали объявление")

                if not ad_status:
                    raise Exception("Не удалось получит текущий статус работы")

                ad_status = str(ad_status[0])

                if ad_status == "1":
                    raise Exception(
                        "Не удалось включить задачу так как она уже включена")

                ad_link = ads_controller.get_ads(
                    '''SELECT link FROM ads WHERE owner_id = ? AND id = ?;''', (chat_id, ad_id,))

                ads_controller.update_ads(
                    '''UPDATE ads SET status = ? WHERE owner_id = ? AND id = ?;''', ("1", chat_id, ad_id))

                l.bot.send_message(
                    chat_id, f"Статус для ({ad_id}) успешно изминен на ВКЛЮЧЕН\n\nВКЛЮЧЕНИЕ может занят некоторое время обычно это минута.")

                run_ad = RunAd(thread_id=int(
                    ad_id), name=f"Threading-{ad_id}", owner_id=chat_id, ad_link=ad_link)
                run_ad.start()

                ads_state.clear_state(chat_id)

            elif callback_data == "ad_off":

                if not ad_id:
                    l.bot.send_message(chat_id, "Вы ещё не выбрали объявление")
                    return

                if not ad_status:
                    raise Exception("Не удалось получит текущий статус работы")

                ad_status = str(ad_status[0])

                if ad_status == "0":
                    raise Exception(
                        "Не удалось выключить задачу так как она уже выключена")

                ads_controller.update_ads(
                    '''UPDATE ads SET status = ? WHERE owner_id = ? AND id = ?;''', ("0", chat_id, ad_id))

                l.bot.send_message(
                    chat_id, f"Статус для ({ad_id}) успешно изминен на ВЫКЛЮЧЕН\n\nВЫКЛЮЧЕНИЕ может занят некоторое время обычно это минута.")

                ads_state.clear_state(chat_id)

        except Exception as e:
            l.cr.info_message(f"Ошибка! {e}", chat_id)
