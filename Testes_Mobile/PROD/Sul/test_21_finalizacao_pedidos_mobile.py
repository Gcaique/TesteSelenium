import time

import pytest
from locators.plp import *
from locators.checkout import *
from locators.home import QTY_INPUT_FIRST
from locators.common import COOKIE_ACCEPT

from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *
from helpers.checkout import *

from conftest import click_if_present


# =========================
# Credenciais
# =========================
VALID_USER = "smoketesting1@automatizacao.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.checkout
@pytest.mark.mobile
def test_21_finalizacao_pedidos_mobile_sul(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Acessando categoria + Adicionando produto no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, wait=wait)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    # 3) Acessando checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 4) Alterando endereço + selecionando outro endereço como principal + voltar para o step de shipping
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_MAIN_ADDRESS(2), wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(BTN_ACCEPT_MODAL))
    mobile_click_strict(driver, BTN_ACCEPT_MODAL, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(3)

    mobile_click_strict(driver, BTN_VOLTAR, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 5) Acesando step de payment
    mobile_click_strict(driver, BTN_CONTINUAR_SHIPPING, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 6) Aplicando cupom pelo radio button + removendo cupom + fechando modal de cupom
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM, wait=wait)
    mobile_click_strict(driver, RADIO_BTN_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, BTN_REMOVER_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, RADIO_BTN_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    # 7) Abrir resumo + finalizando pedido via BOLETO
    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, wait=wait)
    time.sleep(5)  # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)

    mobile_click_strict(driver, BOLETO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, BOLETO_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, BOLETO_OPTION_21, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_BOLETO_SUL, wait=wait, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    mobile_click_strict(driver, BTN_IR_PARA_HOME, wait=wait, retries=4, sleep_between=0.25)

    # 8) Acessando categoria Marcas + Adicionando produto com a qtd superior a valor de R$ 5.000,00
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("marcas"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, wait=wait)

    safe_click_loc(driver, wait, QTY_INPUT_FIRST)
    fill(driver, QTY_INPUT_FIRST, "9")
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    # 9) Acessando checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, wait=wait)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 10) Aplicando cupom pelo radio button
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM)
    mobile_click_strict(driver, RADIO_BTN_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    # 11) Alterando endereço + selecionando outro endereço para entrega
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_SELECIONAR_ENDERECO(2), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 12) Removendo cupom + aceitando recebimento parcial BOLETO
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM)
    mobile_click_strict(driver, BTN_REMOVER_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    mobile_click_strict(driver, BOLETO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    scroll_to(driver, PARTIAL_BILLING_TRIGGER_BOLETO)
    mobile_click_strict(driver, PARTIAL_BILLING_TRIGGER_BOLETO, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_ACCEPT))
    mobile_click_strict(driver, PARTIAL_BILLING_ACCEPT, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_ACCEPT))

    # 13) Finalizando pedido com BOLETO + abrir e fechar resumo
    mobile_click_strict(driver, BOLETO_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, BOLETO_OPTION_21, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY)
    time.sleep(5)  # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_BOLETO_SUL, wait=wait, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    mobile_click_strict(driver, BTN_IR_PARA_HOME, wait=wait, retries=4, sleep_between=0.25)

    # 14) Acessando categoria + Adicionando produtos no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("promocoes"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(3))
    time.sleep(5)

    # 15) Indo para checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 16) Alterando endereço + selecionando outro endereço para entrega
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_SELECIONAR_ENDERECO(1), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 17) Abrir e fechar resumo + finalizar pedido via Boleto

    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, wait=wait)
    time.sleep(5)  # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)

    mobile_click_strict(driver, BOLETO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, BOLETO_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, BOLETO_OPTION_21, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_BOLETO_SUL, wait=wait, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    mobile_click_strict(driver, BTN_IR_PARA_HOME, wait=wait, retries=4, sleep_between=0.25)

