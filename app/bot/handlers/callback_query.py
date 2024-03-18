from .questionnaires.registration import ask_phone_number
from ..keyboards.reply import stop_reply_keyboard

from loader import loader as l

def setup_query_handlers():
    @l.bot.callback_query_handler(func=lambda query: True)
    def callback_query(query):
        chat_id = query.message.chat.id

        if query.data == "new_auth":
            l.bot.send_message(chat_id, "Введите номер телефона", reply_markup=stop_reply_keyboard)
            l.bot.register_next_step_handler_by_chat_id(chat_id, ask_phone_number)
