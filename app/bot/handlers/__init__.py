from .messages import setup_messages_handlers
from .callback_query import setup_query_handlers
from ..keyboards.reply import main_reply_keyboard
from loader import loader as l

def setup_ads():
    try:
        ads_controller = l.cr.database.ads_controller
        user_controller = l.cr.database.user_controller

        all_ads = ads_controller.get_ads('''SELECT DISTINCT owner_id FROM ads''', (), fetchmethod="all")

        ads_controller.update_ads('''UPDATE ads SET status = ?;''', ("0",))

        for ad in all_ads:
            owner_id = ad[0]

            is_auth = int(user_controller.get_user('''SELECT is_auth FROM users WHERE chat_id = ?;''', (owner_id,))[0])

            if is_auth:
                l.bot.send_message(chat_id=owner_id, text="Бот был перезагружен! Просим вас заново запустить ваши объявления. Спасибо", reply_markup=main_reply_keyboard)

    except Exception as e:
        l.cr.info_log(f"Ошибка при попытке увидомления! {e}")


def setup_handlers(e_bot, e_cr):
    l.bot = e_bot
    l.cr = e_cr

    setup_messages_handlers()
    setup_query_handlers()
    setup_ads()
