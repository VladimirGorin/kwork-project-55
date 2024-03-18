from .models.user import UserController
from .models.ads import AdsController
from .models.info import InfoController

import sqlite3

class Database:

    def __init__(self, info_log,  error_log):
        self.info_log = info_log
        self.error_log = error_log

    def disconnect(self):
        try:
            if self.connection:
                self.connection.close()

                self.info_log("Отключились от базы данных")
        except sqlite3.ProgrammingError:
            pass

    def create_models_controllers(self):
        self.user_controller = UserController(self.connection, self.cursor)

    def connect(self):
        try:
            self.connection = sqlite3.connect("./assets/data/farpost.db", check_same_thread=False)

            self.cursor = self.connection.cursor()

            self.info_log("Успешно подключились к базе данных")

        except Exception as e:
            self.error_log(
                f"Ошибка при попытке подключения к базе данных: {e}")

    def initialize_database(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    chat_id VARCHAR(225) NULL,
                                    session_file VARCHAR(225) NULL,
                                    is_auth BOOLEAN DEFAULT false,
                                    phone_number VARCHAR(225) NULL,
                                    password VARCHAR(225) NULL)''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users_info (
                                        id INTEGER PRIMARY KEY,
                                        owner_id VARCHAR(225) NOT NULL,
                                        place INTEGER DEFAULT 5,
                                        max_price VARCHAR(225) DEFAULT '5000',
                                        max_days VARCHAR(225) DEFAULT '7',
                                        from_time VARCHAR(225) DEFAULT '10:00',
                                        to_time VARCHAR(225) DEFAULT '17:00'
                                )''')


            self.cursor.execute('''CREATE TABLE IF NOT EXISTS ads (
                                        id INTEGER PRIMARY KEY,
                                        owner_id VARCHAR(225) NOT NULL,
                                        link VARCHAR(225) NOT NULL,
                                        status INTEGER DEFAULT 0
                                    )''')



            self.connection.commit()

            self.info_log("Таблицы успешно созданы")

            return True

        except Exception as e:
            self.error_log(
                f"Ошибка при попытке создания таблицы: {e}")
