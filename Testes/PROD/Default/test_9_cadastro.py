import pytest

from helpers.cadastro import (
    iniciar_fluxo_cadastro,
    preencher_dados_empresa,
    validar_token_invalido,
    validar_token_valido,
    finalizar_cadastro,
)


@pytest.mark.cadastro
@pytest.mark.fluxo_completo
def test_9_cadastro_completo(driver, setup_site, wait):

    # 1 - Iniciar cadastro
    iniciar_fluxo_cadastro(driver, wait)

    # 2 - Preencher dados empresa
    preencher_dados_empresa(driver, wait)

    # 3 - Validar token inválido
    validar_token_invalido(driver, wait)

    # 4 - Validar token correto
    validar_token_valido(driver, wait)

    # 5 - Finalizar cadastro
    finalizar_cadastro(driver, wait)