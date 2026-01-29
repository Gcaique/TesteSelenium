from helpers.actions import *
from helpers.popups import *
from helpers.home import go_home

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