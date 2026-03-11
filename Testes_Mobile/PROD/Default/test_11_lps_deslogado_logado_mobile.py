import pytest

from helpers.lp_deslogado_logado import *
from helpers.auth import submit_username_valid, login_password
from helpers.minicart import remove_simple_delete_mobile

from locators.cart import MOBILE_MINICART_ICON, MOBILE_MINICART_OPENED

VALID_USER = "caique.oliveira@infobase.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.lp
def test_11_lp_marcas_mobile(driver, setup_site, wait):

    # 1) Acessar LP Alma lusa pelo carrossel da HOME
    entrar_alma_lusa_via_home_mobile(driver, wait)

    # 2) Alma Lusa DESLOGADO
    fluxo_alma_lusa_deslogado_mobile(driver, wait)

    # 3) Ir para Estância
    ir_para_estancia_via_outras_marcas_mobile(driver, wait)

    # 4) Estância DESLOGADO
    fluxo_estancia_deslogado_mobile(driver, wait)

    # 5) Efetuar login
    click_when_clickable(wait, MOBILE_LOGIN_ACESSO)
    visible(driver, USERNAME_INPUT, timeout=10)

    submit_username_valid(driver, VALID_USER, "usuário válido")
    login_password(driver, VALID_PASS, "senha válida", expect_success=True)

    # 6) Navegar nas LPs de marcas logado + adicionar produtos em marcas selecionadas (Alma-lusa e Pul)
    marcas = [
        "alma-lusa",
        "pul",
        "pul-pro",
        "pul-selection",
        "estancia-92",
        "cabana",
    ]
    for marca in marcas:
        navegar_para_marca_mobile(driver, wait, marca)
        scroll_lento(driver)
        buscar_e_add_produto_marca(driver, wait, "sal", marca)

    # 7) Removendo item do mini-cart
    mobile_click_strict(driver, MOBILE_MINICART_ICON, 10, 4, 0.25)
    visible(driver, MOBILE_MINICART_OPENED, 10)
    remove_simple_delete_mobile(driver, wait, 1)
    time.sleep(5)