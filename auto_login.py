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
    browser.add_cookie({"name": "MUSIC_U", "value": "0065A2B6AFE0EE6C4135CB7DBE3C7A776AFCD8181E76C5393952C3BE7533C872B0B529283B32EFF02202771D7B1677AFA442D2365AA7FE3A23854462DF8A5F1250D941EECCD0F6DD825AC97C37E84A7CD1B2C972DFA6C4301D532F0CFF146ECBD1E80BF7DBCA7F92A2AEE4098A27AC09D3492104F5FDC59EC89AA28301BF4088EBE1C49E794E0AADE1599F8BE436B27E74AD4ECEB305BA01F09A1FDB7836641016FA51D373CB3E2EE325CFF50656F29E11A95DC484AB83A9DD5B85F76C7EAD955950989FC26A924043C129D44527AB540C1F5C64645F6D8497745BF5F693AB591C14B3E7556C5EC880C981A51D638AB2656993CFE88DB4750F97C9FFC754F5E5897CDCAF2BC351E1EBA608AF7AFE38E3D2470335AC84BE8FA9AE394A2355FC9F39F02E1CF26F30D66CFC9067D0FD2ECB8142C31DCF5BAEB115F780120B21C0AF8A18C017D4A13BB540404FA7CA0D0F36D0"})
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
