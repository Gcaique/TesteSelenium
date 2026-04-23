import pytest

from helpers.cadastro import *

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT


# =========================
# Altere o e-mail aqui
# =========================
USER_EMAIL = "automatizacao@smoketesting.com"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.cadastro
@pytest.mark.mobile
def test_9_cadastro_mobile(driver, setup_site, wait):
    # 1 - Iniciar cadastro
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    iniciar_fluxo_cadastro_mobile(driver, wait, regiao="default")

    # 2 - Preencher dados empresa
    preencher_dados_empresa(driver, wait, email_cliente=USER_EMAIL)

    # 3 - Validar token correto
    validar_token_valido(driver, wait)

    # 4 - Finalizar cadastro
    finalizar_cadastro(driver, wait)
