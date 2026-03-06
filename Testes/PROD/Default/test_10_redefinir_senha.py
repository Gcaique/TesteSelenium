import pytest

from helpers.redefinir_senha import (
    ensure_logged_out,
    abrir_login,
    clicar_esqueci_senha,
    preencher_email,
    clicar_enviar,
    mensagem_sucesso_visivel
)

VALID_USER = "caique.oliveira4@infobase.com.br"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.recovery
def test_10_redefinir_senha(driver, setup_site, wait):
    """
    Conversão do script:

      1) Garantir logout
      2) Abrir página de login
      3) Clicar em "Esqueci minha senha"
      4) Preencher email válido
      5) Clicar em Enviar
      6) Validar mensagem de sucesso
      TESTE INCOMPLETO
    """

    # 1) Garantir logout
    ensure_logged_out(driver)

    # 2) Abrir página de login
    abrir_login(driver, wait)

    # 3) Clicar em "Esqueci minha senha"
    clicar_esqueci_senha(driver, wait)

    # 4) Preencher email válido
    preencher_email(driver, wait, VALID_USER)

    # 5) Clicar em Enviar
    clicar_enviar(driver, wait)

    # 6) Validar mensagem de sucesso
    assert mensagem_sucesso_visivel(driver, wait), \
        "Mensagem de recuperação não apareceu."