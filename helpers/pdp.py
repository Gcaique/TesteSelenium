import time
from selenium.webdriver.common.by import By

from helpers.wishlist import wait_favorite_status
from helpers.plp import open_product_with_avise_by_pagination, open_product_with_avise_by_pagination_mobile
from helpers.actions import safe_click_loc,mobile_click_strict
from helpers.waiters import _effective_timeout
from selenium.webdriver.support.ui import WebDriverWait

from locators.pdp import *


def add_current_pdp_product_to_favorites(driver, wait):
    """
    Clica no botão de favorito na PDP
    e valida mudança de status.
    """

    safe_click_loc(driver, wait, PDP_WISHLIST_BTN)

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


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def add_current_pdp_product_to_favorites_mobile(driver, wait):
    """
    Clica no botão de favorito na PDP
    e valida mudança de status.
    """

    btn = driver.find_element(*PDP_WISHLIST_BTN)
    before = btn.get_attribute("class")

    mobile_click_strict(driver, PDP_WISHLIST_BTN, timeout=_effective_timeout(wait, 20, default=20), retries=4, sleep_between=0.25, wait=wait)

    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(*PDP_WISHLIST_BTN).get_attribute("class") != before
    )


def open_out_of_stock_product_and_add_to_favorites_mobile(driver, wait, pages=(1,2,3,4,5,6)):
    """
    Fluxo:
      - percorre páginas
      - encontra produto com botão 'Avise-me'
      - abre PDP
      - adiciona aos favoritos
    """

    found = open_product_with_avise_by_pagination_mobile(driver, wait, pages=pages)

    assert found, "Não foi encontrado produto fora de estoque nas páginas percorridas."

    add_current_pdp_product_to_favorites_mobile(driver, wait)
