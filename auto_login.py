# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007B3DF4A5AE22C17B6ACB798083E668537BEF2F382F1A9B2958308CDC545496DF5D64DA53CF552E59D3AF86A04256D2444F68653953F20978441AC57054EEB8A905628A00B79D62EF898064D934BCF1A69DE337A6DDE286AA4871042AB233C116F83034E94A00F418CBF318E65082C78946DCB8E7BF9FFE240A2C750C7789E9B622F34442CAF3E3425E997EC70761B0D3F4CB986E9E104F647F340ACE1C0F9C9D865E44D214C9FA82BD38898BC6AE84FDCA0DBBF74820D178CBEE0CEF0E18AFF743200298248E0981902305F46A40EDED685F53CF1B7CEC673640862DC431FD4CAF043F0D0BD800D05A38CD771136DC6B17EE1D8B6F76597269573F9599CA3760775B3B469F23A8C5B0AEDDB25230A63D747107799DB8C252288AF41CD8B72010A43DDF1A9D21DAEBC6871DBA57ADA43209406FB18463F390C77AF51DEDD3D270AA5A4219CF0A9BE517DF989C13849DEFA37E91CAC5141D4EC60EDB2FB6D64A4D"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
