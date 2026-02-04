import time
from selenium.webdriver.common.by import By

from helpers.wishlist import wait_favorite_status
from helpers.plp import open_product_with_avise_by_pagination
from helpers.actions import safe_click_loc

from locators.pdp import *


def add_current_pdp_product_to_favorites(driver, wait):
    """
    Clica no botão de favorito na PDP
    e valida mudança de status.
    """

    safe_click_loc(driver, wait, PDP_WISHLIST_BTN, timeout=12)

    assert wait_favorite_status(driver), \
        "Não confirmou alteração de status do favorito na PDP."


def open_out_of_stock_product_and_add_to_favorites(
    driver,
    wait,
    category_locator,
    pages=(1, 2, 3, 4, 5, 6)
):
    """
    Fluxo:
      - entra na categoria
      - percorre páginas
      - encontra produto com botão 'Avise-me'
      - abre PDP
      - adiciona aos favoritos
    """

    found = open_product_with_avise_by_pagination(
        driver,
        wait,
        category_locator,
        pages=pages
    )

    assert found, "Não foi encontrado produto fora de estoque nas páginas percorridas."

    add_current_pdp_product_to_favorites(driver, wait)