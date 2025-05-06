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
from utils.iframe import switch_to_iframe_containing_element
from utils.login import login

##clica no botão de login 
def login_button(driver):
    try:
        switch_to_iframe_containing_element(driver, By.ID, "btnEntrar", timeout=10)
        botao_login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "btnEntrar")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", botao_login)
        time.sleep(2)

        if botao_login.is_enabled() and botao_login.is_displayed():
            try:
                botao_login.click()
            except Exception:
                driver.execute_script("arguments[0].click()", botao_login)
        else:
            driver.execute_script("document.getElementById('btnEntrar').click();")


        try:
            WebDriverWait(driver, 10).until(EC.staleness_of(botao_login))
        except TimeoutException:
            pass
    except Exception as e:
        print(f"Erro ao clicar no botão de login: {e}")
        raise
