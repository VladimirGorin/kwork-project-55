

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--window-size=1920,1080')

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()

browser.get("https://python.org")
print(browser.title)
