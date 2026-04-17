import time
import os

import pytest

from conftest import click_if_present

from locators.common import COOKIE_ACCEPT

from helpers.auth import ensure_logged_in_mobile, logout
from helpers.minicart import minicart_visible
from helpers.popups import try_close_popups
from helpers.dashboard import *
from helpers.auth import (login_expect_email_not_found_mobile, login_expect_wrong_password, login_password)
from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("CAIQUE_OLIVEIRA3")

NEW_EMAIL = os.getenv("NEW_EMAIL_DASHBOARD")
NEW_PASS = os.getenv("NEW_PASS_DASHBOARD")


@pytest.mark.regressao
@pytest.mark.default
@pytest.mark.dashboard
@pytest.mark.mobile
def test_5_dashboard_mobile(driver, setup_site, wait):
    # 1) Login inicial
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS, wait=wait)
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
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_MINHA_CONTA, retries=4, sleep_between=0.25, wait=wait)
    open_recent_orders_from_dashboard(driver, wait)

    # 7) Meus pedidos: abre detalhe e copia codigo pix
    orders_open_first_and_copy_pix_mobile(driver, wait)

    # 8) Meus pedidos: filtros e limpar filtros
    mobile_click_strict(driver, MOBILE_BT_BACK, retries=4, sleep_between=0.25, wait=wait)
    orders_filters_flow_mobile(driver, wait)

    # 9) Lista de favoritos
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_LISTA_FAVORITOS, retries=4, sleep_between=0.25, wait=wait)
    time.sleep(3)

    # 10) Endereços: definir segundo como principal
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_ENDERECOS, retries=4, sleep_between=0.25, wait=wait)
    addresses_set_second_as_main_mobile(driver, wait)

    # 11) Meus pontos + relatório
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_MEUS_PONTOS, retries=4, sleep_between=0.25, wait=wait)
    apply_reward_filter_mobile(driver, wait, "earnings") # Ganhou
    apply_reward_filter_mobile(driver, wait, "used") # Usados
    apply_reward_filter_mobile(driver, wait, "expired") # Usados
    apply_reward_filter_mobile(driver, wait, "canceled") # Cancelados
    apply_reward_filter_mobile(driver, wait, "all") # Todos

    mobile_click_strict(driver, BTN_POINTS_REPORT, retries=4, sleep_between=0.25, wait=wait)
    visible(driver, POINTS_REPORT_FILTER, wait=wait)

    # 12) Cadastro de redes: navega tabs
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_CADASTRO_REDES, retries=4, sleep_between=0.25, wait=wait)
    apply_cadastro_redes_filter_mobile(driver, wait, "new-assign") #Agrupar CNPJ
    apply_cadastro_redes_filter_mobile(driver, wait, "info") # Informações
    apply_cadastro_redes_filter_mobile(driver, wait, "rules") # Regras de agrupamento
    apply_cadastro_redes_filter_mobile(driver, wait, "assigned-grid")  # CNPJs agrupados

    # 13) Meus cupons: ver mais/copia/tab indisponíveis
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_MEUS_CUPONS, retries=4, sleep_between=0.25, wait=wait)
    apply_meus_cupons_filter_mobile(driver, wait, "active")  # Ativos
    mobile_click_strict(driver, COUPON_VER_MAIS_1, retries=4, sleep_between=0.25, wait=wait)
    time.sleep(0.8)
    mobile_click_strict(driver, COUPON_COPY_1, retries=4, sleep_between=0.25, wait=wait)
    time.sleep(0.8)
    apply_meus_cupons_filter_mobile(driver, wait, "unavailable")  # Indisponíveis

    # 14) Minhas missões
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_MINHAS_MISSOES, retries=4, sleep_between=0.25, wait=wait)
    visible(driver, MISSIONS_READY, wait=wait)

    # 15) Privacidade e dados + volta para home + acessar minha conta
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_PRIVACIDADE_DADOS, retries=4, sleep_between=0.25, wait=wait)
    privacidade_dados_mobile(driver,wait)
    open_my_account(driver, wait)

    # 16) Info da conta: whatsapp + editar email

    # WhatsApp
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_INFO_CONTA, retries=4, sleep_between=0.25, wait=wait)
    account_whatsapp_toggle_flow_mobile(driver, wait)

    # Alterar email
    account_change_email_flow_mobile(driver, wait, new_email=NEW_EMAIL, current_password=VALID_PASS)

    # 17) Troca senha (aplica)
    change_password_flow_mobile(driver, wait, current_password=VALID_PASS, new_password=NEW_PASS)

    # 18) Logout e validações de login
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
    open_minha_conta_mobile(driver, wait=wait)
    mobile_click_strict(driver, MOBILE_NAV_INFO_CONTA, retries=4, sleep_between=0.25, wait=wait)
    visible(driver, BTN_EDIT_EMAIL, wait=wait)
    account_change_email_flow_mobile(driver, wait, new_email=VALID_USER, current_password=NEW_PASS)

    # volta senha
    change_password_flow_mobile(driver, wait, current_password=NEW_PASS, new_password=VALID_PASS)

    # assert logado no fim
    assert minicart_visible(driver), "Opcional: era para continuar logado no fim."

