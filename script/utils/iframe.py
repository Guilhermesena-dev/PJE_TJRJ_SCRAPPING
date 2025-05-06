import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException


def switch_to_iframe_containing_element(driver, by, value, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return
    except Exception:
        pass
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for index, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
            return
        except Exception:
            driver.switch_to.default_content()
    raise Exception(f"Elemento com {by}='{value}' não foi encontrado em nenhum iframe")     
