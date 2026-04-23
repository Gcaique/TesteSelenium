import time

import pytest
from locators.plp import *
from locators.pdp import FIRST_PRODUCT_PLP, PDP_ADD_TO_CART
from locators.checkout import *
from locators.home import ADD_BTN_FIRST_CAROUSEL

from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *
from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("HUB_TESTE2_BRUNO_POPUP")


@pytest.mark.pipeline
@pytest.mark.default
@pytest.mark.checkout
def test_8_finalizacao_pedidos_pipeline(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Carrossel 1: tenta alterar qtd e adicionar
    scroll_into_view(driver, ADD_BTN_FIRST_CAROUSEL, wait=wait)
    click(driver, ADD_BTN_FIRST_CAROUSEL, wait=wait)
    wait_minicart_ready(driver)

    # 3) Acessando categoria + Adicionando produto no carrinho
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    wait_minicart_loading(driver)

    # 4) Acessando PDP + adicionando item no carrinho
    click(driver, FIRST_PRODUCT_PLP, wait=wait)

    visible(driver, PDP_ADD_TO_CART, wait=wait)
    click(driver, PDP_ADD_TO_CART, wait=wait)
    wait_minicart_loading(driver)

    # 5) Busca: "suino" e add pela sugestão da busca
    click(driver, SEARCH_INPUT, wait=wait)
    fill(driver, SEARCH_INPUT, "suino")
    visible(driver, SEARCH_SUGGEST_ADD_2, wait=wait)
    click(driver, SEARCH_SUGGEST_ADD_2, wait=wait)
    wait_minicart_loading(driver)

    # 6) Acessando checkout
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    time.sleep(5)

    # 7) Acesando step de payment
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)
    time.sleep(5)

    # 8) Finalizando pedido com BOLETO
    scroll_into_view(driver, BOLETO)
    click_when_clickable(wait, BOLETO_SELECT)
    click_when_clickable(wait, BOLETO_OPTION_21)
    time.sleep(5)
    click_when_clickable(wait, BTN_FINALIZAR_COMPRA_BOLETO)
    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    click_when_clickable(wait, BTN_IR_PARA_HOME)
