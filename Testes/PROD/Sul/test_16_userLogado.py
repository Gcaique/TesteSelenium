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
from helpers.credentials import get_creds

from locators.header import SEARCH_INPUT, SEE_ALL_LINK, SEARCH_SUGGEST_ADD_2
from locators.home import CAROUSEL_1, QTY_INPUT_FIRST, ADD_BTN_FIRST_CAROUSEL
from locators.plp import (
    PAGINA_2, FILTER_CONSERVACAO_OPEN, FILTER_CONSERVACAO_RESFRIADO,
    FILTER_MARCA_OPEN, FILTER_MARCA_OPT1, FILTER_CLEAR_ALL,
    SORTER_SELECT, SORT_LOW_TO_HIGH, SORT_HIGH_TO_LOW,
    CATEGORY_PROMOCOES, CATEGORY_BOVINOS, CATEGORY_MAIS_VENDIDOS, PLP_ADD_TO_CART_BY_INDEX
)
from locators.pdp import (
    FIRST_PRODUCT_PLP, PDP_INCREMENT, PDP_ADD_TO_CART,
    ADDRESSES_SELECT, ADDRESSES_OPT2, BTN_VERIFY_FORECAST, FORECAST_RESULT
)
from locators.cart import VIEWCART, EMPTY_CART_BTN, EMPTY_CART_CONFIRM, VER_CATALOGO, MINICART_ICON, MINICART_ACTIVE, MINICART_CLOSE
from locators.header import (
    DD_MINHA_CONTA, DD_COMPARAR, DD_MEUS_PEDIDOS,
    DD_FAVORITOS, DD_MEUS_PONTOS, DD_MEUS_CUPONS, DD_MINHAS_MISSOES, DD_PRIVACIDADE_DADOS
)


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("SMOKETESTING")


@pytest.mark.regressao
@pytest.mark.sul
@pytest.mark.logado
def test_16_user_logado_sul(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    ensure_logged_in(driver, VALID_USER, VALID_PASS)

    # 2) Dropdown do usuário (seus itens)
    open_dropdown_item(driver, DD_MINHA_CONTA, wait=wait)
    time.sleep(3)
    open_dropdown_item(driver, DD_COMPARAR, wait=wait)
    open_dropdown_item(driver, DD_MEUS_PEDIDOS, wait=wait)
    open_dropdown_item(driver, DD_FAVORITOS, wait=wait)
    time.sleep(3)
    open_dropdown_item(driver, DD_MEUS_PONTOS, wait=wait)
    open_dropdown_item(driver, DD_MEUS_CUPONS, wait=wait)
    open_dropdown_item(driver, DD_MINHAS_MISSOES, wait=wait)
    time.sleep(2)
    open_dropdown_item(driver, DD_PRIVACIDADE_DADOS, wait=wait)
    time.sleep(2)

    # 3) Troca de região: sul -> default -> sul
    switch_region(driver, "default")
    switch_region(driver, "sul")

    # 4) Mini-cart abre/fecha
    click(driver, MINICART_ICON, wait=wait)
    visible(driver, MINICART_ACTIVE, wait=wait)
    click(driver, MINICART_CLOSE, wait=wait)
    visible(driver, MINICART_ICON, wait=wait)

    # 5) Carrossel 1: tenta alterar qtd e adicionar
    scroll_into_view(driver, CAROUSEL_1, wait=wait)
    click(driver, QTY_INPUT_FIRST, wait=wait)
    fill(driver, QTY_INPUT_FIRST, "0")
    scroll_into_view(driver, ADD_BTN_FIRST_CAROUSEL, wait=wait)
    click(driver, ADD_BTN_FIRST_CAROUSEL, wait=wait)
    wait_minicart_loading(driver)

    # 6) Busca: "alcatra" e add pela sugestão da busca
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "alcatra")
    visible(driver, SEARCH_SUGGEST_ADD_2, wait=wait)
    click(driver, SEARCH_SUGGEST_ADD_2, wait=wait)
    wait_minicart_loading(driver)

    # 7) Busca: pack -> carne -> ver todos
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "pack")
    visible(driver, SEE_ALL_LINK, wait=wait)

    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "carne")
    visible(driver, SEE_ALL_LINK, wait=wait)
    click(driver, SEE_ALL_LINK, wait=wait)

    # 8) Paginação e filtros / ordenação
    click(driver, PAGINA_2, wait=wait)
    visible(driver, SORTER_SELECT, wait=wait)

    click(driver, FILTER_CONSERVACAO_OPEN, wait=wait)
    click(driver, FILTER_CONSERVACAO_RESFRIADO, wait=wait)
    visible(driver, SORTER_SELECT, wait=wait)

    # filtro marca (se existir)
    if driver.find_elements(*FILTER_MARCA_OPEN):
        click(driver, FILTER_MARCA_OPEN, wait=wait)
        if driver.find_elements(*FILTER_MARCA_OPT1):
            click(driver, FILTER_MARCA_OPT1, wait=wait)

    # limpar filtros
    click(driver, FILTER_CLEAR_ALL, wait=wait)

    # ordenação (low -> high -> high -> low)
    click(driver, SORTER_SELECT, wait=wait)
    click(driver, SORT_LOW_TO_HIGH, wait=wait)
    click(driver, SORTER_SELECT, wait=wait)
    click(driver, SORT_HIGH_TO_LOW, wait=wait)

    # 9) Add primeiro da lista
    click(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait)
    wait_minicart_loading(driver)

    # 10) Promoções: adicionar item
    click(driver, CATEGORY_PROMOCOES, wait=wait)
    visible(driver, SORTER_SELECT, wait=wait)

    click(driver, QTY_INPUT_FIRST, wait=wait)
    fill(driver, QTY_INPUT_FIRST, "2")
    click(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait)
    wait_minicart_loading(driver)

    # 11) Bovinos -> PDP -> add -> previsão entrega
    click(driver, CATEGORY_BOVINOS, wait=wait)
    visible(driver, FIRST_PRODUCT_PLP, wait=wait)
    click(driver, FIRST_PRODUCT_PLP, wait=wait)

    visible(driver, PDP_ADD_TO_CART, wait=wait)
    click(driver, PDP_INCREMENT, wait=wait)
    click(driver, PDP_ADD_TO_CART, wait=wait)
    wait_minicart_loading(driver)

    # previsão entrega
    click(driver, ADDRESSES_SELECT, wait=wait)
    click(driver, ADDRESSES_OPT2, wait=wait)
    click(driver, BTN_VERIFY_FORECAST, wait=wait)
    visible(driver, FORECAST_RESULT, wait=wait)

    # 12) Mais vendidos -> Avise-me (PLP / PDP)
    click(driver, CATEGORY_MAIS_VENDIDOS, wait=wait)
    visible(driver, SORTER_SELECT, wait=wait)

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

    # 13) Limpar carrinho (view cart -> empty -> confirm -> ver catálogo)
    wait_minicart_ready(driver)
    click(driver, VIEWCART, wait=wait)
    visible(driver, EMPTY_CART_BTN, wait=wait)
    click(driver, EMPTY_CART_BTN, wait=wait)
    visible(driver, EMPTY_CART_CONFIRM, wait=wait)
    click(driver, EMPTY_CART_CONFIRM, wait=wait)
    visible(driver, VER_CATALOGO, wait=wait)
    click(driver, VER_CATALOGO, wait=wait)

    # assert final: ainda logado
    assert minicart_visible(driver), "Era para terminar o teste logado, mas mini-cart não está visível."
