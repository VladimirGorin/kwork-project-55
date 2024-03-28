from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

import time, os

options = Options()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")

full_path = os.path.abspath(f"5015947677")
options.add_argument(f"user-data-dir={full_path}")

# Задаем желаемый размер окна браузера
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)

# Устанавливаем максимальный размер окна
driver.maximize_window()

driver.get("https://www.farpost.ru/personal")

print(driver.title)

time.sleep(5)

driver.find_element(By.ID, "sign").send_keys("89502874915")
input_password = driver.find_element(By.ID, "password")
input_password.send_keys("h46h7xed")
time.sleep(2)
input_password.send_keys(Keys.ENTER)
time.sleep(5)
# Сохраняем скриншот
driver.save_screenshot("./screenshot.png")


driver.close()
v
#
