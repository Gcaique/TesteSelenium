import pytest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import click_if_present

from helpers.waiters import visible, clickable
from helpers.actions import click, fill, scroll_into_view, safe_click_loc_retry, mobile_click_strict
from helpers.auth import ensure_logged_in_mobile
from helpers.dropdown import open_dropdown_item_mobile
from helpers.region import switch_region_mobile
from helpers.minicart import wait_minicart_loading, wait_minicart_ready, minicart_visible
from helpers.avise_me import open_pdp_from_first_avise_in_plp, toggle_avise_me_requires_refresh_mobile
from helpers.plp import open_filter_panel_mobile

from locators.header import SEARCH_INPUT, SEE_ALL_LINK, MOBILE_SEARCH_SUGGEST_ADD_1
from locators.home import CAROUSEL_1, QTY_INPUT_FIRST, ADD_BTN_FIRST_CAROUSEL
from locators.plp import *
from locators.pdp import (FIRST_PRODUCT_PLP, PDP_INCREMENT, PDP_ADD_TO_CART, ADDRESSES_SELECT, ADDRESSES_OPT2, BTN_VERIFY_FORECAST, FORECAST_RESULT)
from locators.cart import VIEWCART, EMPTY_CART_BTN, EMPTY_CART_CONFIRM, VER_CATALOGO, MINICART_ICON, MINICART_ACTIVE, MINICART_CLOSE, SUMARY_EXPAND, SUMARY_EXPAND_ARROW
from locators.header import (DD_MINHA_CONTA, DD_COMPARAR, DD_MEUS_PEDIDOS, DD_FAVORITOS, DD_MEUS_PONTOS, DD_MEUS_CUPONS, DD_MINHAS_MISSOES)
from locators.dashboard import BTN_MAIN_ADDRESS_DASHBOARD, BTN_FILTER, REWARD_FILTER_SELECT, COUPON_VER_MAIS_1, MISSIONS_READY
from locators.common import COOKIE_ACCEPT
from locators.productCompare import INPUT_COMPARE

