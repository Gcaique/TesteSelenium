import pytest

from conftest import click_if_present

from locators.checkout import BOLETO_OPTION_21, BOLETO_OPTION_28
from locators.cart import BTN_CHECKOUT_TOP, MOBILE_MINICART_ICON_SUL, MOBILE_MINICART_OPENED_SUL
from locators.header import DD_MEUS_PEDIDOS
from locators.header import MOBILE_LOGIN_ACESSO
from locators.common import COOKIE_ACCEPT

from helpers.lastOrders_lastItems import *
from helpers.auth import submit_username_valid, login_password
from helpers.popups import try_close_popups
from helpers.checkout import avancar_shipping_mobile, selecionar_boleto_e_finalizar_mobile, ir_para_home
from helpers.dropdown import open_dropdown_item
from helpers.actions import mobile_click_strict, visible


# =========================
# Credenciais
# =========================
VALID_USER = "smoketesting2@automatizacao.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.refazer
@pytest.mark.mobile
def test_24_refazer_pedido_mobile_sul(driver, setup_site, wait):
    # 1) Login via Ultimos Pedidos
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    clicar_ultimos_pedidos(driver, wait)
    mobile_click_strict(driver, MOBILE_LOGIN_ACESSO, 10, 4, 0.25)
    submit_username_valid(driver, VALID_USER, "usuário válido")
    login_password(driver, VALID_PASS, "senha válida", expect_success=True)
    aguardar_redirect_ultimos_pedidos(driver, wait)
    try_close_popups(driver)

    # 2) Ultimos Pedidos - (Filtro)
    filtrar_ultimos_7_dias_mobile(driver, wait)

    # 3) Ver Similar + Adicionar pedido ao carrinho
    ver_similar_refazer_e_adicionar_mobile(driver, wait)

    # 4) Finalizar compra
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, timeout=20)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    avancar_shipping_mobile(driver, wait)

    selecionar_boleto_e_finalizar_mobile(driver, wait, BOLETO_OPTION_21)

    ir_para_home(driver, wait)

    # 5) Comprados Recentemente (Filtro + favoritar e desvaforitar um item)
    navegar_comprados_recentemente(driver, wait)
    filtrar_ultimos_7_dias_mobile(driver, wait)
    scroll_ate_adicionar_todos(driver, wait)
    favoritar_e_desfavoritar(driver, wait)

    # 6) Avise-me + refresh na pagina (Verifica se o avise-me continua ativo)
    interagir_avise_me(driver, wait, BTN_PROXIMA_PAGINA)

    # 7) Ver Similar + Adicionar no carrinho
    ver_similar_comprados_e_adicionar_mobile(driver, wait)

    # 8) Adicionar todos ao carrinho
    adicionar_todos_ao_carrinho_mobile(driver, wait)

    # 9) Finalizar compra
    mobile_click_strict(driver, MOBILE_MINICART_ICON_SUL, timeout=20, retries=4, sleep_between=0.25)
    visible(driver, MOBILE_MINICART_OPENED_SUL, timeout=20)

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

    avancar_shipping_mobile(driver, wait)

    selecionar_boleto_e_finalizar_mobile(driver, wait, BOLETO_OPTION_28)

    # 10) Meus Pedidos
    open_dropdown_item(driver, DD_MEUS_PEDIDOS, 10)
    abrir_detalhe_primeiro_pedido_mobile(driver, wait)
    refazer_pedido(driver, wait)