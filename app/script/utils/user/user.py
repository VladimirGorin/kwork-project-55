
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from script.utils.temp import Temp as t
from script.utils.paths import Paths as path

from bot.keyboards.reply import main_reply_keyboard

from bs4 import BeautifulSoup

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import os, time, re


class User:
    def __init__(self, Database, chat_id: str, info_message, send_screenshot, error_message=None ) -> None:
        self.database_cursor = Database.cursor
        self.database_connection = Database.connection

        self.info_message = info_message
        self.error_message = error_message
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
        browser.maximize_window()
        return browser

    def quit(self):
        self.browser.quit()

    def auth(self):
        try:

            self.browser.get("https://www.farpost.ru/personal")

            time.sleep(t.sleep)

            link = self.browser.current_url

            if "sign" in link:
                raise Exception(
                    "Вы не авторизованы! Мы вынуждены сбросить вам доступ. Нажмите /start что бы авторизоватся")

            return True

        except Exception as e:
            self.error_message(
                message=f"При проверке авторизации: {e}", chat_id=self.chat_id)

            self.send_screenshot(self.browser, self.chat_id)
            self.browser.quit()

    def get_soup(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def replace_stick_price(self, url, new_value):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        query_params['stickPrice'] = [str(new_value)]

        updated_query_string = urlencode(query_params, doseq=True)

        updated_url_tuple = parsed_url._replace(query=updated_query_string)

        updated_url = urlunparse(updated_url_tuple)

        return updated_url

    def export_stick_data(self):
        time.sleep(t.sleep)

        soup = self.get_soup(self.browser.page_source)

        def get_position():
            stick_position_div_text = soup.find(
                    name="div", class_=path.STICK_POSITION_DIV_CLASS).text

            stick_position_text = int(
                    re.search(r'\d+', stick_position_div_text).group())

            return stick_position_text

        try:

            next_price = self.browser.find_element(By.CLASS_NAME, path.SPINS_UP_BUTTON_CLASS)
            stick_price = int(next_price.get_attribute("price"))

        except Exception as e:
            raise Exception(f"Не удалось получить цену за место: {e}")

        try:
            stick_position_text = get_position()
        except Exception as e:
            raise Exception(f"Не удалось получить место: {e}")


        return [stick_position_text, stick_price]

    def slick_button_click(self, where="up"):

        if where == "up":
            try:
                self.browser.find_element(By.CLASS_NAME, path.SPINS_UP_BUTTON_CLASS).click()
            except Exception as e:
                raise Exception(f"Не удалось нажать на кнопку поднять цену: {e}")

        elif where == "down":
            try:
                self.browser.find_element(By.CLASS_NAME, path.SPINS_DOWN_BUTTON_CLASS).click()
            except Exception as e:
                raise Exception(f"Не удалось нажать на кнопку понизить цену: {e}")

    def confirm_button(self):
        confirm_button = self.browser.find_element(By.XPATH, path.SPINS_CONFRIM_BUTTON_XPATH)
        confirm_button_text = confirm_button.text

        if "Сохранить" in confirm_button_text:
            confirm_button.click()
            time.sleep(t.sleep)
            current_url = self.browser.current_url

            if "service-configure" in current_url:
                raise Exception("Не удалось сохранить. Не хватает денег?")

        elif "Приклеить" in confirm_button_text:
            confirm_button.click()
            time.sleep(t.sleep)
            try:
                buy_button = self.browser.find_element(By.ID, path.SPINS_FIRST_BUY_BUTTON_ID)
                buy_button.click()
                time.sleep(t.sleep)
            except NoSuchElementException:
                raise Exception("Не удалось нажать на кнопку покупки. Не хватает баланса?")

    def launch_ad(self, ad_link, get_user_info, check_status):
        try:
            self.browser.get(ad_link)
            time.sleep(t.sleep)
            soup = self.get_soup(self.browser.page_source)
            stick_a = soup.find(name="a", class_=path.STICK_A_CLASS)
            stick_a_link = stick_a.get("href")

            if not stick_a_link:
                raise Exception("Ссылка для кнопки приклеить не найдена")

            stick_a_link = f"https://www.farpost.ru{stick_a_link}"
            self.browser.get(stick_a_link)

            time.sleep(t.sleep)

            while True:
                stick_data = self.export_stick_data()

                stick_place = stick_data[0]
                stick_price = stick_data[1]

                try:
                    user_info = get_user_info()

                    user_info_place = int(user_info[0])
                    user_info_max_price = int(user_info[1])
                except Exception as e:
                    raise Exception(f"Не удалось получить данные о пользователе: {e}")


                check_status()

                # Пропускаем если место совпадает
                if stick_place == user_info_place:
                    if user_info_max_price >= stick_price:

                        self.confirm_button()
                        return True

                    elif user_info_max_price < stick_price:
                        raise Exception(f"Цена за место {user_info_place} поднялась до {stick_price} не удалось поднять ставку так как ваш лимит {user_info_max_price}")


                # Если место меньше чем должно быть
                elif user_info_place < stick_place:

                    if user_info_max_price >= stick_price:
                        self.slick_button_click()
                        self.info_message(f"Цена за место {user_info_place} поднялась до {stick_price} поднимаем ставку так как ваш лимит {user_info_max_price}. Текущие место: {stick_place}")

                    elif user_info_max_price < stick_price:
                        raise Exception(f"Цена за место {user_info_place} поднялась до {stick_price} не удалось поднять ставку так как ваш лимит {user_info_max_price}")

                elif user_info_place > stick_place:

                    self.slick_button_click(where="down")
                    self.info_message(f"Цена за ваше место {user_info_place} уменшилась до {stick_price} опускаемся ниже. Текущие место: {stick_place}")

        except Exception as e:
            self.error_message(
                message=e, chat_id=self.chat_id)

            self.send_screenshot(self.browser, self.chat_id)
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


class UserBrowse:
    control: User = None