# =========================
# Credenciais
# =========================
VALID_USER = "caique.oliveira3@infobase.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.logado
@pytest.mark.mobile
def test_3_userLogadoMobile(driver, setup_site, wait):
    """
    Usuário LOGADO (default):
    - login
    - navega itens do dropdown do usuário
    - troca região (default <-> sul)
    - abre/fecha minicart
    - interações de compra/busca/categoria/pdp/filtros/ordenacao
    - avise-me (PLP e PDP, com refresh obrigatório)
    - limpa carrinho
    """

    visible(driver, SEARCH_INPUT, timeout=20)

    # 1) Login (fonte da verdade = mini-cart)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)

    # 2) Dropdown do usuário (seus itens)
    open_dropdown_item_mobile(driver, DD_MINHA_CONTA, timeout=15)
    visible(driver, BTN_MAIN_ADDRESS_DASHBOARD, timeout=25)
    open_dropdown_item_mobile(driver, DD_COMPARAR, timeout=15)
    visible(driver, INPUT_COMPARE, timeout=25)
    open_dropdown_item_mobile(driver, DD_MEUS_PEDIDOS, timeout=15)
    visible(driver, BTN_FILTER, timeout=25)
    open_dropdown_item_mobile(driver, DD_FAVORITOS, timeout=15)
    time.sleep(5)
    open_dropdown_item_mobile(driver, DD_MEUS_PONTOS, timeout=15)
    visible(driver, REWARD_FILTER_SELECT, timeout=25)
    open_dropdown_item_mobile(driver, DD_MEUS_CUPONS, timeout=15)
    visible(driver, COUPON_VER_MAIS_1, timeout=25)
    open_dropdown_item_mobile(driver, DD_MINHAS_MISSOES, timeout=15)
    visible(driver, MISSIONS_READY, timeout=25)

    # 3) Troca de região: default -> sul -> default
    switch_region_mobile(driver, "sul")
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    switch_region_mobile(driver, "default")

    # 4) Mini-cart abre/fecha
    mobile_click_strict(driver, MINICART_ICON, timeout=20, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, MINICART_CLOSE, timeout=20, retries=4, sleep_between=0.25)

    # 5) Carrossel 1: tenta alterar qtd e adicionar
    scroll_into_view(driver, CAROUSEL_1, timeout=15)
    click(driver, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "2")
    scroll_into_view(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    click(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    wait_minicart_loading(driver)

    # 6) Busca: "suino" e add pela sugestão da busca
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "suino")
    visible(driver, MOBILE_SEARCH_SUGGEST_ADD_1, timeout=20)
    click(driver, MOBILE_SEARCH_SUGGEST_ADD_1, timeout=10)
    wait_minicart_loading(driver)

    # 7) Busca: pack -> carne -> ver todos
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "pack")
    visible(driver, SEE_ALL_LINK, timeout=20)

    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "carne")
    visible(driver, SEE_ALL_LINK, timeout=20)
    click(driver, SEE_ALL_LINK, timeout=10)

    # paginação e filtros / ordenação
    mobile_click_strict(driver, PAGINA_2, timeout=20, retries=4, sleep_between=0.25)
    time.sleep(5)
    visible(driver, MOBILE_FILTER_OPEN_PANEL, timeout=10)

    open_filter_panel_mobile(driver, timeout=20, retries=4)
    mobile_click_strict(driver, MOBILE_FILTER_CONSERVACAO_OPEN, timeout=20, retries=4)
    visible(driver, MOBILE_FILTER_CONSERVACAO_RESFRIADO, timeout=20)
    mobile_click_strict(driver, MOBILE_FILTER_CONSERVACAO_RESFRIADO, timeout=20, retries=4)

    # limpar filtros
    visible(driver, FILTER_CLEAR_ALL, timeout=20)
    mobile_click_strict(driver, FILTER_CLEAR_ALL, timeout=15, retries=4, sleep_between=0.25)

    # ordenação (low -> high -> high -> low)
    mobile_click_strict(driver, SORTER_SELECT, 10, 4, 0.25)
    mobile_click_strict(driver, SORT_LOW_TO_HIGH, 10, 4, 0.25)
    time.sleep(5)
    mobile_click_strict(driver, SORTER_SELECT, 10, 4, 0.25)
    mobile_click_strict(driver, SORT_HIGH_TO_LOW, 10, 4, 0.25)
    time.sleep(5)

    # add primeiro da lista
    mobile_click_strict(driver, (By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]"), 10, 4, 0.25)
    wait_minicart_loading(driver)

    # 8) Promoções: adicionar item
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, timeout=20)

    mobile_click_strict(driver,(By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]"), timeout=20, retries=4, sleep_between=0.25)
    wait_minicart_loading(driver)

    # 9) Pescados -> PDP -> add -> previsão entrega
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("pescados"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, timeout=15)
    visible(driver, FIRST_PRODUCT_PLP, timeout=20)
    mobile_click_strict(driver, FIRST_PRODUCT_PLP, 15, 4, 0.25)

    visible(driver, PDP_ADD_TO_CART, timeout=20)
    scroll_into_view(driver, PDP_ADD_TO_CART,timeout=10)
    safe_click_loc_retry(driver, PDP_INCREMENT, 10, 4, 0.25)
    click(driver, PDP_ADD_TO_CART, timeout=10)
    wait_minicart_loading(driver)

    # previsão entrega
    scroll_into_view(driver, ADDRESSES_SELECT, timeout=10)
    click(driver, ADDRESSES_SELECT, timeout=10)
    click(driver, ADDRESSES_OPT2, timeout=10)
    click(driver, BTN_VERIFY_FORECAST, timeout=10)
    visible(driver, FORECAST_RESULT, timeout=20)
    scroll_into_view(driver, FORECAST_RESULT, timeout=10)

    # 10) Cordeiros -> página 2
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("cordeiros"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, timeout=15)

    mobile_click_strict(driver, PAGINA_2, timeout=15, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, timeout=20)

    # PLP: toggle avise-me
    ok_plp = toggle_avise_me_requires_refresh_mobile(driver, page_ready_locator=SORTER_SELECT)
    if not ok_plp:
        print("[WARN] PLP: não achei Avise-me para testar.")

    # PDP: abrir PDP do primeiro produto que tenha avise-me e repetir o teste
    if open_pdp_from_first_avise_in_plp(driver):
        ok_pdp = toggle_avise_me_requires_refresh_mobile(driver, page_ready_locator=None, wait_click_class=True)
        if not ok_pdp:
            print("[WARN] PDP: não consegui alternar Avise-me.")
    else:
        print("[WARN] Não consegui abrir PDP a partir de um produto com Avise-me.")

    # 12) Limpar carrinho (view cart -> empty -> confirm -> ver catálogo)
    wait_minicart_ready(driver, timeout=25)
    mobile_click_strict(driver, MINICART_ICON, 10, 4, 0.25)
    visible(driver, MINICART_ACTIVE, timeout=10)
    mobile_click_strict(driver, VIEWCART, 15, 4, 0.25)
    visible(driver, SUMARY_EXPAND, timeout=25)
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, 20, 4, 0.25)
    mobile_click_strict(driver, EMPTY_CART_BTN, 20, 4, 0.25)
    visible(driver, EMPTY_CART_CONFIRM, timeout=20)
    mobile_click_strict(driver, EMPTY_CART_CONFIRM, 20, 4, 0.25)
    visible(driver, VER_CATALOGO, timeout=25)
    mobile_click_strict(driver, VER_CATALOGO, 20, 4, 0.25)

    # assert final: ainda logado
    assert minicart_visible(driver), "Era para terminar o teste logado, mas mini-cart não está visível."
