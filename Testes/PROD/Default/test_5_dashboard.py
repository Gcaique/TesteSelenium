import pytest

from helpers.auth import ensure_logged_in, logout
from helpers.minicart import minicart_visible
from helpers.popups import try_close_popups

from helpers.dashboard import *

from helpers.auth import (login_expect_email_not_found, login_expect_wrong_password, login_password)

# =========================
# Credenciais (padrão seu)
# =========================
VALID_USER = "caique.oliveira3@infobase.com.br"
VALID_PASS = "Min@1234"

NEW_EMAIL = "caique.oliveira31@infobase.com.br"
NEW_PASS = "Min@1234567"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.dashboard
def test_5_dashboard(driver, setup_site, wait):
    """
    Parte A: Login + Compra + Checkout Pix
    Parte B: Minha Conta / Dashboard (endereços, pedidos, filtros, favoritos, endereços)
    Parte C: Pontos / Relatórios / Cadastro de redes / Cupons / Missões
    Parte D: Info da conta (editar email + trocar senha)  <-- obrigatório
    Parte E: Logout + validações login + login com senha nova + voltar email  <-- obrigatório
    """

    # 1) Login inicial
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    assert minicart_visible(driver), "Era para estar logado, mas o minicart não apareceu."
    try_close_popups(driver)

    # 2) Compra + checkout pix
    buy_first_product_and_checkout_pix(driver, wait)
    try_close_popups(driver)

    # 3) Acessa Minha Conta
    open_my_account(driver, wait)

    # 4) Dashboard: definir endereço principal (se existir)
    dashboard_set_main_address(driver, wait)

    # 5) Ver todos endereços
    go_all_addresses(driver, wait)

    # 6) Volta Minha conta e abre pedidos recentes
    open_my_account(driver, wait)
    open_recent_orders_from_dashboard(driver, wait)

    # 7) Meus pedidos: abre detalhe e copia codigo pix
    orders_open_first_and_copy_pix(driver, wait)

    # 8) Meus pedidos: filtros e limpar filtros
    orders_filters_flow(driver, wait)

    # 9) Lista de favoritos
    favorites_page(driver, wait)

    # 10) Endereços: definir segundo como principal
    addresses_set_second_as_main(driver, wait)

    # 11) Meus pontos + relatório + volta
    points_flow(driver, wait)

    # 12) Cadastro de redes: navega tabs
    cadastro_redes_flow(driver, wait)

    # 13) Meus cupons: ver mais/copia/tab indisponíveis
    cupons_flow(driver, wait)

    # 14) Minhas missões
    misssoes_flow(driver, wait)

    # ------------------------------------------------------------
    # 15) OBRIGATÓRIO: Info da conta: whatsapp + editar email + cancelar
    # ------------------------------------------------------------
    # WhatsApp
    account_whatsapp_toggle_flow(driver, wait)

    # Alterar email
    account_change_email_flow(driver, wait, new_email=NEW_EMAIL, current_password=VALID_PASS)

    # ------------------------------------------------------------
    # 16) OBRIGATÓRIO: Troca senha (aplica)
    # ------------------------------------------------------------
    change_password_flow(driver, wait, current_password=VALID_PASS, new_password=NEW_PASS)

    # ------------------------------------------------------------
    # 17) OBRIGATÓRIO: Logout e validações de login
    # ------------------------------------------------------------
    logout(driver)

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
    visible(driver, BTN_EDIT_EMAIL, timeout=12)
    account_change_email_flow(driver, wait, new_email=VALID_USER, current_password=NEW_PASS)

    # volta senha
    change_password_flow(driver, wait, current_password=NEW_PASS, new_password=VALID_PASS)

    # assert logado no fim
    assert minicart_visible(driver), "Opcional: era para continuar logado no fim."
