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

def login(driver, usuario, senha):
    driver.maximize_window()
    
    try:
        switch_to_iframe_containing_element(driver, By.ID, "username", timeout=10)
    except Exception:
        pass
    
    try:
        input_usuario = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "username")))
        input_usuario.clear()
        try:
            input_usuario.send_keys(usuario)
        except Exception:
            driver.execute_script("arguments[0].value = arguments[1]", input_usuario, usuario)
        print("ID username foi encontrado com sucesso.")
    except Exception as e:
        raise
    driver.switch_to.default_content() 

    try:
        switch_to_iframe_containing_element(driver, By.ID, "password", timeout=10)
    except Exception:
        pass    
    
    try:
        input_senha = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "password")))

        input_senha.clear()
        try:
            input_senha.send_keys(senha)
        except Exception:
            driver.execute_script("arguments[0].value = arguments[1]", input_senha, senha)
        print("ID da senha foi encontrado com sucesso.")
    except Exception as e:
        raise
    driver.switch_to.default_content()            
