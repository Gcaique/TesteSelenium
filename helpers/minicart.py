from selenium.webdriver.support import expected_conditions as EC

from helpers.waiters import wait, visible
from helpers.actions import click

from locators.common import (
    MINICART_WRAPPER
)

from locators.cart import (
    MINICART_ACTIVE,
    MINICART_ICON,
    MINICART_LOADING_1,
    MINICART_LOADING_2,
)

from locators.cart import VIEWCART


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
