import pytest
from locators.refazer_pedido import BOLETO_COND_21, BOLETO_COND_28
from helpers.refazer_pedido import *

# Dados de teste
USERNAME = "smoketesting@automatizacao.com.br"
PASSWORD = "Min@1234"


@pytest.mark.smoke
@pytest.mark.refazer_pedidos
def test_12_refazerPedidos(driver, setup_site, wait):
    """
    Fluxo completo Refazer Pedidos (com Ver Similar):
    Login -> filtro -> Ver Similar -> adicionar pedido -> checkout cond 21 ->
    Comprados Recentemente -> filtro -> favoritos -> avise-me ->
    Ver Similar + Adicionar -> adicionar todos -> checkout cond 28 ->
    Meus Pedidos -> detalhe -> refazer pedido.
    """

    # ── 1) Login via Ultimos Pedidos ────────────────────────
    clicar_ultimos_pedidos(driver, wait)
    preencher_email_login(driver, wait, USERNAME)
    preencher_senha_login(driver, wait, PASSWORD)
    aguardar_redirect_ultimos_pedidos(driver, wait)
    fechar_roleta_cupons(driver, wait)

    # ── 2) Ultimos Pedidos - Filtro ─────────────────────────
    filtrar_ultimos_7_dias(driver, wait)

    # ── 3) Ver Similar + Adicionar pedido ao carrinho ──────
    ver_similar_refazer_e_adicionar(driver, wait)

    # ── 4) Checkout 1 - Shipping ──────────────────────────
    avancar_shipping(driver, wait)

    # ── 5) Checkout 1 - Payment Boleto cond 21 ────────────
    selecionar_boleto_e_finalizar(driver, wait, BOLETO_COND_21)

    # ── 6) Volta para Home com refresh ────────────────────
    ir_para_home(driver, wait)

    # ── 7) Comprados Recentemente - Navegacao e Filtro ────
    navegar_comprados_recentemente(driver, wait)
    filtrar_comprados_recentemente(driver, wait)
    scroll_ate_adicionar_todos(driver, wait)
    favoritar_e_desfavoritar(driver, wait)

    # ── 8) Avise-me / Sem Estoque ─────────────────────────
    interagir_avise_me(driver, wait)

    # ── 9) Ver Similar + Adicionar no carrinho ────────────
    ver_similar_comprados_e_adicionar(driver, wait)

    # ── 10) Adicionar todos ao carrinho + Checkout ────────
    adicionar_todos_ao_carrinho_e_checkout(driver, wait)

    # ── 11) Checkout 2 - Shipping ─────────────────────────
    avancar_shipping(driver, wait)

    # ── 12) Checkout 2 - Payment Boleto cond 28 ───────────
    selecionar_boleto_e_finalizar(driver, wait, BOLETO_COND_28)

    # ── 13) Meus Pedidos ──────────────────────────────────
    abrir_meus_pedidos(driver, wait)
    ordenar_por_forma_pagamento(driver, wait)
    abrir_detalhe_primeiro_pedido(driver, wait)
    refazer_pedido(driver, wait)

    print("AUTOMACAO FINALIZADA COM SUCESSO")
