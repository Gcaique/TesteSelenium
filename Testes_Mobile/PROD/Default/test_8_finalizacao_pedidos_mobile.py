import time

import pytest
from locators.plp import *
from locators.checkout import *
from locators.home import QTY_INPUT_FIRST

from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *
from helpers.checkout import *


# =========================
# Credenciais
# =========================
VALID_USER = "hub.teste2-bruno-popup@minervafoods.com"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.checkout
@pytest.mark.mobile
def test_8_finalizacao_pedidos_mobile(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Acessando categoria + Adicionando produto no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos-premium"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, timeout=15)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    # 3) Acessando checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, timeout=20)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 4) Alterando endereço + selecionando outro endereço como principal + voltar para o step de shipping
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_MAIN_ADDRESS(2), timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(BTN_ACCEPT_MODAL))
    mobile_click_strict(driver, BTN_ACCEPT_MODAL, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(3)

    mobile_click_strict(driver, BTN_VOLTAR, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 5) Acesando step de payment
    mobile_click_strict(driver, BTN_CONTINUAR_SHIPPING, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 6) Aplicando cupom pelo radio button + removendo cupom + fechando modal de cupom
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM, timeout=10)
    mobile_click_strict(driver, RADIO_BTN_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, BTN_REMOVER_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, RADIO_BTN_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    # 7) Rejeitando recebimento parcial PIX
    mobile_click_strict(driver, PIX, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, PARTIAL_BILLING_TRIGGER_PIX, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_REJECT))
    mobile_click_strict(driver, PARTIAL_BILLING_REJECT, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_REJECT))

    # 8) Abrir resumo + finalizando pedido via PIX + copiar codigo pix via pagina de sucesso
    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, timeout=10)
    time.sleep(5) # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.5)

    mobile_click_strict(driver, TERMS_PIX, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_PIX, timeout=12, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PIX_SUCESSO))
    mobile_click_strict(driver, PIX_COPIAR, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(1)
    click_when_clickable(wait, LOGO)
    
    # 9) Acessando categoria Bovinos + Adicionando produto com a qtd superior a valor de R$ 5.000,00
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, timeout=15)

    safe_click_loc(driver, wait, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "9")
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1), timeout=10)
    time.sleep(5)

    # 10) Acessando checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, timeout=20)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 11) Aplicando cupom pelo radio button
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM, timeout=10)
    mobile_click_strict(driver, RADIO_BTN_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    # 12) Alterando endereço + selecionando outro endereço para entrega
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_SELECIONAR_ENDERECO(2), timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 13) Selecionando o método cartão de crédito
    mobile_click_strict(driver, CARTAO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(2)

    # 14) Removendo cupom + aceitando recebimento parcial BOLETO
    mobile_click_strict(driver, MOBILE_APLICAR_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MODAL_APLICAR_CUPOM, timeout=10)
    mobile_click_strict(driver, BTN_REMOVER_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    mobile_click_strict(driver, MOBILE_BTN_CLOSE_MODAL_CUPOM, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(MOBILE_MODAL_APLICAR_CUPOM))

    mobile_click_strict(driver, BOLETO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)
    scroll_to(driver, PARTIAL_BILLING_TRIGGER_BOLETO, timeout=10)
    mobile_click_strict(driver, PARTIAL_BILLING_TRIGGER_BOLETO, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_ACCEPT))
    mobile_click_strict(driver, PARTIAL_BILLING_ACCEPT, timeout=12, retries=4, sleep_between=0.25)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_ACCEPT))

    # 15) Finalizando pedido com BOLETO + abrir e fechar resumo
    mobile_click_strict(driver, BOLETO_SELECT, timeout=12, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, BOLETO_OPTION_21, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, TERMS_BOLETO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(1)
    
    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, timeout=10)
    time.sleep(5) # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_BOLETO, timeout=12, retries=4, sleep_between=0.25)

    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    mobile_click_strict(driver, BTN_IR_PARA_HOME, timeout=12, retries=4, sleep_between=0.25)

    # 16) Acessando categoria + Adicionando produtos no carrinho
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("pescados"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, timeout=10, retries=4, sleep_between=0.25)
    clickable(driver, SORTER_SELECT, timeout=15)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(3))
    time.sleep(5)

    # 17) Indo para checkout
    mobile_click_strict(driver, MOBILE_MINICART_ICON, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED, timeout=20)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 18) Alterando endereço + selecionando outro endereço para entrega
    mobile_click_strict(driver, BTN_ALTERAR_ENDERECO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(2)

    mobile_click_strict(driver, BTN_SELECIONAR_ENDERECO(1), timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    # 19) Abrir e fechar resumo + finalizar pedido via CARTÃO + aguardando disparo de erro
    mobile_click_strict(driver, CARTAO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    scroll_to(driver, INPUT_NOME_CARTAO, timeout=10)
    fill_input(driver, wait, INPUT_NOME_CARTAO, "Teste Automatizado", timeout=20)
    scroll_to(driver, INPUT_NUMERO_CARTAO, timeout=10)
    fill_input(driver, wait, INPUT_NUMERO_CARTAO, "5361 2006 8355 9262", timeout=20)
    scroll_to(driver, SELECT_MES_CARTAO, timeout=10)
    mobile_click_strict(driver, SELECT_MES_CARTAO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, OPTION_MES_CARTAO, timeout=12, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, SELECT_ANO_CARTAO, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.5)
    mobile_click_strict(driver, OPTION_ANO_CARTAO, timeout=12, retries=4, sleep_between=0.25)
    scroll_to(driver, INPUT_CVV_CARTAO, timeout=10)
    fill_input(driver, wait, INPUT_CVV_CARTAO, "898", timeout=20)

    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_CLOSE_SUMARY, timeout=10)
    time.sleep(5)  # tempo para conferencia
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.5)

    mobile_click_strict(driver, TERMS_CARTAO, timeout=12, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_CARTAO, timeout=12, retries=4, sleep_between=0.25)

    visible(driver, ERRO_CARTAO, timeout=20)

    # 22 Finalizar pedido com PIX
    mobile_click_strict(driver, PIX, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)
    mobile_click_strict(driver, TERMS_PIX, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_PIX, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, PIX_COPIAR, timeout=20)