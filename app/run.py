from telebot import TeleBot, types

from script.utils.config import get
from script.controller import Controller

from bot.handlers import setup_handlers

bot = TeleBot(get("TELEGRAM_BOT", "TOKEN"))
cr = Controller(bot)

setup_handlers(bot, cr)

cr.info_log("Бот запущен!")
bot.polling(none_stop=True)
