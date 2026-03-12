import pytest

from helpers.cadastro import (
    iniciar_fluxo_cadastro_mobile,
    preencher_dados_empresa,
    validar_token_invalido,
    validar_token_valido,
    finalizar_cadastro,
)

# ALTERE O E-MAIL AQUI
USER_EMAIL = "automatizacao@smoketesting.com"

@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.cadastro
@pytest.mark.mobile
def test_9_cadastro_mobile(driver, setup_site, wait):

    # 1 - Iniciar cadastro
    iniciar_fluxo_cadastro_mobile(driver, wait)

    # 2 - Preencher dados empresa
    preencher_dados_empresa(driver, wait, email_cliente=USER_EMAIL)

    # 3 - Validar token inválido
    validar_token_invalido(driver, wait)

    # 4 - Validar token correto
    validar_token_valido(driver, wait)

    # 5 - Finalizar cadastro
    finalizar_cadastro(driver, wait)