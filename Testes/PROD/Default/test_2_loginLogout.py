import time

import pytest
from git import refresh

from helpers.auth import *
from helpers.waiters import *
from helpers.popups import *
from helpers.navigation import *
from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("CAIQUE_OLIVEIRA")


@pytest.mark.regressao
@pytest.mark.default
@pytest.mark.loginLogout
def test_2_loginLogout(driver, setup_site, wait):
    # 1) Abrir modal de login
    open_login(driver)

    # 2) Username inválido: email não encontrado
    submit_username_invalid(driver,
        "teste.12345@teste.com",
        "email não encontrado",
        tokens=["verifique", "cpf", "cnpj", "e-mail", "email"],
    )

    # 3) Username inválido: cnpj mismatch/não encontrado
    submit_username_invalid(
        driver,
        "42.765.782/0001-08",
        "cnpj não encontrado",
        tokens=["verifique", "e-mail", "email", "cpf", "cnpj"],
    )

    # 4) Username inválido: formato inválido
    submit_username_invalid(
        driver,
        "teste.teste",
        "formato inválido",
        tokens=["insira", "e-mail", "email", "cpf", "cnpj", "invál", "inval"],
    )

    # 5) Username inválido: cnpj fake
    submit_username_invalid(
        driver,
        "11.222.333/4444-55",
        "cnpj fake",
        tokens=["insira", "e-mail", "email", "cpf", "cnpj", "invál", "inval"],
    )

    # 6) Username válido: abrir senha
    submit_username_valid(driver, VALID_USER, "usuário válido")

    # 7) Senha inválida: erro
    login_password(driver, "SenhaErrada_", "senha inválida", expect_success=False)

    # 8) Senha válida: login OK
    login_password(driver, VALID_PASS, "senha válida", expect_success=True)

    # 9) Fluxos públicos LOGADO
    try_close_popups(driver)
    validate_navigation_by_auth_state(driver, logged=True)

    # 10) Logout
    logout(driver)
    assert_logged_out(driver, "após logout")

    # 11) Fluxos públicos DESLOGADO
    validate_navigation_by_auth_state(driver, logged=False)

    # 12) Últimos pedidos deslogado -> loga -> ver produtos
    go_home(driver)
    click(driver, LAST_ORDERS, wait=wait)

    visible(driver, USERNAME_INPUT, wait=wait)
    submit_username_valid(driver, VALID_USER, "login via últimos pedidos (username)")
    login_password(driver, VALID_PASS, "login via últimos pedidos (senha)", expect_success=True)

    visible(driver, EMPTY_GRID_ORDERS, wait=wait)
    try_close_hotjar(driver)
    click(driver, EMPTY_GRID_ORDERS, wait=wait)

    # 13) Logout final
    logout(driver)
    assert_logged_out(driver, "fim do teste")
