import time
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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


def add_favorite_from_home_first_carousel(driver, wait, timeout=25):

    # 1) Espera o carrossel existir
    carousel = wait.until(EC.presence_of_element_located(HOME_CAROUSEL_1))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", carousel)

    end = time.time() + timeout

    while time.time() < end:
        try:
            # 2) Re-encontra o carrossel (evita stale)
            carousel = driver.find_element(*HOME_CAROUSEL_1)

            # 3) Pega o primeiro card REAL
            card = carousel.find_element(*FIRST_PRODUCT_CARD)

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)

            # 4) HOVER (essencial no seu layout)
            ActionChains(driver).move_to_element(card).perform()

            time.sleep(0.5)  # pequeno tempo pro botão aparecer

            # 5) Agora busca o botão dentro do card
            btn = card.find_element(*WISHLIST_BTN_INSIDE)

            # 6) Clique seguro
            try:
                wait.until(lambda d: btn.is_displayed() and btn.is_enabled())
                btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", btn)

            return True

        except StaleElementReferenceException:
            time.sleep(0.3)

    raise TimeoutError("Não consegui clicar no botão wishlist do primeiro produto.")


