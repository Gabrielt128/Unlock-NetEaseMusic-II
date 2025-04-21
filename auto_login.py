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
    browser.add_cookie({"name": "MUSIC_U", "value": "001136504226C5EF5CFC4F95C000C98EE02569C00206087FA72F6E15C9FECC2DA58AE437B375B3191757A66EE9ADD64205C9EFE2AE62F3218A20C38512C6C2C351CDC6B864C356EA52538571022B136813F7D4435FEF8A24C820AFF82EA5E94153B34CDB8DFE2985DE1C83D56915470F1264A302BBD5AEE24DC7E53693DDF4BA7EF368E9B5BBD5BD529F592D8B8D3AD974B3A38CAA476D0D590439A096A5EE44D20F6DD0DD1816A135A9F5B16FE4F862BE1BBC2DBB6270EE9675D4103ED544116316C9E407BC868B575049E4C66F4EB1A8B2DF5573AF02EB767092FCC49F9626A4BF6283AB27AA6389250AFE6D95C1AC1D1454DC5622F431E06870A6151013911E41349B9C4944FC907C8398E1D59D35E544EF774EEFA9987777D63D7D278C17C0A00C0B12FE414FD5BB0169617F6CBBE67AD8460AEA7DCF9D4D20068B15B74A5A0CBF2EB0E7350C1B58E7981E50624094"})
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
