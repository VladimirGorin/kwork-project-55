
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from script.utils.temp import Temp as t
from script.utils.paths import Paths as path

from bot.keyboards.reply import main_reply_keyboard

import os, time


class User:
    def __init__(self, Database, chat_id: str, info_log, info_message, send_screenshot) -> None:
        self.database_cursor = Database.cursor
        self.database_connection = Database.connection

        self.info_log = info_log
        self.info_message = info_message
        self.send_screenshot = send_screenshot

        self.chat_id = chat_id

        self.login_status = None

        self.browser = self.create_browser()

    def create_browser(self):

        chrome_options = Options()
        chrome_options.add_argument("disable-gpu")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")

        full_path = os.path.abspath(f"assets/sessions/{self.chat_id}")
        chrome_options.add_argument(f"user-data-dir={full_path}")

        browser = webdriver.Chrome(options=chrome_options)
        return browser

    def quit(self):
        self.browser.quit()

    def create_user(self, phone_number: str, password: str):
        try:
            self.browser.get(f"https://www.farpost.ru/sign")
            time.sleep(t.sleep)

            self.browser.find_element(
                By.ID, path.LOGIN_INPUT_ID).send_keys(phone_number)
            input_password = self.browser.find_element(
                By.ID, path.PASSWORD_INPUT_ID)

            input_password.send_keys(password)
            time.sleep(2)
            input_password.send_keys(Keys.ENTER)
            time.sleep(t.sleep)

            login_url = self.browser.current_url

            self.login_status = True

            if "login_by_password=1" in login_url:
                self.login_status = False
                raise Exception("данные не верны или не указаны")

            redirected_url = self.browser.current_url.split("?")
            temp_sms_url = f"{redirected_url[0]}/sms?{redirected_url[1]}"

            self.browser.get(temp_sms_url)
            time.sleep(t.sleep)

            self.browser.find_element(
                By.XPATH, "//button[@type='submit']").click()
            time.sleep(t.sleep)

            self.info_message(
                message="Авторизация прошла успешна, теперь введите код", chat_id=self.chat_id)

        except NoSuchElementException as e:
            self.info_message(
                message=f"Ошибка! При попытке создания юзера (Капча?): Элемент не найден", chat_id=self.chat_id)

            self.send_screenshot(self.browser, self.chat_id)

            self.login_status = False
            self.browser.quit()

        except Exception as e:
            self.info_message(
                message=f"Ошибка! При попытке создания юзера: {e}", chat_id=self.chat_id)

            self.send_screenshot(self.browser, self.chat_id)

            self.login_status = False
            self.browser.quit()

    def set_code(self, code):
        try:

            input_code = self.browser.find_element(By.ID, path.CODE_INPUT_ID)
            input_code.send_keys(code)
            input_code.send_keys(Keys.ENTER)

            time.sleep(t.sleep)

            home_url = self.browser.current_url

            if "personal" in home_url:
                self.info_message(
                    message="Авторизация и создание сесси прошла успешно\nТеперь у вас есть доступ к функционалу!\nНачните с установки настроек", chat_id=self.chat_id, keyboard=main_reply_keyboard)
                self.browser.quit()
            else:
                raise Exception(
                    "Url не соответствует домашнему. Не удалось войти в аккаунт.")

        except Exception as e:
            self.info_message(
                message=f"Ошибка! При попытке ввода кода: {e}", chat_id=self.chat_id)
            self.send_screenshot(self.browser, self.chat_id)

            self.login_status = False

            self.browser.quit()

        # def test(self, chat_id:str, phone_number:str, password:str):

    #     new_user = ('chast_id', 'session_file', True, "phone_number", "password")

    #     self.database_cursor.execute(
    #         '''INSERT INTO users (
    #             chat_id, session_file, is_auth, phone_number, password
    #             ) VALUES (?, ?, ?, ?, ?)''', new_user)

    #     self.database_connection.commit()


class UserBrowse:
    control: User = None
