from .messages import setup_messages_handlers
from .callback_query import setup_query_handlers
from loader import loader as l

def setup_ads():
    try:
        ads_controller = l.cr.database.ads_controller

        all_ads = ads_controller.get_ads('''SELECT DISTINCT owner_id FROM ads''', (), fetchmethod="all")

        ads_controller.update_ads('''UPDATE ads SET status = ?;''', ("0",))

        for ad in all_ads:
            owner_id = ad[0]

            l.bot.send_message(chat_id=owner_id, text="Бот был перезагружен! Просим вас заново запустить ваши объявления. Спасибо")

    except Exception as e:
        l.cr.info_log(f"Ошибка при попытке указания! {e}")


def setup_handlers(e_bot, e_cr):
    l.bot = e_bot
    l.cr = e_cr

    setup_messages_handlers()
    setup_query_handlers()
    setup_ads()
