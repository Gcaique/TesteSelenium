import pytest

from locators.home import LAST_ORDERS
from locators.lastOrders_lastItems import EMPTY_GRID_ORDERS

from helpers.auth import *
from helpers.waiters import *
from helpers.popups import *
from helpers.navigation import validate_navigation_by_auth_state_mobile
from helpers.dropdown import mobile_open_login_modal_from_dropdown
from helpers.home import go_home


# =========================
# Credenciais
# =========================
VALID_USER = "caique.oliveira@infobase.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.loginLogout
@pytest.mark.mobile
def test_2_loginLogout_mobile(driver, setup_site, wait):
    # 1) Abrir modal de login
    mobile_open_login_modal_from_dropdown(driver, timeout=12)

    # 2) Username inválido: email não encontrado
    submit_username_invalid(
        driver,
        "teste.12345@teste.com",
        "03) email não encontrado",
        tokens=["verifique", "cpf", "cnpj", "e-mail", "email"],
    )

    # 3) Username inválido: cnpj mismatch/não encontrado
    submit_username_invalid(
        driver,
        "42.765.782/0001-08",
        "04) cnpj não encontrado",
        tokens=["verifique", "e-mail", "email", "cpf", "cnpj"],
    )

    # 4) Username inválido: formato inválido
    submit_username_invalid(
        driver,
        "teste.teste",
        "05) formato inválido",
        tokens=["insira", "e-mail", "email", "cpf", "cnpj", "invál", "inval"],
    )

    # 5) Username inválido: cnpj fake
    submit_username_invalid(
        driver,
        "11.222.333/4444-55",
        "06) cnpj fake",
        tokens=["insira", "e-mail", "email", "cpf", "cnpj", "invál", "inval"],
    )

    # 6) Username válido: abrir senha
    submit_username_valid(driver, VALID_USER, "07) usuário válido")

    # 7) Senha inválida: erro
    login_password(driver, "SenhaErrada_", "08) senha inválida", expect_success=False)

    # 8) Senha válida: login OK
    login_password(driver, VALID_PASS, "09) senha válida", expect_success=True)

    # 9) Fluxos públicos LOGADO
    try_close_popups(driver)
    validate_navigation_by_auth_state_mobile(driver, logged=True)

    # 10) Logout
    logout_mobile(driver)
    assert_logged_out(driver, "11) após logout")

    # 11) Fluxos públicos DESLOGADO
    validate_navigation_by_auth_state_mobile(driver, logged=False)

    # 12) Últimos pedidos deslogado -> loga -> ver produtos
    go_home(driver)
    click(driver, LAST_ORDERS, timeout=20)

    visible(driver, MOBILE_LOGIN_DROPDOWN_OPENED, timeout=10)
    click(driver, MOBILE_LOGIN_ACESSO, timeout=10)
    submit_username_valid(driver, VALID_USER, "13) login via últimos pedidos (username)")
    login_password(driver, VALID_PASS, "13) login via últimos pedidos (senha)", expect_success=True)

    visible(driver, EMPTY_GRID_ORDERS, timeout=20)
    try_close_hotjar(driver)
    click(driver, EMPTY_GRID_ORDERS, timeout=10)

    # 13) Logout final
    logout_mobile(driver)
    assert_logged_out(driver, "14) fim do teste")