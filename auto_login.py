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
    browser.add_cookie({"name": "MUSIC_U", "value": "008ABB77E2B66683CDA9963304192DC80C1B649474C8E632FAC4DDAFF0D1B71AC84BCD49BB994D1880F07210C0BEEAB30485854E9C0C9284144849CADB9B954FE4A94BCE4F18B17DB4A22A3C7B95BA7ED86205E860F13244257BD69E89BCE2B290D3DDF13C49B9F993DA77721411F66A6776B02764F9DDC79B092E297867BEAF9DB99A6C16196121CE4344D6638E580B503C963FB679C923BC01E627054ABA23C3D7ABB263514490717B29F47936F230DF714215F60015E155EEDE1D3D69CDFAADB95D63DE4F2B9050E95B4E5B0C570E616CC42AD62398420FF3E6B81B9DECDB753639BCA962DCB4AC17BF1A3FACE07D1AA9888DC41CB3521214B4C7E39CBE8588952A03C0C0765745FD15D6DCDA9722640D0962645B68F779CC15920FFA9FF15B026C7EAC05F4B5289C65B1257B32D0132EEA2CA90761812B39F93571F94182EB4B1588AEC998686B9D519FE7200F4D4C"})
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
