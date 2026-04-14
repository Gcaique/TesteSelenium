import os
import time

import pytest
from selenium.webdriver.common.keys import Keys

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT
from locators.checkout import *
from locators.pdp import ADDRESSES_SELECT

from helpers.plp import *
from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *


# =========================
# Credenciais
# =========================
VALID_USER = "smoketesting@automatizacao.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.regressao
@pytest.mark.sul
@pytest.mark.cart
@pytest.mark.mobile
def test_20_minicart_carrinho_mobile_sul(driver, setup_site, wait):
    # 1) Login
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Categoria Bovinos + adicionar item ao carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, wait=wait)

    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    wait_minicart_loading(driver)

    # 3) Favoritar + remoção do favorito pelo Mini-cart
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)  # abre minicart
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)
    time.sleep(1)
    wishlist_toggle_add_towishlist(driver, wait, index=1)

    time.sleep(2)  # Tempo para conferencia

    wishlist_toggle_remove_onwishlist(driver, wait, 1)

    time.sleep(2)  # Tempo para conferencia

    # 4) Incrementar 2x
    minicart_increment_qty(driver, wait)
    minicart_increment_qty(driver, wait)

    # 5) Decrementar
    minicart_decrement_qty(driver, wait)

    # 6) Remover (confirmar)
    if driver.find_elements(*MINICART_ITEMS):
        items = driver.find_elements(*MINICART_ITEMS)

        if len(items) > 0:
            try:
                minicart_empty_mobile(driver, wait)
            except TimeoutException:
                pytest.fail("Timeout ao tentar esvaziar minicart")
    wait.until(EC.visibility_of_element_located(MINICART_EMPTY))

    # 7) Ver produtos
    click_when_clickable(wait, MINICART_EMPTY_VIEW_PRODUCTS)

    # 8) Categoria Marcas + ordenação por menor valor + adicionar item no carrinho + Conferencia de produto adicionado no mini-cart
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT("marcas"), wait=wait, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, wait=wait)

    mobile_click_strict(driver, SORTER_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, SORT_LOW_TO_HIGH, wait=wait, retries=4, sleep_between=0.25)
    WebDriverWait(driver, 20).until(EC.url_contains("product_list_order=low_to_high"))
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    wait_minicart_loading(driver)

    #  Mini-cart abre/fecha
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25) # abre
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)

    time.sleep(2)  # Tempo para conferencia

    mobile_click_strict(driver, MOBILE_MINICART_CLOSE, wait=wait, retries=4, sleep_between=0.25) # fecha
    time.sleep(2)

    # 9) Categoria Bovinos + adicionar itens no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, SORTER_SELECT, wait=wait)

    # Produto 1 (2x incremento)
    mobile_click_strict(driver, PLP_INCREMENT_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, PLP_INCREMENT_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(4)

    # Produto 2
    mobile_click_strict(driver, PLP_INCREMENT_BY_INDEX(2), wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(2), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(4)

    # Produto 3 (3x incremento)
    mobile_click_strict(driver, PLP_INCREMENT_BY_INDEX(3), wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, PLP_INCREMENT_BY_INDEX(3), wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, PLP_INCREMENT_BY_INDEX(3), wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(3), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(4)

    # Produto 4 + conferencia de produtos adicionados
    mobile_click_strict(driver, PLP_ADD_TO_CART_BY_INDEX(4), wait=wait, retries=4, sleep_between=0.25)
    wait_minicart_loading(driver)

    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)
    time.sleep(3)  # Tempo para conferencia

    # 10) Acessando PDP do item pelo mini-cart
    safe_click_loc(driver, wait, MINICART_ITEMS_BY_INDEX(1))
    wait.until(EC.visibility_of_element_located(ADDRESSES_SELECT))
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)
    safe_click_loc(driver, wait, MINICART_ITEMS_BY_INDEX(2))
    time.sleep(2)
    wait.until(EC.visibility_of_element_located(ADDRESSES_SELECT))

    # 11) Finalizar Compra via MiniCart
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    time.sleep(8)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 12) Voltar Home + abrir mini-cart + acessar pagina do carrinho
    click_when_clickable(wait, LOGO)
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)
    click_when_clickable(wait, VIEWCART)
    wait.until(EC.url_contains("/checkout/cart"))

    #13 Alterar qty pelo o botão "+" e "-"
    wait.until(EC.presence_of_all_elements_located(SUMARY_EXPAND))
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2) # respiro para ocultar o resumo do pedido
    mobile_click_strict(driver, CART_INCREMENT_BTN(3), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(3)
    wait.until(EC.presence_of_all_elements_located(SUMARY_EXPAND))
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)  # respiro para ocultar o resumo do pedido
    wait.until(EC.presence_of_all_elements_located(CART_DECREMENT_BTN(3)))
    mobile_click_strict(driver, CART_DECREMENT_BTN(3), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(3)
    wait.until(EC.presence_of_all_elements_located(SUMARY_EXPAND))
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)  # respiro para ocultar o resumo do pedido

    # 14) Remover segundo item manualmente
    wait.until(EC.presence_of_all_elements_located(CART_REMOVE_PRODUCT_BTN))
    btn = driver.find_elements(*CART_REMOVE_PRODUCT_BTN)[1]
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(5)
    wait.until(EC.presence_of_all_elements_located(SUMARY_EXPAND))
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)  # respiro para ocultar o resumo do pedido

    # 15) Finalizar compra pelo carrinho
    wait.until(EC.presence_of_all_elements_located(CART_PROCEED_CHECKOUT))
    btn_checkout = driver.find_element(*CART_PROCEED_CHECKOUT)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_checkout)
    driver.execute_script("arguments[0].click();", btn_checkout)

    wait.until(EC.presence_of_all_elements_located(BTN_CONTINUAR_SHIPPING))

    # 16) Voltar direto para o carrinho
    driver.get(os.getenv("URL_SUL") + "checkout/cart/")
    wait.until(EC.url_contains("/checkout/cart"))

    # 17) Limpar carrinho
    mobile_click_strict(driver, SUMARY_EXPAND_ARROW, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)  # respiro para ocultar o resumo do pedido
    click_when_clickable(wait, EMPTY_CART_BTN)
    click_when_clickable(wait, MC_MODAL_ACCEPT)

    wait.until(EC.visibility_of_element_located(CART_EMPTY_MESSAGE))