import time

from helpers.actions import *
from helpers.popups import *
from helpers.home import go_home
from helpers.waiters import wait_category_loaded

from locators.home import *
from locators.lastOrders_lastItems import *
from locators.plp import *
from locators.header import *


def validate_navigation_by_auth_state(driver, logged: bool):
    """
    Fluxos públicos (reutilizável para logado/deslogado):
    - scroll em seções
    - navegar categorias
    - busca
    - últimos pedidos e últimos itens
    """
    # scroll seções
    for xp in HOME_SECTIONS:
        scroll_to(driver, xp)

    # categorias
    for categoria in ["Promoções"]:
        click(driver, CATEGORY_MENU(categoria), timeout=10)
        visible(driver, SEARCH_INPUT, timeout=10)

    # busca
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "peixe")
    click(driver, SEARCH_BUTTON, timeout=10)
    visible(driver, SEARCH_INPUT, timeout=10)

    # últimos pedidos
    go_home(driver)
    click(driver, LAST_ORDERS, timeout=10)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, timeout=20)
        try_close_hotjar(driver)
        click(driver, EMPTY_GRID_ORDERS, timeout=10)
    else:
        visible(driver, USERNAME_INPUT, timeout=10)
        click(driver, LOGIN_MENU, timeout=5)  # fecha modal

    # últimos produtos comprados
    click(driver, LAST_ITEMS, timeout=10)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, timeout=20)
        click(driver, EMPTY_GRID_ORDERS, timeout=10)
    else:
        visible(driver, USERNAME_INPUT, timeout=10)
        click(driver, LOGIN_MENU, timeout=5)  # fecha modal


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def validate_navigation_by_auth_state_mobile(driver, logged: bool):
    """
    Fluxos públicos (reutilizável para logado/deslogado):
    - scroll em seções
    - navegar categorias
    - busca
    - últimos pedidos e últimos itens
    """
    # scroll seções
    for xp in HOME_SECTIONS:
        scroll_to(driver, xp)

    # categorias
    for categoria in ["promocoes"]:
        safe_click_loc_retry(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
        time.sleep(2)
        safe_click_loc_retry(driver, MOBILE_MENU_PARENT_NEXT(categoria), timeout=10, retries=4, sleep_between=0.25)
        time.sleep(2)
        safe_click_loc_retry(driver, MOBILE_MENU_SEE_ALL, retries=4, sleep_between=0.25)
        try:
            wait_category_loaded(WebDriverWait(driver, 12), driver)
        except TimeoutException:
            pass

    # busca
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "peixe")
    visible(driver, SEE_ALL_LINK, timeout=10)
    click(driver, MOBILE_SEARCH_BUTTON, timeout=10)
    visible(driver, SEARCH_INPUT, timeout=10)
    time.sleep(5)

    # últimos pedidos
    safe_click_loc_retry(driver, LOGO, 10, 4, 0.25)
    click(driver, LAST_ORDERS, timeout=10)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, timeout=20)
        try_close_hotjar(driver)
        click(driver, EMPTY_GRID_ORDERS, timeout=10)
    else:
        visible(driver, MOBILE_LOGIN_DROPDOWN_OPENED, timeout=10)
        click(driver, LOGIN_MENU, timeout=5)  # fecha modal

    # últimos produtos comprados
    click(driver, LAST_ITEMS, timeout=10)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, timeout=20)
        click(driver, EMPTY_GRID_ORDERS, timeout=10)
    else:
        visible(driver, MOBILE_LOGIN_DROPDOWN_OPENED, timeout=10)
        click(driver, LOGIN_MENU, timeout=5)  # fecha modal