import time

import pytest

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT
from locators.plp import *
from locators.checkout import *
from locators.home import QTY_INPUT_FIRST

from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *
from helpers.checkout import *
from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("HUB_TESTE2_BRUNO_POPUP")


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.checkout
@pytest.mark.mobile
def test_8_finalizacao_pedidos_mobile(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Acessando categoria + Adicionando produto no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos-premium"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, wait=wait)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    # 3) Acessando checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, wait=wait)

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

    # 7) Rejeitando recebimento parcial PIX
    mobile_click_strict(driver, PIX, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, PARTIAL_BILLING_TRIGGER_PIX, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_REJECT))
    mobile_click_strict(driver, PARTIAL_BILLING_REJECT, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_REJECT))

    # 8) Abrir resumo + finalizando pedido via PIX + copiar codigo pix via pagina de sucesso
    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, wait=wait)
    time.sleep(5) # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)

    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_PIX, wait=wait, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PIX_SUCESSO))
    mobile_click_strict(driver, PIX_COPIAR, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    click_when_clickable(wait, LOGO)
    
    # 9) Acessando categoria Bovinos + Adicionando produto com a qtd superior a valor de R$ 5.000,00
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, wait=wait)

    safe_click_loc(driver, wait, QTY_INPUT_FIRST)
    fill(driver, QTY_INPUT_FIRST, "9")
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    # 10) Acessando checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, wait=wait)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 11) Aplicando cupom pelo radio button
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM, wait=wait)
    mobile_click_strict(driver, RADIO_BTN_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    # 12) Alterando endereço + selecionando outro endereço para entrega
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_SELECIONAR_ENDERECO(2), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 13) Selecionando o metodo cartão de crédito
    mobile_click_strict(driver, CARTAO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 14) Removendo cupom + aceitando recebimento parcial BOLETO
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM)
    mobile_click_strict(driver, BTN_REMOVER_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    mobile_click_strict(driver, BOLETO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    scroll_to(driver, PARTIAL_BILLING_TRIGGER_BOLETO, wait=wait)
    mobile_click_strict(driver, PARTIAL_BILLING_TRIGGER_BOLETO, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_ACCEPT))
    mobile_click_strict(driver, PARTIAL_BILLING_ACCEPT, wait=wait, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_ACCEPT))

    # 15) Finalizando pedido com BOLETO + abrir e fechar resumo
    mobile_click_strict(driver, BOLETO_SELECT, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, BOLETO_OPTION_21, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    
    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, wait=wait)
    time.sleep(5) # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_BOLETO, wait=wait, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    mobile_click_strict(driver, BTN_IR_PARA_HOME, wait=wait, retries=4, sleep_between=0.25)

    # 16) Acessando categoria + Adicionando produtos no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("pescados"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, wait=wait)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(3))
    time.sleep(5)

    # 17) Indo para checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, wait=wait)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 18) Alterando endereço + selecionando outro endereço para entrega
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_SELECIONAR_ENDERECO(1), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 19) Abrir e fechar resumo + finalizar pedido via CARTÃO + aguardando disparo de erro
    mobile_click_strict(driver, CARTAO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)

    scroll_to(driver, INPUT_NOME_CARTAO, wait=wait)
    fill_input(driver, wait, INPUT_NOME_CARTAO, "Teste Automatizado")
    scroll_to(driver, INPUT_NUMERO_CARTAO, wait=wait)
    fill_input(driver, wait, INPUT_NUMERO_CARTAO, "5361 2006 8355 9262")
    scroll_to(driver, SELECT_MES_CARTAO, wait=wait)
    mobile_click_strict(driver, SELECT_MES_CARTAO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, OPTION_MES_CARTAO, wait=wait, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, SELECT_ANO_CARTAO, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, OPTION_ANO_CARTAO, wait=wait, retries=4, sleep_between=0.25)
    scroll_to(driver, INPUT_CVV_CARTAO, wait=wait)
    fill_input(driver, wait, INPUT_CVV_CARTAO, "898")

    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, wait=wait)
    time.sleep(5)  # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(0.5)

    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_CARTAO, wait=wait, retries=4, sleep_between=0.25)

    visible(driver, ERRO_CARTAO, wait=wait)

    # 22 Finalizar pedido com PIX
    mobile_click_strict(driver, PIX, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_PIX, wait=wait, retries=4, sleep_between=0.25)
    visible(driver, PIX_COPIAR, wait=wait)
