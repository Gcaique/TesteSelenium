import time
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from helpers.actions import click_when_clickable, click
from helpers.auth import expect_login_popup, expect_login_popup_mobile
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
    # Espera o carrossel aparecer
    carousel = wait.until(EC.presence_of_element_located(HOME_CAROUSEL_1))

    # Faz scroll até ele
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", carousel)
    time.sleep(1)

    # Pega o primeiro card
    card = carousel.find_element(*FIRST_PRODUCT_CARD)

    # Faz scroll até o card
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
    time.sleep(1)

    # Pega o botão wishlist dentro do card
    btn = card.find_element(*WISHLIST_BTN_INSIDE)

    # Clica com JS
    driver.execute_script("arguments[0].click();", btn)

    return True


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def header_requires_login_mobile(driver, wait, locator, label="header_action"):
    """
    Clica em uma ação do header (LAST_ORDERS, LAST_ITEMS, etc)
    e valida que o popup de login foi exibido.
    """
    # Clica na ação do header
    click_when_clickable(wait, locator)

    # Espera popup de login aparecer
    expect_login_popup_mobile(driver, wait, timeout=8)

    # Fecha o popup (clicando novamente no header)
    click_when_clickable(wait, LOGIN_MENU)

def add_favorite_from_home_first_carousel_mobile(driver, wait, timeout=25):

    carousel = wait.until(EC.presence_of_element_located(HOME_CAROUSEL_1))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", carousel)

    end = time.time() + timeout

    while time.time() < end:
        try:
            # re-encontra o carrossel
            carousel = driver.find_element(*HOME_CAROUSEL_1)

            # slide ativo (não clonado)
            active_slide = carousel.find_element(*MOBILE_HOME_CAROUSEL_ACTIVE_SLIDE)

            # card dentro do slide ativo
            card = active_slide.find_element(*MOBILE_HOME_CAROUSEL_ACTIVE_PRODUCT_CARD)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)

            # botão wishlist dentro do card
            btn = card.find_element(*MOBILE_HOME_CAROUSEL_WISHLIST_BTN)

            wait.until(lambda d: btn.is_displayed() and btn.is_enabled())

            try:
                btn.click()
            except WebDriverException:
                driver.execute_script("arguments[0].click();", btn)

            return True

        except StaleElementReferenceException:
            time.sleep(0.3)
        except Exception:
            time.sleep(0.3)

    raise TimeoutError("Não consegui clicar no botão wishlist do primeiro produto (mobile).")