import time

import pytest

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT

from helpers.auth import ensure_logged_in_mobile, logout
from helpers.minicart import minicart_visible
from helpers.popups import try_close_popups
from helpers.dashboard import *
from helpers.auth import (login_expect_email_not_found_mobile, login_expect_wrong_password, login_password)


# =========================
# Credenciais
# =========================
VALID_USER = "caique.oliveira3@infobase.com.br"
VALID_PASS = "Min@1234"

NEW_EMAIL = "caique.oliveira31@infobase.com.br"
NEW_PASS = "Min@1234567"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.dashboard
@pytest.mark.mobile
def test_5_dashboard_mobile(driver, setup_site, wait):
    # 1) Login inicial
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)
    assert minicart_visible(driver), "Era para estar logado, mas o minicart não apareceu."
    try_close_popups(driver)

    # 2) Compra + checkout pix
    buy_first_product_and_checkout_pix_mobile(driver, wait)
    try_close_popups(driver)

    # 3) Acessa Minha Conta
    open_my_account(driver, wait)

    # 4) Dashboard: definir endereço principal (se existir)
    dashboard_set_main_address(driver, wait)

    # 5) Ver todos endereços
    go_all_addresses(driver, wait)

    # 6) Volta Minha conta e abre pedidos recentes
    time.sleep(2)
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_MINHA_CONTA, timeout=12, retries=4, sleep_between=0.25)
    open_recent_orders_from_dashboard(driver, wait)

    # 7) Meus pedidos: abre detalhe e copia codigo pix
    orders_open_first_and_copy_pix_mobile(driver, wait)

    # 8) Meus pedidos: filtros e limpar filtros
    mobile_click_strict(driver, MOBILE_BT_BACK, timeout=12, retries=4, sleep_between=0.25)
    orders_filters_flow_mobile(driver, wait)

    # 9) Lista de favoritos
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_LISTA_FAVORITOS, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(3)

    # 10) Endereços: definir segundo como principal
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_ENDERECOS, timeout=12, retries=4, sleep_between=0.25)
    addresses_set_second_as_main_mobile(driver, wait)

    # 11) Meus pontos + relatório
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_MEUS_PONTOS, timeout= 12, retries=4, sleep_between=0.25)
    apply_reward_filter_mobile(driver, wait, "earnings") # Ganhou
    apply_reward_filter_mobile(driver, wait, "used") # Usados
    apply_reward_filter_mobile(driver, wait, "expired") # Usados
    apply_reward_filter_mobile(driver, wait, "canceled") # Cancelados
    apply_reward_filter_mobile(driver, wait, "all") # Todos

    mobile_click_strict(driver, BTN_POINTS_REPORT, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, POINTS_REPORT_FILTER, timeout=25)

    # 12) Cadastro de redes: navega tabs
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_CADASTRO_REDES, timeout=12, retries=4, sleep_between=0.25)
    apply_cadastro_redes_filter_mobile(driver, wait, "new-assign") #Agrupar CNPJ
    apply_cadastro_redes_filter_mobile(driver, wait, "info") # Informações
    apply_cadastro_redes_filter_mobile(driver, wait, "rules") # Regras de agrupamento
    apply_cadastro_redes_filter_mobile(driver, wait, "assigned-grid")  # CNPJs agrupados

    # 13) Meus cupons: ver mais/copia/tab indisponíveis
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_MEUS_CUPONS, timeout=12, retries=4, sleep_between=0.25)
    apply_meus_cupons_filter_mobile(driver, wait, "active")  # Ativos
    mobile_click_strict(driver, COUPON_VER_MAIS_1, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.8)
    mobile_click_strict(driver, COUPON_COPY_1, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(0.8)
    apply_meus_cupons_filter_mobile(driver, wait, "unavailable")  # Indisponíveis

    # 14) Minhas missões
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_MINHAS_MISSOES, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, MISSIONS_READY, timeout=25)

    # 15) Info da conta: whatsapp + editar email

    # WhatsApp
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_INFO_CONTA, timeout=12, retries=4, sleep_between=0.25)
    account_whatsapp_toggle_flow_mobile(driver, wait)

    # Alterar email
    account_change_email_flow_mobile(driver, wait, new_email=NEW_EMAIL, current_password=VALID_PASS)

    # 16) Troca senha (aplica)
    change_password_flow_mobile(driver, wait, current_password=VALID_PASS, new_password=NEW_PASS)

    # 17) Logout e validações de login
    logout(driver)

    # email antigo não encontrado
    login_expect_email_not_found_mobile(driver, wait, VALID_USER)

    # usuário novo + senha antiga -> senha inválida
    login_expect_wrong_password(driver, wait, NEW_EMAIL, VALID_PASS)

    # loga com senha nova
    login_password(driver, password=NEW_PASS, context="login com senha nova", expect_success=True)

    assert minicart_visible(driver), "Era para estar logado com a senha nova, mas o minicart não apareceu."
    try_close_popups(driver)

    # volta email
    open_my_account(driver, wait)
    open_minha_conta_mobile(driver, timeout=20)
    mobile_click_strict(driver, MOBILE_NAV_INFO_CONTA, timeout=12, retries=4, sleep_between=0.25)
    visible(driver, BTN_EDIT_EMAIL, timeout=12)
    account_change_email_flow_mobile(driver, wait, new_email=VALID_USER, current_password=NEW_PASS)

    # volta senha
    change_password_flow_mobile(driver, wait, current_password=NEW_PASS, new_password=VALID_PASS)

    # assert logado no fim
    assert minicart_visible(driver), "Opcional: era para continuar logado no fim."

