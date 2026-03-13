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
def test_8_finalizacao_pedidos(driver, setup_site, wait):
    # 1) Login (fonte da verdade = mini-cart)
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Acessando categoria + Adicionando produto no carrinho
    click_when_clickable(wait, CATEGORY_MENU("Bovinos Premium"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # 3) Acessando checkout
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    time.sleep(5)

    # 4) Alterando endereço + selecionando outro endereço como principal + voltar para o step de shipping
    click_when_clickable(wait, BTN_ALTERAR_ENDERECO)
    time.sleep(2)

    click_when_clickable(wait, BTN_MAIN_ADDRESS(2))
    wait.until(EC.visibility_of_element_located(BTN_ACCEPT_MODAL))
    click_when_clickable(wait, BTN_ACCEPT_MODAL)
    time.sleep(3)

    click_when_clickable(wait, BTN_VOLTAR)
    time.sleep(2)

    # 5) Acesando step de payment
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)
    time.sleep(5)

    # 6) Aplicando cupom pelo input + removendo cupom + aplicando cupom pelo radio button
    fill_input(driver, wait, INPUT_CUPOM, "automacao10", timeout=20)
    click_when_clickable(wait, BTN_APLICAR_CUPOM)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    click_when_clickable(wait, BTN_REMOVER_CUPOM)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    click_when_clickable(wait, RADIO_BTN_CUPOM)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    # 7) Rejeitando recebimento parcial PIX
    click_when_clickable(wait, PIX)
    time.sleep(5)
    click_when_clickable(wait, PARTIAL_BILLING_TRIGGER_PIX)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_REJECT))
    click_when_clickable(wait, PARTIAL_BILLING_REJECT)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_REJECT))

    # 8) Finalizando pedido via PIX + copiar codigo pix via pagina de sucesso + ir para home
    click_when_clickable(wait, TERMS_PIX)
    time.sleep(1)
    click_when_clickable(wait, BTN_FINALIZAR_COMPRA_PIX)
    wait.until(EC.visibility_of_element_located(PIX_SUCESSO))
    click_when_clickable(wait, PIX_COPIAR)
    time.sleep(1)
    click_when_clickable(wait, LOGO)

    # 9) Acessando categoria Bovinos + Adicionando produto com a qtd superior a valor de R$ 5.000,00
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "9")
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1), timeout=10)
    wait_minicart_ready(driver)

    # 10) Acessando checkout
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    time.sleep(5)

    # 11) Aplicando cupom pelo radio button
    click_when_clickable(wait, RADIO_BTN_CUPOM)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    # 12) Alterando endereço + selecionando outro endereço para entrega
    click_when_clickable(wait, BTN_ALTERAR_ENDERECO)
    time.sleep(2)

    click_when_clickable(wait, BTN_SELECIONAR_ENDERECO(2))
    time.sleep(5)

    # 13) Selecionando o método cartão de crédito
    click_when_clickable(wait, CARTAO)
    time.sleep(2)

    # 14) Removendo cupom + aceitando recebimento parcial BOLETO
    click_when_clickable(wait, BTN_REMOVER_CUPOM)
    wait.until(EC.visibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))
    wait.until(EC.invisibility_of_element_located(MENSAGEM_SUCESSO_CUPOM))

    click_when_clickable(wait, BOLETO)
    time.sleep(5)
    click_when_clickable(wait, PARTIAL_BILLING_TRIGGER_BOLETO)
    wait.until(EC.visibility_of_element_located(PARTIAL_BILLING_ACCEPT))
    click_when_clickable(wait, PARTIAL_BILLING_ACCEPT)
    wait.until(EC.invisibility_of_element_located(PARTIAL_BILLING_ACCEPT))

    # 15) Finalizando pedido com BOLETO
    click_when_clickable(wait, BOLETO_SELECT)
    click_when_clickable(wait, BOLETO_OPTION_21)
    time.sleep(5)
    click_when_clickable(wait, TERMS_BOLETO)
    time.sleep(1)
    click_when_clickable(wait, BTN_FINALIZAR_COMPRA_BOLETO)
    wait.until(EC.visibility_of_element_located(PAGINA_SUCESSO))
    click_when_clickable(wait, BTN_IR_PARA_HOME)

    # 16) Acessando categoria + Adicionando produtos no carrinho
    click_when_clickable(wait, CATEGORY_MENU("Cordeiros"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    time.sleep(5)

    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(3))
    wait_minicart_ready(driver)

    # 17) Indo para checkout
    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 18) Alterando endereço + selecionando outro endereço para entrega
    click_when_clickable(wait, BTN_ALTERAR_ENDERECO)
    time.sleep(2)

    click_when_clickable(wait, BTN_SELECIONAR_ENDERECO(1))
    time.sleep(5)

    # 19) Acessando step de shipping + selecionando e definindo o endereço como principal
    click_when_clickable(wait, STEP_ENDERECO)
    time.sleep(2)

    click_when_clickable(wait, BTN_MAIN_ADRESS_SHIPPING)
    wait.until(EC.visibility_of_element_located(BTN_ACCEPT_MODAL))
    click_when_clickable(wait, BTN_ACCEPT_MODAL)
    time.sleep(3)

    # 20) Acesando step de payment
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)
    time.sleep(5)

    # 21) Finalizar pedido via CARTÃO + aguardando disparo de erro
    click_when_clickable(wait, CARTAO)
    time.sleep(5)

    fill_input(driver, wait, INPUT_NOME_CARTAO, "Teste Automatizado", timeout=20)
    fill_input(driver, wait, INPUT_NUMERO_CARTAO, "5361 2006 8355 9262", timeout=20)
    click_when_clickable(wait, SELECT_MES_CARTAO)
    time.sleep(0.5)
    click_when_clickable(wait, OPTION_MES_CARTAO)
    click_when_clickable(wait, SELECT_ANO_CARTAO)
    time.sleep(0.5)
    click_when_clickable(wait, OPTION_ANO_CARTAO)
    fill_input(driver, wait, INPUT_CVV_CARTAO, "898", timeout=20)

    click_when_clickable(wait, TERMS_CARTAO)
    click_when_clickable(wait, BTN_FINALIZAR_COMPRA_CARTAO)
    visible(driver, ERRO_CARTAO, timeout=20)

    # 22 Finalizar pedido com PIX
    click_when_clickable(wait, PIX)
    time.sleep(5)
    click_when_clickable(wait, TERMS_PIX)
    time.sleep(1)
    click_when_clickable(wait, BTN_FINALIZAR_COMPRA_PIX)
    wait.until(EC.visibility_of_element_located(PIX_SUCESSO))