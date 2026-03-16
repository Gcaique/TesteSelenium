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
from helpers.minicart import wait_minicart_loading
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
VALID_USER = "smoketesting@automatizacao.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.logado
@pytest.mark.mobile
def test_16_user_logado_mobile_sul(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)

    # 2) Dropdown do usuário
    validate_user_dropdown_mobile(driver, wait)

    # 3) Troca de região: -> default-> sul
    switch_region_mobile(driver, "default")
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    switch_region_mobile(driver, "sul")

    # 4) Mini-cart abre/fecha
    # abre
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, timeout=20)

    # fecha
    mobile_click_strict(driver, MOBILE_MINICART_CLOSE, timeout=20, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 5) Carrossel 1: adicionar produto ao carrinho
    scroll_into_view(driver, CAROUSEL_1, timeout=15)
    click(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    time.sleep(5)

    # 6) Busca: "suino" e add pela sugestão da busca
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "contra")
    visible(driver, MOBILE_SEARCH_SUGGEST_ADD_1, timeout=20)
    click(driver, MOBILE_SEARCH_SUGGEST_ADD_1, timeout=10)
    time.sleep(5)

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

    ok = open_filter_panel_mobile(driver, timeout=20, tries=4)
    if not ok:
        raise AssertionError("Não consegui abrir o painel de filtros no mobile")
    mobile_click_strict(driver, MOBILE_FILTER_CONSERVACAO_OPEN, timeout=20, retries=4)
    visible(driver, MOBILE_FILTER_CONSERVACAO_RESFRIADO, timeout=20)
    mobile_click_strict(driver, MOBILE_FILTER_CONSERVACAO_RESFRIADO, timeout=20, retries=4)
    WebDriverWait(driver, 20).until(EC.url_contains("conservacao=Resfriado"))

    # limpar filtros
    assert clear_filters_strict(driver, wait, FILTER_CLEAR_ALL, timeout=15, retries=5), \
        "Não consegui limpar os filtros."

    # ordenação (low -> high -> high -> low)
    mobile_click_strict(driver, SORTER_SELECT, 10, 4, 0.25)
    mobile_click_strict(driver, SORT_LOW_TO_HIGH, 10, 4, 0.25)
    WebDriverWait(driver, 20).until(EC.url_contains("product_list_order=low_to_high"))
    mobile_click_strict(driver, SORTER_SELECT, 10, 4, 0.25)
    mobile_click_strict(driver, SORT_HIGH_TO_LOW, 10, 4, 0.25)
    WebDriverWait(driver, 20).until(EC.url_contains("product_list_order=high_to_low"))

    # 9) Add primeiro da lista
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(1), 10, 4, 0.25)
    time.sleep(5)

    # 10) Promoções: adicionar item
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("promocoes"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, timeout=20)

    mobile_click_strict(driver,PLP_ADD_TO_CART_BY_INDEX(1), timeout=20, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 11) Marcas -> PDP -> add -> previsão entrega
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("marcas"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, timeout=15)
    visible(driver, FIRST_PRODUCT_PLP, timeout=20)
    mobile_click_strict(driver, FIRST_PRODUCT_PLP, 15, 4, 0.25)

    visible(driver, PDP_ADD_TO_CART, timeout=20)
    scroll_into_view(driver, PDP_ADD_TO_CART,timeout=10)
    safe_click_loc_retry(driver, PDP_INCREMENT, 10, 4, 0.25)
    click(driver, PDP_ADD_TO_CART, timeout=10)
    time.sleep(5)

    # previsão entrega
    scroll_into_view(driver, ADDRESSES_SELECT, timeout=10)
    click(driver, ADDRESSES_SELECT, timeout=10)
    click(driver, ADDRESSES_OPT2, timeout=10)
    click(driver, BTN_VERIFY_FORECAST, timeout=10)
    visible(driver, FORECAST_RESULT, timeout=20)
    scroll_into_view(driver, FORECAST_RESULT, timeout=10)

    # 12) Bovinos -> Interagir com o botão do avise-me PLP e PDP
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=20, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, timeout=15)

    # PLP: toggle avise-me
    ok_plp = find_avise_me_plp_mobile(driver, page_ready_locator=SORTER_SELECT, max_pages=5)
    if not ok_plp:
        print("[WARN] PLP: não achei Avise-me para testar.")

    # Clica no Avise-me disabled
    mobile_click_strict(driver, MOBILE_AVISE_BTN_DISABLED(1), timeout=20, retries=4, sleep_between=0.25)

    # Espera AJAX: virar alert-active clicked (sem refresh ainda)
    time.sleep(3)

    # Refresh
    driver.refresh()

    # Página pronta de novo
    visible(driver, SORTER_SELECT, timeout=25)

    # Scroll no botão ativado
    el_active = scroll_to_avise(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH)
    assert el_active is not None

    # Clica no botão ativado (para desativar)
    mobile_click_strict(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH, timeout=20, retries=4, sleep_between=0.25)

    # Aguarda voltar para "disabled" (sem alert-active)
    time.sleep(4)

    # PDP: abrir PDP do primeiro produto que tenha avise-me e repetir o teste
    ok_pdp = open_pdp_from_first_avise_in_plp(driver)
    if not ok_pdp:
        print("[WARN] Não consegui abrir PDP a partir de um produto com Avise-me.")

    # Clica no Avise-me disabled
    mobile_click_strict(driver, MOBILE_AVISE_BTN_DISABLED(1), timeout=20, retries=4, sleep_between=0.25)

    # Espera AJAX: virar alert-active clicked (sem refresh ainda)
    time.sleep(3)

    # Refresh
    driver.refresh()

    # Scroll no botão ativado
    el_active = scroll_to_avise(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH)
    assert el_active is not None

    # Clica no botão ativado (para desativar)
    mobile_click_strict(driver, MOBILE_AVISE_BTN_ACTIVE_AFTER_REFRESH, timeout=20, retries=4, sleep_between=0.25)

    # Aguarda voltar para "disabled" (sem alert-active)
    time.sleep(4)

    # 13) Limpar carrinho (view cart -> empty -> confirm -> ver catálogo)
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MINICART_ACTIVE, timeout=10)
    mobile_click_strict(driver, VIEWCART, 15, 4, 0.25)
    visible(driver, SUMARY_EXPAND, timeout=25)
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, 20, 4, 0.25)
    mobile_click_strict(driver, EMPTY_CART_BTN, 20, 4, 0.25)
    visible(driver, EMPTY_CART_CONFIRM, timeout=20)
    mobile_click_strict(driver, EMPTY_CART_CONFIRM, 20, 4, 0.25)
    visible(driver, VER_CATALOGO, timeout=25)
    mobile_click_strict(driver, VER_CATALOGO, 20, 4, 0.25)

    # Final: ainda logado
    time.sleep(5)
