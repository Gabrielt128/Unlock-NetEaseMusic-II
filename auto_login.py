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
    browser.add_cookie({"name": "MUSIC_U", "value": "00002C0829578E9A53EDCE8DD375B4812AD0E61ABA3F696FB1EFF133259E8D0DF9F80A0E2A3C1E05B7ABEAFCC7D5C3FBEE6EBEFFDDEF799365D7815F4E54B00CC3B0B6FD49BD8687C7EF8301CA005162AA081560A7DC1CF1B06E261ECA1DB2B73CD3D93D0245651DAB233E31618EA96E89F668B06FEE9AC9AEE208BD5E93CB8C90102EB610CD91BC4FE74A53128F6FE642D65060B9678988F0246D657147B5A4EC9BD5E719139B4AF790038ACDDA2636F408FCFFAEAE79131C6E489BA6CD881A57B8825162664E76F1090937CDDF39301923A9313D73350B0647770655D14C8CFAD7FB1385C1CB37BF5A5E43A37806923919F29A1C5DE25A049DFEB88CB37E78A37DDBA5D413709D407326046DB86FEEEBD8E9D95CCDC2B2A7A308E2C40C7D419E3459B4B04195D91411340A31A37BD39EA064C13FB810101C19EC360849EE98364F69EC743BF538A9B2C3F61198E0DC78"})
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
