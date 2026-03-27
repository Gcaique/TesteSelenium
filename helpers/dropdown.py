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

def validate_user_dropdown_mobile(driver, wait):
    """
    Valida os links do dropdown do usuario no mobile.
    """

    # Minha conta
    open_dropdown_item_mobile(driver, MOBILE_DD_MINHA_CONTA, timeout=15)
    wait.until(lambda d: "/customer/account/" in d.current_url)
    time.sleep(2)

    # Comparar produtos
    open_dropdown_item_mobile(driver, MOBILE_DD_COMPARAR, timeout=15)
    wait.until(lambda d: "/catalog/product_compare/" in d.current_url)
    time.sleep(2)

    # Meus pedidos
    open_dropdown_item_mobile(driver, MOBILE_DD_MEUS_PEDIDOS, timeout=15)
    wait.until(lambda d: "/sales/order/history/" in d.current_url)
    time.sleep(2)

    # Lista de favoritos
    open_dropdown_item_mobile(driver, MOBILE_DD_FAVORITOS, timeout=15)
    wait.until(lambda d: "/wishlist/" in d.current_url)
    time.sleep(2)

    # Meus pontos
    open_dropdown_item_mobile(driver, MOBILE_DD_MEUS_PONTOS, timeout=15)
    wait.until(lambda d: "/reward/customer/info/" in d.current_url)
    time.sleep(2)

    # Meus cupons
    open_dropdown_item_mobile(driver, MOBILE_DD_MEUS_CUPONS, timeout=15)
    wait.until(lambda d: "/mycoupons/customer/coupons/" in d.current_url)
    time.sleep(2)

    # Minhas missões
    open_dropdown_item_mobile(driver, MOBILE_DD_MINHAS_MISSOES, timeout=15)
    wait.until(lambda d: "/rewardquests/customer/missions/" in d.current_url)
    time.sleep(2)
