import time
from helpers.actions import click, safe_click_loc_retry, mobile_click_strict

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.header import *


def open_user_dropdown(driver):
    """Abre dropdown do usuário"""
    click(driver, LOGIN_NAME_CONTAINER, timeout=10)
    time.sleep(1)


def open_dropdown_item(driver, locator, timeout=10):
    """Abre item específico do dropdown"""
    open_user_dropdown(driver)
    click(driver, locator, timeout=timeout)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def mobile_open_login_dropdown(driver, timeout=10):
    w = WebDriverWait(driver, timeout)
    w.until(EC.element_to_be_clickable(LOGIN_MENU)).click()

def mobile_open_login_modal_from_dropdown(driver, timeout=12):
    """Mobile: clicar em 'Faça seu login' abre dropdown.
    Para abrir a modal de login precisa clicar em 'Acesso'. """
    w = WebDriverWait(driver, timeout)
    mobile_open_login_dropdown(driver, timeout=timeout)
    w.until(EC.element_to_be_clickable(MOBILE_LOGIN_ACESSO)).click()

def mobile_open_quero_ser_cliente_from_dropdown(driver, timeout=12):
    w = WebDriverWait(driver, timeout)
    mobile_open_login_dropdown(driver, timeout=timeout)
    w.until(EC.element_to_be_clickable(MOBILE_QUERO_SER_CLIENTE)).click()

def open_user_dropdown_mobile(driver):
    """Abre dropdown do usuário"""
    time.sleep(1.5)
    mobile_click_strict(driver, LOGIN_NAME_CONTAINER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1.5)

def open_dropdown_item_mobile(driver, locator, timeout=10):
    """Abre item específico do dropdown"""
    open_user_dropdown_mobile(driver)
    mobile_click_strict(driver, locator, timeout=10, retries=4, sleep_between=0.25)