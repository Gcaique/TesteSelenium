from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.actions import click_when_clickable, click, scroll_and_safe_click_loc, safe_click_loc, scroll_into_view
from helpers.auth import expect_login_popup
from helpers.wishlist import wait_favorite_status

from locators.header import LOGIN_MENU, LOGO
from locators.home import *


# Redireciona a pagina para os elementos da HOME PAGE (Carrossel / mapa de corte / footer)
def scroll_and_confirm(wait, driver, xpath: str):
    locator = (By.XPATH, xpath)
    try:
        element = wait.until(EC.visibility_of_element_located(locator))
    except TimeoutException:
        assert False, f"Elemento NÃO encontrado (ou não visível) para o XPath: {xpath}"

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    assert element.is_displayed(), f"Elemento encontrado, mas NÃO visível após scroll. XPath: {xpath}"


def header_requires_login(driver, wait, locator, label="header_action"):
    """
    Clica em uma ação do header (LAST_ORDERS, LAST_ITEMS, etc)
    e valida que o popup de login foi exibido.
    """

    # Clica na ação do header
    click_when_clickable(wait, locator)

    # Espera popup de login aparecer
    expect_login_popup(driver, wait, label=label)

    # Fecha o popup (clicando novamente no header)
    click_when_clickable(wait, LOGIN_MENU)



def go_home(driver):
    """Volta para a home clicando na logo."""
    click(driver, LOGO, timeout=10)


def add_favorite_from_home_first_carousel(driver, wait):
    scroll_into_view(driver, CAROUSEL_1, timeout=15)
    safe_click_loc(driver, wait, HOME_WISHLIST_BTN_1, timeout=12)
    assert wait_favorite_status(driver), "Não confirmou status de favorito na HOME."
