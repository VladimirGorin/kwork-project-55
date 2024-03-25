from .user import User, UserBrowse

from loader import loader as l

from threading import Thread
from datetime import datetime

import time, pytz

moscow_tz = pytz.timezone('Europe/Moscow')

class RunAd(Thread):
    def __init__(self, thread_id, name, owner_id, ad_link) -> None:
        try:
            Thread.__init__(self)
            self.thread_id = thread_id
            self.name = name

            self.ad_link = ad_link[0]
            self.owner_id = owner_id

            self.database = l.cr.database
            self.bot = l.bot
            self.ads_controller = l.cr.database.ads_controller
            self.user_controller = l.cr.database.user_controller
            self.info_controller = l.cr.database.info_controller

            self.send_screenshot = l.cr.send_screenshot

            self.he_sleep = False

            self.control = self.get_user(owner_id)

        except Exception as e:
            self.error_message(message=f"Произошла глобальная ошибка: {e}")

    def error_message(self, message, chat_id = None):
        self.ads_controller.update_ads('''UPDATE ads SET status = ? WHERE owner_id = ? AND id = ? ;''', ("2", self.owner_id, self.thread_id,))
        self.bot.send_message(self.owner_id, f"({self.thread_id} объяв.) Ошибка! {message}")

    def info_message(self, message, chat_id = None):
        self.bot.send_message(self.owner_id, f"({self.thread_id} объяв.) {message}")


    def get_user(self, chat_id: str):
        user = User(Database=self.database, chat_id=chat_id,
                    info_message=self.info_message, error_message=self.error_message, send_screenshot=self.send_screenshot)

        return user

    def check_status(self):
        ad_status = str(self.ads_controller.get_ads('''SELECT status FROM ads WHERE owner_id = ? AND id = ?;''', (self.owner_id, self.thread_id,))[0])

        if ad_status == "2" or ad_status == "0":
            # Error
            raise Exception("Выключаем объяв. так как вы дали команду.")

        return True

    def get_user_info(self):
        try:

            user_info = self.info_controller.get_user_info(
                    '''SELECT place, max_price, max_days, from_time, to_time FROM users_info WHERE owner_id = ?''', (self.owner_id,))

            if not user_info or None in user_info:
                raise Exception("User is none")

            return user_info

        except Exception as e:
            raise Exception(f"Не удалось получить информацию о пользователе: {e}")

    def run(self):
        try:
            while True:

                user_info = self.get_user_info()

                try:
                    current_time = datetime.now(moscow_tz).time()
                    week_day = datetime.now(moscow_tz).weekday() + 1

                    user_info_max_days = int(user_info[2])
                    user_info_from_time = user_info[3]
                    user_info_to_time = user_info[4]

                    user_info_from_time = datetime.strptime(user_info_from_time, "%H-%M").time()
                    user_info_to_time = datetime.strptime(user_info_to_time, "%H-%M").time()

                except Exception as e:
                    raise Exception(f"Не удалось получить данные о пользователе: {e}")

                self.check_status()

                if user_info_from_time <= current_time <= user_info_to_time:

                    if user_info_max_days >= week_day:
                        if self.he_sleep:
                            self.info_message(f"Запускаем процесс! Время по мск: {current_time}, Дата: {week_day}")
                            self.he_sleep = False

                        login_stauts = self.control.auth()

                        if not login_stauts:
                            self.user_controller.update_user('''UPDATE users SET is_auth = ? WHERE chat_id = ?;''', (False, self.owner_id,))
                            return

                        launch_ad_status = self.control.launch_ad(self.ad_link, self.get_user_info, self.check_status)

                        if not launch_ad_status:
                            return

                    elif week_day > user_info_max_days:
                        if not self.he_sleep:
                            self.info_message(f"Не запускаем процесс. Так как дата не находится в заданом деопозоне. Ограничение по дням: {user_info_max_days} Сегодня: {week_day}")
                            self.he_sleep = True

                else:
                    if not self.he_sleep:
                        self.info_message(f"Не запускаем процесс. Так как время не находится в заданом деопозоне времени. Cейчас по мск:{current_time}")
                        self.he_sleep = True

                time.sleep(60)

        except Exception as e:
            self.error_message(message=f"Произошла ошибка в методе run: {e}")
