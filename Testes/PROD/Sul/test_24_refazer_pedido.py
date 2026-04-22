import pytest

from locators.checkout import BOLETO_OPTION_21, BOLETO_OPTION_28
from locators.cart import BTN_CHECKOUT_TOP
from locators.header import DD_MEUS_PEDIDOS

from helpers.lastOrders_lastItems import *
from helpers.auth import submit_username_valid, login_password
from helpers.popups import try_close_popups
from helpers.checkout import avancar_shipping, selecionar_boleto_e_finalizar, ir_para_home
from helpers.dropdown import open_dropdown_item
from helpers.credentials import get_creds


# Dados de teste
VALID_USER, VALID_PASS = get_creds("SMOKETESTING2")


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.refazer
def test_24_refazer_pedido_sul(driver, setup_site, wait):
    # 1) Login via Ultimos Pedidos
    clicar_ultimos_pedidos(driver, wait)
    submit_username_valid(driver, VALID_USER, "usuário válido")
    login_password(driver, VALID_PASS, "senha válida", expect_success=True)
    aguardar_redirect_ultimos_pedidos(driver, wait)
    try_close_popups(driver)

    # 2) Ultimos Pedidos - (Filtro)
    filtrar_ultimos_7_dias(driver, wait)

    # 3) Ver Similar + Adicionar pedido ao carrinho
    ver_similar_refazer_e_adicionar(driver, wait)

    # 4) Finalizar compra
    wait.until(EC.element_to_be_clickable(BTN_CHECKOUT_TOP))
    click_when_clickable(wait, BTN_CHECKOUT_TOP)

    avancar_shipping(driver, wait)

    selecionar_boleto_e_finalizar(driver, wait, BOLETO_OPTION_21)

    ir_para_home(driver, wait)

    # 5) Comprados Recentemente (Filtro + favoritar e desvaforitar um item)
    navegar_comprados_recentemente(driver, wait)
    filtrar_comprados_recentemente(driver, wait)
    scroll_ate_adicionar_todos(driver, wait)
    favoritar_e_desfavoritar(driver, wait)

    # 6) Avise-me + refresh na pagina (Verifica se o avise-me continua ativo)
    interagir_avise_me(driver, wait, BTN_PROXIMA_PAGINA)

    # 7) Ver Similar + Adicionar no carrinho
    ver_similar_comprados_e_adicionar(driver, wait)

    # 8) Adicionar todos ao carrinho
    adicionar_todos_ao_carrinho(driver, wait)

    # 9) Finalizar compra
    wait.until(EC.element_to_be_clickable(BTN_CHECKOUT_TOP))
    click_when_clickable(wait, BTN_CHECKOUT_TOP)

    avancar_shipping(driver, wait)

    selecionar_boleto_e_finalizar(driver, wait, BOLETO_OPTION_28)

    # 10) Meus Pedidos
    open_dropdown_item(driver, DD_MEUS_PEDIDOS, wait=wait)
    ordenar_por_forma_pagamento(driver, wait)
    abrir_detalhe_primeiro_pedido(driver, wait)
    refazer_pedido(driver, wait)
