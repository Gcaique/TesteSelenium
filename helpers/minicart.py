import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.waiters import wait, visible
from helpers.actions import click, safe_click_loc
from helpers.wishlist import remove_simple_delete_with_confirm, wait_minicart_remove_alert_disappear


from locators.common import (MINICART_WRAPPER)
from locators.cart import *
from locators.wishlist import *


def minicart_visible(driver) -> bool:
    """Fonte da verdade para usuário logado"""
    try:
        el = wait(driver, 1.5).until(
            EC.visibility_of_element_located(MINICART_WRAPPER)
        )
        return el.is_displayed()
    except Exception:
        return False


def wait_minicart_loading(driver):
    """Espera loading do minicart (duas variações de classe)"""
    try:
        wait(driver, 8).until(
            EC.visibility_of_element_located(MINICART_LOADING_2)
        )
    except Exception:
        pass

    try:
        wait(driver, 20).until(
            EC.invisibility_of_element_located(MINICART_LOADING_2)
        )
    except Exception:
        pass

    try:
        wait(driver, 8).until(
            EC.visibility_of_element_located(MINICART_LOADING_1)
        )
    except Exception:
        pass

    try:
        wait(driver, 20).until(
            EC.invisibility_of_element_located(MINICART_LOADING_1)
        )
    except Exception:
        pass


def wait_minicart_ready(driver, timeout=20):
    """
    Garante:
    - loading sumiu
    - minicart está aberto
    - botão 'Ver carrinho' está visível
    """
    wait_minicart_loading(driver)

    if not driver.find_elements(*MINICART_ACTIVE):
        click(driver, MINICART_ICON, timeout=10)
        visible(driver, MINICART_ACTIVE, timeout=10)

    visible(driver, VIEWCART, timeout=timeout)


def wishlist_toggle_remove_onwishlist(driver, wait, idx: int):
    '''Remoção item dos favoritos'''
    safe_click_loc(driver, wait, WISHLIST_REMOVE_ONWISHLIST_BY_INDEX(idx), timeout=15)
    time.sleep(1.2)


def wishlist_toggle_add_towishlist(driver, wait):
    '''Adicionar item nos favoritos'''
    safe_click_loc(driver, wait, WISHLIST_ADD_TOWISHLIST, timeout=15)
    time.sleep(1.2)


def remove_simple_delete_with_confirm(driver, wait, idx: int):
    '''Remove produto do minicart'''
    safe_click_loc(driver, wait, REMOVE_SIMPLE_DELETE_BY_INDEX(idx), timeout=15)
    visible(driver, CONFIRM_MODAL_ACCEPT, timeout=15)
    safe_click_loc(driver, wait, CONFIRM_MODAL_ACCEPT, timeout=15)
    time.sleep(1.0)


def wait_minicart_remove_alert_disappear(driver, wait, timeout=25):
    '''Aguarda alerta do produto removido do minicart ficar visivel e invisivel'''
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(MINICART_REMOVE_ALERT))
    WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(MINICART_REMOVE_ALERT))


def wishlist_empty_and_go_products(driver, wait):
    """
    Remove até o minicart ficar vazio e clica em "Ver produtos".
    """
    # remove 3x
    for _ in range(3):
        remove_simple_delete_with_confirm(driver, wait, 1)
        wait_minicart_remove_alert_disappear(driver, wait, timeout=25)

    visible(driver, MINICART_EMPTY, timeout=25)
    visible(driver, MINICART_EMPTY_VIEW_PRODUCTS, timeout=25)
    safe_click_loc(driver, wait, MINICART_EMPTY_VIEW_PRODUCTS, timeout=15)
    time.sleep(5)
