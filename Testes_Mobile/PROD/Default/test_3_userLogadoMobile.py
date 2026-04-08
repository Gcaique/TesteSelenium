import pytest
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import click_if_present

from helpers.waiters import visible, clickable
from helpers.actions import click, fill, scroll_into_view, safe_click_loc_retry, mobile_click_strict
from helpers.auth import ensure_logged_in_mobile
from helpers.dropdown import validate_user_dropdown_mobile
from helpers.region import switch_region_mobile
from helpers.avise_me import open_pdp_from_first_avise_in_plp, find_avise_me_plp_mobile
from helpers.plp import open_filter_panel_mobile, scroll_to_avise, clear_filters_strict

from locators.header import SEARCH_INPUT, SEE_ALL_LINK, MOBILE_SEARCH_SUGGEST_ADD_1
from locators.home import CAROUSEL_1, ADD_BTN_FIRST_CAROUSEL
from locators.plp import *
from locators.pdp import (FIRST_PRODUCT_PLP, PDP_INCREMENT, PDP_ADD_TO_CART, ADDRESSES_SELECT, ADDRESSES_OPT2, BTN_VERIFY_FORECAST, FORECAST_RESULT)
from locators.cart import *
from locators.common import COOKIE_ACCEPT



# =========================
# Credenciais
# =========================
VALID_USER = "hub.teste2-bruno-popup@minervafoods.com"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.logado
@pytest.mark.mobile
def test_3_user_logado_mobile(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)

    # 2) Dropdown do usuário
    validate_user_dropdown_mobile(driver, wait)

    # 3) Troca de região: default -> sul -> default
    switch_region_mobile(driver, "sul")
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    switch_region_mobile(driver, "default")

    # 4) Mini-cart abre/fecha
    # abre
    mobile_click_strict(driver, MOBILE_MINICART_ICON, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, wait=wait)

    # fecha
    mobile_click_strict(driver, MOBILE_MINICART_CLOSE, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_CLOSED, wait=wait)

    # 5) Carrossel 1: adicionar produto ao carrinho
    scroll_into_view(driver, CAROUSEL_1, wait=wait)
    click(driver, ADD_BTN_FIRST_CAROUSEL, wait=wait)
    time.sleep(5)

    # 6) Busca: "suino" e add pela sugestão da busca
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "suino")
    visible(driver, MOBILE_SEARCH_SUGGEST_ADD_1, wait=wait)
    click(driver, MOBILE_SEARCH_SUGGEST_ADD_1, wait=wait)
    time.sleep(5)

    # 7) Busca: pack -> carne -> ver todos
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "pack")
    visible(driver, SEE_ALL_LINK, wait=wait)

    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "carne")
    visible(driver, SEE_ALL_LINK, wait=wait)
    click(driver, SEE_ALL_LINK, wait=wait)

    # 8) Paginação e filtros / ordenação
    mobile_click_strict(driver, PAGINA_2, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    visible(driver, MOBILE_FILTER_OPEN_PANEL, wait=wait)

    ok = open_filter_panel_mobile(driver, tries=4)
    if not ok:
        raise AssertionError("Não consegui abrir o painel de filtros no mobile")
    mobile_click_strict(driver, MOBILE_FILTER_CONSERVACAO_OPEN, wait=wait, retries=4)
    visible(driver, MOBILE_FILTER_CONSERVACAO_RESFRIADO, wait=wait)
    mobile_click_strict(driver, MOBILE_FILTER_CONSERVACAO_RESFRIADO, wait=wait, retries=4)
    WebDriverWait(driver, 20).until(EC.url_contains("conservacao=Resfriado"))

    # limpar filtros
    assert clear_filters_strict(driver, wait, FILTER_CLEAR_ALL, retries=5), \
        "Não consegui limpar os filtros."

    # ordenação (low -> high -> high -> low)
    mobile_click_strict(driver, SORTER_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, SORT_LOW_TO_HIGH, wait=wait, retries=4, sleep_between=0.25)
    WebDriverWait(driver, 20).until(EC.url_contains("product_list_order=low_to_high"))
    mobile_click_strict(driver, SORTER_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, SORT_HIGH_TO_LOW, wait=wait, retries=4, sleep_between=0.25)
    WebDriverWait(driver, 20).until(EC.url_contains("product_list_order=high_to_low"))

    # 9 Add primeiro da lista
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 10) Promoções: adicionar item
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("promocoes"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, wait=wait)

    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 11) Pescados -> PDP -> add -> previsão entrega
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("pescados"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, wait=wait)
    visible(driver, FIRST_PRODUCT_PLP, wait=wait)
    mobile_click_strict(driver, FIRST_PRODUCT_PLP, wait=wait, retries=4, sleep_between=0.25)

    visible(driver, PDP_ADD_TO_CART, wait=wait)
    scroll_into_view(driver, PDP_ADD_TO_CART, wait=wait)
    safe_click_loc_retry(driver, PDP_INCREMENT, wait=wait, retries=4, sleep_between=0.25)
    click(driver, PDP_ADD_TO_CART, wait=wait)
    time.sleep(5)

    # previsão entrega
    scroll_into_view(driver, ADDRESSES_SELECT, wait=wait)
    click(driver, ADDRESSES_SELECT, wait=wait)
    click(driver, ADDRESSES_OPT2, wait=wait)
    click(driver, BTN_VERIFY_FORECAST, wait=wait)
    visible(driver, FORECAST_RESULT, wait=wait)
    scroll_into_view(driver, FORECAST_RESULT, wait=wait)

    # 12) Cordeiros -> Interagir com o botão do avise-me PLP e PDP
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("cordeiros"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, wait=wait)

    # PLP: toggle avise-me
    ok_plp = find_avise_me_plp_mobile(driver, page_ready_locator=SORTER_SELECT, max_pages=5)
    if not ok_plp:
        print("[WARN] PLP: não achei Avise-me para testar.")

    # Clica no Avise-me disabled
    mobile_click_strict(driver, MOBILE_AVISE_BTN_DISABLED(1), wait=wait, retries=4, sleep_between=0.25)

    # Espera AJAX: virar alert-active clicked (sem refresh ainda)
    time.sleep(3)

    # Refresh
    driver.refresh()

    # Página pronta de novo
    visible(driver, SORTER_SELECT, wait=wait)

    # Scroll no botão ativado
    el_active = scroll_to_avise(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH)
    assert el_active is not None

    # Clica no botão ativado (para desativar)
    mobile_click_strict(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH, wait=wait, retries=4, sleep_between=0.25)

    # Aguarda voltar para "disabled" (sem alert-active)
    time.sleep(3)

    # PDP: abrir PDP do primeiro produto que tenha avise-me e repetir o teste
    ok_pdp = open_pdp_from_first_avise_in_plp(driver)
    if not ok_pdp:
        print("[WARN] Não consegui abrir PDP a partir de um produto com Avise-me.")

    # Clica no Avise-me disabled
    mobile_click_strict(driver, MOBILE_AVISE_BTN_DISABLED(1), wait=wait, retries=4, sleep_between=0.25)

    # Espera AJAX: virar alert-active clicked (sem refresh ainda)
    time.sleep(3)

    # Refresh
    driver.refresh()

    # Scroll no botão ativado
    el_active = scroll_to_avise(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH)
    assert el_active is not None

    # Clica no botão ativado (para desativar)
    mobile_click_strict(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH, wait=wait, retries=4, sleep_between=0.25)

    # Aguarda voltar para "disabled" (sem alert-active)
    time.sleep(3)

    # 13) Limpar carrinho (view cart -> empty -> confirm -> ver catálogo)
    mobile_click_strict(driver, MOBILE_MINICART_ICON, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MINICART_ACTIVE, wait=wait)
    mobile_click_strict(driver, VIEWCART, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, SUMARY_EXPAND, wait=wait)
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, EMPTY_CART_BTN, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, EMPTY_CART_CONFIRM, wait=wait)
    mobile_click_strict(driver, EMPTY_CART_CONFIRM, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, VER_CATALOGO, wait=wait)
    mobile_click_strict(driver, VER_CATALOGO, wait=wait, retries=4, sleep_between=0.25)

    # Final: ainda logado
    time.sleep(5)
