import pytest
from selenium.webdriver.common.by import By
import time

from helpers.waiters import visible
from helpers.actions import click, fill, scroll_into_view
from helpers.auth import ensure_logged_in
from helpers.dropdown import open_dropdown_item
from helpers.region import switch_region
from helpers.minicart import wait_minicart_loading, wait_minicart_ready, minicart_visible
from helpers.avise_me import open_pdp_from_first_avise_in_plp, toggle_avise_me_requires_refresh

from locators.header import SEARCH_INPUT, SEE_ALL_LINK, SEARCH_SUGGEST_ADD_2
from locators.home import CAROUSEL_1, QTY_INPUT_FIRST, ADD_BTN_FIRST_CAROUSEL
from locators.plp import (
    PAGINA_2, FILTER_CONSERVACAO_OPEN, FILTER_CONSERVACAO_RESFRIADO,
    FILTER_MARCA_OPEN, FILTER_MARCA_OPT1, FILTER_CLEAR_ALL,
    SORTER_SELECT, SORT_LOW_TO_HIGH, SORT_HIGH_TO_LOW,
    CATEGORY_PROMOCOES, CATEGORY_PESCADOS, CATEGORY_CORDEIROS,
)
from locators.pdp import (
    FIRST_PRODUCT_PLP, PDP_INCREMENT, PDP_ADD_TO_CART,
    ADDRESSES_SELECT, ADDRESSES_OPT2, BTN_VERIFY_FORECAST, FORECAST_RESULT
)
from locators.cart import VIEWCART, EMPTY_CART_BTN, EMPTY_CART_CONFIRM, VER_CATALOGO, MINICART_ICON, MINICART_ACTIVE, MINICART_CLOSE
from locators.header import (
    DD_MINHA_CONTA, DD_COMPARAR, DD_MEUS_PEDIDOS,
    DD_FAVORITOS, DD_MEUS_PONTOS, DD_MEUS_CUPONS, DD_MINHAS_MISSOES
)
from locators.dashboard import BTN_MAIN_ADDRESS_DASHBOARD, BTN_FILTER, REWARD_FILTER_SELECT, COUPON_FILTER_SELECT, MISSIONS_READY
from locators.productCompare import INPUT_COMPARE

