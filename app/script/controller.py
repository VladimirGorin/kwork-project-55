from .utils.db.database import Database
from .utils.temp import Temp
from .utils.user import User

from selenium.webdriver import Chrome
from telebot import TeleBot, types

from .utils.config import get

from io import BytesIO
from PIL import Image

import logging


class Controller:
    def __init__(self, bot):
        self.logger = self.initialize_logger()

        self.database = None
        self.database_init()

        self.screenshots = True if get("TELEGRAM_BOT", "SCREENSHOTS") == "True" else False

        self.bot:TeleBot = bot

    def database_init(self):

        self.database = Database(
            self.info_log, self.error_log)
        self.database.connect()

        status = self.database.initialize_database()

        if status:
            self.database.create_models_controllers()

    def info_message(self, message, chat_id, keyboard = None):
        self.bot.send_message(chat_id, message, reply_markup=keyboard)

    def info_log(self, message):
        print(message)
        self.logger.info(message)

    def send_screenshot(self, browser:Chrome, chat_id):

        if self.screenshots:
            screenshot = browser.get_screenshot_as_png()
            image = Image.open(BytesIO(screenshot))

            image_stream = BytesIO()
            image.save(image_stream, format='PNG')
            image_stream.seek(0)

            self.bot.send_photo(chat_id, image_stream)

    def error_log(self, message):
        print(message)
        self.logger.error(f'[Global error] {message}')

        Temp.global_error = True

    def initialize_logger(self):
        logger = logging.getLogger("GLOBAL")
        logger.setLevel(logging.DEBUG)

        log_file = './assets/logs/main.log'
        file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def get_user(self, chat_id: str):
        user = User(Database=self.database, chat_id=chat_id, info_log=self.info_log,
                    info_message=self.info_message, send_screenshot=self.send_screenshot)

        return user
    def get_user(self, chat_id: str):
        user = User(Database=self.database, chat_id=chat_id, info_log=self.info_log,
                    info_message=self.info_message, send_screenshot=self.send_screenshot)

        return user
