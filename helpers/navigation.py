import time

from helpers.actions import *
from helpers.popups import *
from helpers.home import go_home
from helpers.waiters import wait_category_loaded, _effective_timeout

from locators.home import *
from locators.lastOrders_lastItems import *
from locators.plp import *
from locators.header import *


def validate_navigation_by_auth_state(driver, logged: bool, wait=None):
    """
    Fluxos públicos (reutilizável para logado/deslogado):
    - scroll em seções
    - navegar categorias
    - busca
    - últimos pedidos e últimos itens
    """
    t = _effective_timeout(wait, None)
    # scroll seções
    for xp in HOME_SECTIONS:
        scroll_to(driver, xp)

    # categorias
    for categoria in ["Promoções"]:
        click(driver, CATEGORY_MENU(categoria), wait=wait)
        visible(driver, SEARCH_INPUT, wait=wait)

    # busca
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "peixe", wait=wait)
    click(driver, SEARCH_BUTTON, wait=wait)
    visible(driver, SEARCH_INPUT, wait=wait)

    # últimos pedidos
    go_home(driver)
    click(driver, LAST_ORDERS, wait=wait)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
        try_close_hotjar(driver)
        click(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
    else:
        visible(driver, USERNAME_INPUT, wait=wait)
        click(driver, LOGIN_MENU, timeout=_effective_timeout(wait, None), wait=wait)  # fecha modal

    # últimos produtos comprados
    click(driver, LAST_ITEMS, wait=wait)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
        click(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
    else:
        visible(driver, USERNAME_INPUT, wait=wait)
        click(driver, LOGIN_MENU, timeout=_effective_timeout(wait, None), wait=wait)  # fecha modal


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def validate_navigation_by_auth_state_mobile(driver, logged: bool, wait=None):
    """
    Fluxos públicos (reutilizável para logado/deslogado):
    - scroll em seções
    - navegar categorias
    - busca
    - últimos pedidos e últimos itens
    """
    t = _effective_timeout(wait, None)
    # scroll seções
    for xp in HOME_SECTIONS:
        scroll_to(driver, xp)

    # categorias
    for categoria in ["promocoes"]:
        safe_click_loc_retry(driver, MOBILE_MENU_HAMBURGER, timeout=_effective_timeout(wait, None), retries=4, sleep_between=0.25, wait=wait)
        time.sleep(2)
        safe_click_loc_retry(driver, MOBILE_MENU_PARENT_NEXT(categoria), timeout=_effective_timeout(wait, None), retries=4, sleep_between=0.25, wait=wait)
        time.sleep(2)
        safe_click_loc_retry(driver, MOBILE_MENU_SEE_ALL, retries=4, sleep_between=0.25, wait=wait)
        try:
            eff = _effective_timeout(wait, None)
            wait_category_loaded(wait if wait is not None else WebDriverWait(driver, eff), driver)
        except TimeoutException:
            pass

    # busca
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "peixe", wait=wait)
    visible(driver, SEE_ALL_LINK, wait=wait)
    click(driver, MOBILE_SEARCH_BUTTON, wait=wait)
    visible(driver, SEARCH_INPUT, wait=wait)
    time.sleep(5)

    # últimos pedidos
    safe_click_loc_retry(driver, LOGO, timeout=_effective_timeout(wait, None), retries=4, sleep_between=0.25, wait=wait)
    click(driver, LAST_ORDERS, wait=wait)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
        try_close_hotjar(driver)
        click(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
    else:
        visible(driver, MOBILE_LOGIN_DROPDOWN_OPENED, wait=wait)
        click(driver, LOGIN_MENU, timeout=_effective_timeout(wait, None), wait=wait)  # fecha modal

    # últimos produtos comprados
    click(driver, LAST_ITEMS, wait=wait)

    if logged:
        visible(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
        click(driver, EMPTY_GRID_ORDERS, wait=wait, timeout=t)
    else:
        visible(driver, MOBILE_LOGIN_DROPDOWN_OPENED, wait=wait)
        click(driver, LOGIN_MENU, timeout=_effective_timeout(wait, None), wait=wait)  # fecha modal
