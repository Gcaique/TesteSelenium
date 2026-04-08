import time
from helpers.actions import click, safe_click_loc_retry, mobile_click_strict
from helpers.waiters import _effective_timeout

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.header import *


def open_user_dropdown(driver, wait=None, timeout=None):
    """Abre dropdown do usuário"""
    click(driver, LOGIN_NAME_CONTAINER, timeout=timeout, wait=wait)
    time.sleep(1)


def open_dropdown_item(driver, locator, timeout=None, wait=None):
    """Abre item específico do dropdown"""
    open_user_dropdown(driver, wait=wait, timeout=timeout)
    click(driver, locator, timeout=timeout, wait=wait)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def mobile_open_login_dropdown(driver, timeout=None, wait=None):
    t = _effective_timeout(wait, timeout)
    w = wait if wait is not None else WebDriverWait(driver, t)
    w.until(EC.element_to_be_clickable(LOGIN_MENU)).click()

def mobile_open_login_modal_from_dropdown(driver, timeout=None, wait=None):
    """Mobile: clicar em 'Faça seu login' abre dropdown.
    Para abrir a modal de login precisa clicar em 'Acesso'. """
    t = _effective_timeout(wait, timeout)
    w = wait if wait is not None else WebDriverWait(driver, t)
    mobile_open_login_dropdown(driver, timeout=t, wait=wait)
    w.until(EC.element_to_be_clickable(MOBILE_LOGIN_ACESSO)).click()

def mobile_open_quero_ser_cliente_from_dropdown(driver, timeout=None, wait=None):
    t = _effective_timeout(wait, timeout)
    w = wait if wait is not None else WebDriverWait(driver, t)
    mobile_open_login_dropdown(driver, timeout=t, wait=wait)
    w.until(EC.element_to_be_clickable(MOBILE_QUERO_SER_CLIENTE)).click()

def open_user_dropdown_mobile(driver, wait=None, timeout=None):
    """Abre dropdown do usuário"""
    t = _effective_timeout(wait, timeout)
    time.sleep(1.5)
    mobile_click_strict(driver, LOGIN_NAME_CONTAINER, timeout=t, retries=4, sleep_between=0.25, wait=wait)
    time.sleep(1.5)

def open_dropdown_item_mobile(driver, locator, timeout=None, wait=None):
    """Abre item específico do dropdown"""
    t = _effective_timeout(wait, timeout)
    open_user_dropdown_mobile(driver, wait=wait, timeout=t)
    mobile_click_strict(driver, locator, timeout=t, retries=4, sleep_between=0.25, wait=wait)

def validate_user_dropdown_mobile(driver, wait):
    """
    Valida os links do dropdown do usuario no mobile.
    """

    # Minha conta
    open_dropdown_item_mobile(driver, MOBILE_DD_MINHA_CONTA, wait=wait)
    wait.until(lambda d: "/customer/account/" in d.current_url)
    time.sleep(2)

    # Comparar produtos
    open_dropdown_item_mobile(driver, MOBILE_DD_COMPARAR, wait=wait)
    wait.until(lambda d: "/catalog/product_compare/" in d.current_url)
    time.sleep(2)

    # Meus pedidos
    open_dropdown_item_mobile(driver, MOBILE_DD_MEUS_PEDIDOS, wait=wait)
    wait.until(lambda d: "/sales/order/history/" in d.current_url)
    time.sleep(2)

    # Lista de favoritos
    open_dropdown_item_mobile(driver, MOBILE_DD_FAVORITOS, wait=wait)
    wait.until(lambda d: "/wishlist/" in d.current_url)
    time.sleep(2)

    # Meus pontos
    open_dropdown_item_mobile(driver, MOBILE_DD_MEUS_PONTOS, wait=wait)
    wait.until(lambda d: "/reward/customer/info/" in d.current_url)
    time.sleep(2)

    # Meus cupons
    open_dropdown_item_mobile(driver, MOBILE_DD_MEUS_CUPONS, wait=wait)
    wait.until(lambda d: "/mycoupons/customer/coupons/" in d.current_url)
    time.sleep(2)

    # Minhas missões
    open_dropdown_item_mobile(driver, MOBILE_DD_MINHAS_MISSOES, wait=wait)
    wait.until(lambda d: "/rewardquests/customer/missions/" in d.current_url)
    time.sleep(2)

    # Privacidade e dados
    open_dropdown_item_mobile(driver, MOBILE_DD_PRIVACIDADE_DADOS, wait=wait)
    wait.until(lambda d: "/consent/customer/" in d.current_url)
    time.sleep(2)

