from selenium import webdriver
from selenium_recaptcha import Recaptcha_Solver
driver = webdriver.Chrome()
driver.get('https://www.google.com/recaptcha/api2/demo')


solver = Recaptcha_Solver(
driver=driver, # Your Web Driver
ffmpeg_path='', # Optional. If does not exists, it will automatically download.
log=1 # If you want to view the progress.
)
solver.solve_recaptcha()
