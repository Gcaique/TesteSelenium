import pytest
from locators.plp import *
from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *
from helpers.checkout import *

VALID_USER = "hub.teste2-bruno-popup@minervafoods.com"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.checkout
@pytest.mark.fluxo_completo
def test_8_finalizacao_pedidos_completo(driver, setup_site, wait):

    print("1 - LOGIN")
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # =====================================================
    # 2 - FLUXO PIX
    # =====================================================

    print("2 - Acessando categoria Bovinos Premium")
    click_when_clickable(wait, CATEGORY_MENU("Bovinos Premium"))
    wait_category_loaded(wait, driver)

    print("3 - Adicionando produto ao carrinho")
    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    print("4 - Indo para checkout")
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    print("5 - Continuando shipping")
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)
    wait.until(EC.invisibility_of_element_located(CHECKOUT_LOADING))

    print("6 - Alterando endereço")
    alterar_endereco_checkout(driver, wait)

    print("7 - Aplicando cupom QA10")
    aplicar_cupom(driver, wait, "AUTOMACAO10")

    print("8 - Finalizando via PIX")
    finalizar_pix(driver, wait, copiar_codigo=True)

    print("9 - Retornando para Home")
    click_when_clickable(wait, LOGO)

    # =====================================================
    # 10 - FLUXO BOLETO
    # =====================================================

    print("10 - Acessando categoria Bovinos")
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    print("11 - Adicionando produto")
    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    print("12 - Indo para checkout")
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    print("13 - Continuando shipping")
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)
    wait.until(EC.invisibility_of_element_located(CHECKOUT_LOADING))

    print("14 - Alterando endereço")
    alterar_endereco_checkout(driver, wait)

    print("15 - Finalizando via Boleto")
    finalizar_boleto(driver, wait)

    print("16 - Retornando para Home")
    click_when_clickable(wait, LOGO)

    # =====================================================
    # 17 - FLUXO CARTÃO (ERRO + FALLBACK)
    # =====================================================

    print("17 - Acessando categoria Cordeiros")
    click_when_clickable(wait, CATEGORY_MENU("Cordeiros"))
    wait_category_loaded(wait, driver)

    print("18 - Adicionando produto")
    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    print("19 - Indo para checkout")
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    print("20 - Continuando shipping")
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)
    wait.until(EC.invisibility_of_element_located(CHECKOUT_LOADING))

    print("21 - Alterando endereço")
    alterar_endereco_checkout(driver, wait)

    print("22 - Finalizando Cartão (erro esperado + fallback)")
    finalizar_cartao_com_fallback_pix(driver, wait)

    print("23 - Retornando para Home")
    click_when_clickable(wait, LOGO)

    print("24 - AUTOMACAO FINALIZADA COM SUCESSO")