# =========================
# Credenciais
# =========================
VALID_USER = "hub.teste2-bruno-popup@minervafoods.com"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.logado
def test_3_userLogado(driver, setup_site):
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
    ensure_logged_in(driver, VALID_USER, VALID_PASS)

    # 2) Dropdown do usuário (seus itens)
    open_dropdown_item(driver, DD_MINHA_CONTA, timeout=15)
    visible(driver, BTN_MAIN_ADDRESS_DASHBOARD, timeout=20)
    open_dropdown_item(driver, DD_COMPARAR, timeout=15)
    visible(driver, INPUT_COMPARE, timeout=15)
    open_dropdown_item(driver, DD_MEUS_PEDIDOS, timeout=15)
    visible(driver, BTN_FILTER, timeout=15)
    open_dropdown_item(driver, DD_FAVORITOS, timeout=15)
    time.sleep(5)
    open_dropdown_item(driver, DD_MEUS_PONTOS, timeout=15)
    visible(driver, REWARD_FILTER_SELECT, timeout=15)
    open_dropdown_item(driver, DD_MEUS_CUPONS, timeout=15)
    visible(driver, COUPON_FILTER_SELECT, timeout=15)
    open_dropdown_item(driver, DD_MINHAS_MISSOES, timeout=15)
    visible(driver, MISSIONS_READY, timeout=15)

    # 3) Troca de região: default -> sul -> default
    switch_region(driver, "sul")
    switch_region(driver, "default")

    # 4) Mini-cart abre/fecha
    click(driver, MINICART_ICON, timeout=10)
    visible(driver, MINICART_ACTIVE, timeout=10)
    click(driver, MINICART_CLOSE, timeout=10)
    visible(driver, MINICART_ICON, timeout=10)

    # 5) Carrossel 1: tenta alterar qtd e adicionar
    scroll_into_view(driver, CAROUSEL_1, timeout=15)
    click(driver, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "0")
    scroll_into_view(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    click(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    wait_minicart_loading(driver)

    # 6) Busca: "suino" e add pela sugestão da busca
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "suino")
    visible(driver, SEARCH_SUGGEST_ADD_2, timeout=20)
    click(driver, SEARCH_SUGGEST_ADD_2, timeout=10)
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
    click(driver, PAGINA_2, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    click(driver, FILTER_CONSERVACAO_OPEN, timeout=10)
    click(driver, FILTER_CONSERVACAO_RESFRIADO, timeout=10)
    visible(driver, SORTER_SELECT, timeout=20)

    # filtro marca (se existir)
    if driver.find_elements(*FILTER_MARCA_OPEN):
        click(driver, FILTER_MARCA_OPEN, timeout=8)
        if driver.find_elements(*FILTER_MARCA_OPT1):
            click(driver, FILTER_MARCA_OPT1, timeout=8)

    # limpar filtros
    click(driver, FILTER_CLEAR_ALL, timeout=15)

    # ordenação (low -> high -> high -> low)
    click(driver, SORTER_SELECT, timeout=10)
    click(driver, SORT_LOW_TO_HIGH, timeout=10)
    click(driver, SORTER_SELECT, timeout=10)
    click(driver, SORT_HIGH_TO_LOW, timeout=10)

    # add primeiro da lista
    click(driver, (By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]"), timeout=10)
    wait_minicart_loading(driver)

    # 8) Promoções: adicionar item
    click(driver, CATEGORY_PROMOCOES, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    click(driver, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "2")
    click(driver, (By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]"), timeout=10)
    wait_minicart_loading(driver)

    # 9) Pescados -> PDP -> add -> previsão entrega
    click(driver, CATEGORY_PESCADOS, timeout=15)
    visible(driver, FIRST_PRODUCT_PLP, timeout=20)
    click(driver, FIRST_PRODUCT_PLP, timeout=15)

    visible(driver, PDP_ADD_TO_CART, timeout=20)
    click(driver, PDP_INCREMENT, timeout=10)
    click(driver, PDP_ADD_TO_CART, timeout=10)
    wait_minicart_loading(driver)

    # previsão entrega
    click(driver, ADDRESSES_SELECT, timeout=10)
    click(driver, ADDRESSES_OPT2, timeout=10)
    click(driver, BTN_VERIFY_FORECAST, timeout=10)
    visible(driver, FORECAST_RESULT, timeout=20)

    # 10) Cordeiros -> página 2
    click(driver, CATEGORY_CORDEIROS, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    click(driver, PAGINA_2, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    # PLP: toggle avise-me
    ok_plp = toggle_avise_me_requires_refresh(driver, page_ready_locator=SORTER_SELECT)
    if not ok_plp:
        print("[WARN] PLP: não achei Avise-me para testar.")

    # PDP: abrir PDP do primeiro produto que tenha avise-me e repetir o teste
    if open_pdp_from_first_avise_in_plp(driver):
        ok_pdp = toggle_avise_me_requires_refresh(driver, page_ready_locator=None, wait_click_class=True)
        if not ok_pdp:
            print("[WARN] PDP: não consegui alternar Avise-me.")
    else:
        print("[WARN] Não consegui abrir PDP a partir de um produto com Avise-me.")

    # 12) Limpar carrinho (view cart -> empty -> confirm -> ver catálogo)
    wait_minicart_ready(driver, timeout=25)
    click(driver, VIEWCART, timeout=15)
    visible(driver, EMPTY_CART_BTN, timeout=25)
    click(driver, EMPTY_CART_BTN, timeout=20)
    visible(driver, EMPTY_CART_CONFIRM, timeout=20)
    click(driver, EMPTY_CART_CONFIRM, timeout=20)
    visible(driver, VER_CATALOGO, timeout=25)
    click(driver, VER_CATALOGO, timeout=20)

    # assert final: ainda logado
    assert minicart_visible(driver), "Era para terminar o teste logado, mas mini-cart não está visível."
