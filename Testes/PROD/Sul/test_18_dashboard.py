import pytest
import os

from helpers.auth import ensure_logged_in, logout
from helpers.minicart import minicart_visible

from helpers.dashboard import *

from helpers.auth import (login_expect_email_not_found, login_expect_wrong_password, login_password)

from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("SMOKETESTING1")

NEW_EMAIL = os.getenv("NEW_EMAIL_DASHBOARD_SUL")
NEW_PASS = os.getenv("NEW_PASS_DASHBOARD")


@pytest.mark.regressao
@pytest.mark.sul
@pytest.mark.dashboard
def test_18_dashboard_sul(driver, setup_site, wait):
    # 1) Login inicial
    ensure_logged_in(driver, VALID_USER, VALID_PASS, wait=wait)
    assert minicart_visible(driver), "Era para estar logado, mas o minicart não apareceu."
    try_close_popups(driver)

    # 2) Acessa Minha Conta
    open_my_account(driver, wait)

    # 3) Dashboard: definir endereço principal (se existir)
    dashboard_set_main_address(driver, wait)

    # 4) Ver todos endereços
    go_all_addresses(driver, wait)

    # 5) Volta Minha conta e abre pedidos recentes
    open_my_account(driver, wait)
    open_recent_orders_from_dashboard(driver, wait)

    # 6) Meus pedidos: filtros e limpar filtros
    orders_filters_flow(driver, wait)

    # 7) Lista de favoritos
    favorites_page(driver, wait)

    # 8) Endereços: definir segundo como principal
    addresses_set_second_as_main(driver, wait)

    # 9) Meus pontos + relatório + volta
    points_flow(driver, wait)

    # 10) Cadastro de redes: navega tabs
    cadastro_redes_flow(driver, wait)

    # 11) Meus cupons: ver mais/copia/tab indisponíveis
    cupons_flow(driver, wait)

    # 12) Minhas missões
    misssoes_flow(driver, wait)

    # 13) Privacidade e dados + volta para home + acessar minha conta
    privacidade_dados(driver, wait)
    open_my_account(driver, wait)

    # 14) Info da conta: whatsapp + editar email + cancelar

    # WhatsApp
    account_whatsapp_toggle_flow(driver, wait)

    # Alterar email
    account_change_email_flow(driver, wait, new_email=NEW_EMAIL, current_password=VALID_PASS)

    # 15) Troca senha (aplica)
    change_password_flow(driver, wait, current_password=VALID_PASS, new_password=NEW_PASS)

    # 16) Logout e validações de login
    logout(driver, wait=wait)

    # email antigo não encontrado
    login_expect_email_not_found(driver, wait, VALID_USER)

    # usuário novo + senha antiga -> senha inválida
    login_expect_wrong_password(driver, wait, NEW_EMAIL, VALID_PASS)

    # loga com senha nova
    login_password(driver, password=NEW_PASS, context="login com senha nova", expect_success=True)

    assert minicart_visible(driver), "Era para estar logado com a senha nova, mas o minicart não apareceu."
    try_close_popups(driver)

    # volta email
    open_my_account(driver, wait)
    scroll_and_safe_click_loc(driver, wait, NAV_INFO_CONTA, timeout=12)
    visible(driver, BTN_EDIT_EMAIL, wait=wait)
    account_change_email_flow(driver, wait, new_email=VALID_USER, current_password=NEW_PASS)

    # volta senha
    change_password_flow(driver, wait, current_password=NEW_PASS, new_password=VALID_PASS)

    # assert logado no fim
    assert minicart_visible(driver), "Opcional: era para continuar logado no fim."
