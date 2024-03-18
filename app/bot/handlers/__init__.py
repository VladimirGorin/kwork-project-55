from .messages import setup_messages_handlers
from .callback_query import setup_query_handlers
from loader import loader

def setup_handlers(e_bot, e_cr):
    loader.bot = e_bot
    loader.cr = e_cr

    setup_messages_handlers()
    setup_query_handlers()
