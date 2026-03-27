import pytest

from helpers.cadastro import (
    iniciar_fluxo_cadastro,
    preencher_dados_empresa,
    validar_token_invalido,
    validar_token_valido,
    finalizar_cadastro,
)


# =========================
# Altere o e-mail aqui
# =========================
USER_EMAIL = "automatizacao1@smoketesting.com"


@pytest.mark.smoke
@pytest.mark.sul
@pytest.mark.cadastro
def test_22_cadastro_sul(driver, setup_site, wait):
    # 1 - Iniciar cadastro
    iniciar_fluxo_cadastro(driver, wait)

    # 2 - Preencher dados empresa
    preencher_dados_empresa(driver, wait, email_cliente=USER_EMAIL)

    # 3 - Validar token inválido
    validar_token_invalido(driver, wait)

    # 4 - Validar token correto
    validar_token_valido(driver, wait)

    # 5 - Finalizar cadastro
    finalizar_cadastro(driver, wait)