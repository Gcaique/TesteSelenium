import time

import pytest

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT

from helpers.auth import ensure_logged_in_mobile
from helpers.wishlist import *
from helpers.home import add_favorite_from_home_first_carousel_mobile
from helpers.plp import add_favorite_from_category_first_item_mobile, search_and_add_favorite_by_index_mobile
from helpers.pdp import open_out_of_stock_product_and_add_to_favorites_mobile
from helpers.waiters import _effective_timeout

from locators.plp import *
from helpers.credentials import get_creds

# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("SMOKETESTING2")


@pytest.mark.regressao
@pytest.mark.sul
@pytest.mark.favoritos
@pytest.mark.mobile
def test_19_lista_de_favoritos_mobile_sul(driver, setup_site, wait):
    # 1) Login
    click_if_present(driver, COOKIE_ACCEPT, 20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS, wait=wait)
    assert minicart_visible(driver), "Era para estar logado, mas o minicart não apareceu."
    try_close_popups(driver)

    # 2) Favorita na Home (primeiro carrossel)
    add_favorite_from_home_first_carousel_mobile(driver, wait)

    # 3) Favorita na categoria Bovinos (primeiro item)
    add_favorite_from_category_first_item_mobile(driver, wait)

    # 4) Busca "peixe" e favorita o item 6 (igual script)
    search_and_add_favorite_by_index_mobile(driver, wait, term="peixe")

    # 5) Favorita na PDP um produto fora de estoque
    open_out_of_stock_product_and_add_to_favorites_mobile(driver, wait, pages=(1, 2, 3, 4, 5, 6))

    # 6) Abre Lista de favoritos
    open_favorites_page(driver, wait)

    # 7) Incrementa item 2
    wishlist_increment_by_index_mobile(driver, wait, 2)

    # 8) Incrementa item 3
    wishlist_increment_by_index_mobile(driver, wait, 1)
    wishlist_increment_by_index_mobile(driver, wait, 1)

    # 9) Adicionar todos ao carrinho + abrir minicart e fechar
    wishlist_add_all_to_cart_mobile(driver, wait)

    # abre
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)

    time.sleep(4)  # Tempo para conferencia de produtos adicionados

    # fecha
    mobile_click_strict(driver, MOBILE_MINICART_CLOSE, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 10) Interações no primeiro item: ++, - e adiciona + abrir minicart e fechar
    wishlist_increment_by_index_mobile(driver, wait, 3)
    wishlist_increment_by_index_mobile(driver, wait, 3)
    wishlist_decrement_by_index_mobile(driver, wait, 3)
    wishlist_add_item_to_cart_by_index_mobile(driver, wait, 3)

    # abre
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)

    time.sleep(4)  # Tempo para conferencia de produtos adicionados

    # fecha
    mobile_click_strict(driver, MOBILE_MINICART_CLOSE, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 11) Avise-me
    wishlist_avise_me_flow_mobile(driver, wait)

    # 12) Botão favorito dentro do minicart (remove produto dos favoritos pelo minicart, favorita novamente pelo minicart)
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)  # abre minicart
    time.sleep(1)
    wishlist_toggle_remove_onwishlist(driver, wait, 1)

    time.sleep(3)  # Tempo para conferencia

    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25) # abre minicart
    time.sleep(2)

    wishlist_toggle_add_towishlist(driver, wait, 1)

    time.sleep(3)  # Tempo para conferencia

    # 13) Remover itens da lista pelo o botão do card
    assert remove_all_cards_wishlist(driver, wait), "Ainda existiam itens na wishlist."

    # 14) Esvaziar minicart
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    minicart_empty(driver, wait)

    # valida que segue logado
    assert minicart_visible(driver), "Era para continuar logado ao final do fluxo."

