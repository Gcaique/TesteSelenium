import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from locators.plp import SORTER_SELECT
from locators.common import MINICART_WRAPPER


def wait(driver, timeout=10, poll=0.1):
    """Cria WebDriverWait padrão com polling rápido"""
    return WebDriverWait(driver, timeout, poll_frequency=poll)


def visible(driver, locator, timeout=10):
    """Espera elemento ficar visível"""
    return wait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def clickable(driver, locator, timeout=10):
    """Espera elemento ficar clicável"""
    return wait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )


def wait_any_visible(driver, locator, timeout=20):
    """
    Espera qualquer elemento visível de um locator.
    Retorna o WebElement ou None.
    """
    end = time.time() + timeout
    while time.time() < end:
        els = driver.find_elements(*locator)
        for e in els:
            try:
                if e.is_displayed():
                    return e
            except Exception:
                pass
        time.sleep(0.2)
    return None


def wait_visible_any(driver, locators, timeout=25, poll=0.2):
    """
    Espera até QUALQUER locator da lista ficar visível.
    Retorna o WebElement encontrado.
    """
    end = time.time() + timeout
    while time.time() < end:
        for loc in locators:
            els = driver.find_elements(*loc)
            for el in els:
                try:
                    if el.is_displayed():
                        return el
                except Exception:
                    pass
        time.sleep(poll)

    raise TimeoutException(
        f"Nenhum locator ficou visível: {locators}"
    )


def try_visible(wait, locator, timeout=3) -> bool:
    driver = wait._driver
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def wait_category_loaded(wait, driver):
    # validação simples: campo de busca visível (página carregou)
    wait.until(EC.visibility_of_element_located(SORTER_SELECT))


def minicart_visible(driver) -> bool:
    # Verificar se o mini-cart é apresentado, usamos isso para verificar se o usuário está logado
    try:
        el = wait(driver, 1.5).until(EC.visibility_of_element_located(MINICART_WRAPPER))
        return el.is_displayed()
    except Exception:
        return False

def assert_logged_out(driver, context=""):
    assert not minicart_visible(driver), f"[{context}] Era para estar DESLOGADO, mas mini-cart está visível."
