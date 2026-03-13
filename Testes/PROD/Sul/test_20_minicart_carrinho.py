import os
import time

import pytest
from selenium.webdriver.common.keys import Keys

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


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.logado
def test_7_minicart_carrinho_sul(driver, setup_site, wait):
    # 1) Login
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Categoria Bovinos + adicionar item ao carrinho
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # 3) Favoritar no MiniCart
    wishlist_toggle_add_towishlist(driver, wait, index=1)

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
                minicart_empty(driver, wait)
            except TimeoutException:
                pytest.fail("Timeout ao tentar esvaziar minicart")
    wait.until(EC.visibility_of_element_located(MINICART_EMPTY))

    # 7) Ver produtos
    click_when_clickable(wait, MINICART_EMPTY_VIEW_PRODUCTS)

    # 8) Categoria Mais Vendidos + adicionar item no carrinho
    click_when_clickable(wait, CATEGORY_MENU("Mais Vendidos"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # 9) Categoria Marcas Premium + adicionar itens no carrinho
    click_when_clickable(wait, CATEGORY_MENU("Marcas"))
    wait_category_loaded(wait, driver)
    scroll_into_view(driver, TOOLBAR_AMOUNT)

    # Produto 1 (2x incremento)
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(1))
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(1))
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # Produto 2
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(2))
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    wait_minicart_ready(driver)

    # Produto 3 (3x incremento)
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(3))
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(3))
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(3))
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(3))
    wait_minicart_ready(driver)

    # Produto 4
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(4))
    wait_minicart_ready(driver)

    # 10) Acessando PDP do item pelo mini-cart
    safe_click_loc(driver, wait, MINICART_ITEMS_BY_INDEX(1), timeout=10)
    wait.until(EC.visibility_of_element_located(ADDRESSES_SELECT))
    safe_click_loc(driver, wait, MINICART_ITEMS_BY_INDEX(2), timeout=10)
    time.sleep(2)
    wait.until(EC.visibility_of_element_located(ADDRESSES_SELECT))

    # 11) Finalizar Compra via MiniCart
    wait_minicart_ready(driver)
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 12) Voltar Home + abrir mini-cart + acessar pagina do carrinho
    click_when_clickable(wait, LOGO)
    click(driver, MINICART_ICON)
    wait_minicart_ready(driver)
    click_when_clickable(wait, VIEWCART)
    wait.until(EC.url_contains("/checkout/cart"))

    # 13) Alterar qty segundo item pelo input
    cart_qty_inputs = wait.until(
        EC.visibility_of_all_elements_located(CART_PRODUCT_QTY_INPUT)
    )
    cart_qty_inputs[1].send_keys("1")
    cart_qty_inputs[1].send_keys(Keys.RETURN)
    time.sleep(5) # respiro para o carregamento da pagina

    #14 Alterar qty pelo o botão "+" e "-"
    wait.until(EC.presence_of_all_elements_located(CART_DECREMENT_BTN(3)))
    safe_click_loc(driver, wait, CART_INCREMENT_BTN(3), timeout=30)
    time.sleep(3)
    wait.until(EC.presence_of_all_elements_located(CART_DECREMENT_BTN(3)))
    safe_click_loc(driver, wait, CART_DECREMENT_BTN(3), timeout=30)
    time.sleep(3)

    # 15) Remover segundo item manualmente
    wait.until(EC.presence_of_all_elements_located(CART_REMOVE_PRODUCT_BTN))
    btn = driver.find_elements(*CART_REMOVE_PRODUCT_BTN)[1]
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(5)

    # 16) Finalizar compra pelo carrinho
    wait.until(EC.presence_of_all_elements_located(CART_PROCEED_CHECKOUT))
    btn_checkout = driver.find_element(*CART_PROCEED_CHECKOUT)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_checkout)
    driver.execute_script("arguments[0].click();", btn_checkout)

    wait.until(EC.presence_of_all_elements_located(BTN_CONTINUAR_SHIPPING))

    # 17) Voltar direto para o carrinho
    driver.get(os.getenv("URL_SUL") + "checkout/cart/")
    wait.until(EC.url_contains("/checkout/cart"))

    # 18) Limpar carrinho
    click_when_clickable(wait, EMPTY_CART_BTN)
    click_when_clickable(wait, MC_MODAL_ACCEPT)

    wait.until(EC.visibility_of_element_located(CART_EMPTY_MESSAGE))