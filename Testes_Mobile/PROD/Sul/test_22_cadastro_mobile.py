import pytest

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT

from helpers.cadastro import *


# =========================
# Altere o e-mail aqui
# =========================
USER_EMAIL = "automatizacao1@smoketesting.com"


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.cadastro
@pytest.mark.mobile
def test_22_cadastro_mobile_sul(driver, setup_site, wait):
    # 1 - Iniciar cadastro
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    iniciar_fluxo_cadastro_mobile(driver, wait, regiao="sul")

    # 2 - Preencher dados empresa
    preencher_dados_empresa(driver, wait, email_cliente=USER_EMAIL)

    # 3 - Validar token inválido
    validar_token_invalido(driver, wait)

    # 4 - Validar token correto
    validar_token_valido(driver, wait)

    # 5 - Finalizar cadastro
    finalizar_cadastro(driver, wait)
