import time
from selenium.webdriver.support import expected_conditions as EC

from helpers.actions import safe_click_loc, scroll_into_view, fill_input, try_click, scroll_and_safe_click_loc
from helpers.waiters import visible

from helpers.minicart import wait_minicart_loading
from helpers.popups import try_close_popups
from helpers.dropdown import open_user_dropdown

from locators.plp import *
from locators.cart import *
from locators.checkout import *
from locators.header import *
from locators.dashboard import *
from locators.common import *


# ---------------------------
# COMPRA + CHECKOUT PIX
# ---------------------------
def buy_first_product_and_checkout_pix(driver, wait):
    # acesso categoria
    safe_click_loc(driver, wait, CATEGORY_BOVINOS_PREMIUM, timeout=12)

    # garante listagem carregada + scroll
    visible(driver, BTN_INCREMENT_QTY, timeout=20)
    scroll_into_view(driver, TOOLBAR_AMOUNT, timeout=12)

    # incrementa e adiciona
    safe_click_loc(driver, wait, BTN_INCREMENT_QTY, timeout=12)
    safe_click_loc(driver, wait, BTN_ADD_TO_CART, timeout=12)

    # espera minicart atualizar
    wait_minicart_loading(driver)

    visible(driver, BTN_CHECKOUT_TOP, timeout=20)
    safe_click_loc(driver, wait, BTN_CHECKOUT_TOP, timeout=12)

    # shipping -> continuar
    visible(driver, BTN_CONTINUAR_SHIPPING, timeout=30)
    safe_click_loc(driver, wait, BTN_CONTINUAR_SHIPPING, timeout=20)

    # payment -> PIX + termos + finalizar
    visible(driver, PIX, timeout=30)
    safe_click_loc(driver, wait, PIX, timeout=12)

    visible(driver, TERMS_PIX, timeout=25)
    safe_click_loc(driver, wait, TERMS_PIX, timeout=12)

    visible(driver, BTN_FINALIZAR_COMPRA, timeout=25)
    safe_click_loc(driver, wait, BTN_FINALIZAR_COMPRA, timeout=12)

    # aguarda retorno
    time.sleep(6)


# ---------------------------
# NAVEGAÇÕES DASHBOARD
# ---------------------------
def open_my_account(driver, wait):
    open_user_dropdown(driver)
    safe_click_loc(driver, wait, DD_MINHA_CONTA, timeout=12)
    visible(driver, BTN_MAIN_ADDRESS_DASHBOARD, timeout=25)


def dashboard_set_main_address(driver, wait):
    try:
        visible(driver, BTN_MAIN_ADDRESS_DASHBOARD, timeout=12)
        scroll_and_safe_click_loc(driver, wait, BTN_MAIN_ADDRESS_DASHBOARD, timeout=12)
        visible(driver, BTN_ACCEPT_MODAL, timeout=12)
        scroll_and_safe_click_loc(driver, wait, BTN_ACCEPT_MODAL, timeout=12)
        time.sleep(1)
    except Exception:
        pass


def go_all_addresses(driver, wait):
    scroll_and_safe_click_loc(driver, wait, LINK_VER_TODOS_ENDERECOS, timeout=12)
    time.sleep(2)


def open_recent_orders_from_dashboard(driver, wait):
    scroll_and_safe_click_loc(driver, wait, LINK_PEDIDOS_RECENTES, timeout=12)
    time.sleep(2)


def orders_open_first_and_copy_pix(driver, wait):
    # Em vez de só "visible", scroll ajuda bastante em grids
    scroll_into_view(driver, GRID_ORDERS_READY, timeout=25)

    scroll_and_safe_click_loc(driver, wait, FIRST_ORDER_DETAILS, timeout=12)
    time.sleep(5)

    scroll_and_safe_click_loc(driver, wait, BTN_COPY_PIX, timeout=12)
    visible(driver, BTN_COPY_PIX_COPIED, timeout=12)
    time.sleep(2)


def orders_filters_flow(driver, wait):
    scroll_and_safe_click_loc(driver, wait, NAV_MEUS_PEDIDOS, timeout=12)

    # período 7 dias + filtrar
    scroll_and_safe_click_loc(driver, wait, SEL_PERIOD, timeout=12)
    scroll_and_safe_click_loc(driver, wait, OPT_PERIOD_7D, timeout=12)

    scroll_into_view(driver, BTN_FILTER, timeout=12)
    scroll_and_safe_click_loc(driver, wait, BTN_FILTER, timeout=12)
    time.sleep(1)

    # status pedido + status pagamento + filtrar
    scroll_and_safe_click_loc(driver, wait, SEL_ORDER_STATUS, timeout=12)
    scroll_and_safe_click_loc(driver, wait, OPT_ORDER_STATUS_FATURADO, timeout=12)
    time.sleep(0.5)

    scroll_and_safe_click_loc(driver, wait, SEL_PAYMENT_STATUS, timeout=12)
    scroll_and_safe_click_loc(driver, wait, OPT_PAYMENT_STATUS_AGUARDANDO, timeout=12)
    time.sleep(0.5)

    scroll_and_safe_click_loc(driver, wait, BTN_FILTER_ACTIVE, timeout=12)
    time.sleep(5)

    scroll_and_safe_click_loc(driver, wait, BTN_CLEAR_FILTER, timeout=12)
    scroll_into_view(driver, GRID_ORDERS_READY, timeout=25)
    time.sleep(2)


def favorites_page(driver, wait):
    safe_click_loc(driver, wait, NAV_LISTA_FAVORITOS, timeout=12)
    time.sleep(1)


def addresses_set_second_as_main(driver, wait):
    safe_click_loc(driver, wait, NAV_ENDERECOS, timeout=12)
    visible(driver, BTN_MAIN_ADDRESS_DEFAULT_2, timeout=25)

    scroll_into_view(driver, SECOND_ADDRESS_BOX, timeout=12)
    safe_click_loc(driver, wait, BTN_MAIN_ADDRESS_DEFAULT_2, timeout=12)

    visible(driver, BTN_ACCEPT_MODAL, timeout=12)
    safe_click_loc(driver, wait, BTN_ACCEPT_MODAL, timeout=12)
    visible(driver, BTN_MAIN_ADDRESS_DEFAULT_2, timeout=25)
    time.sleep(2)


def points_flow(driver, wait):
    safe_click_loc(driver, wait, NAV_MEUS_PONTOS, timeout=12)
    time.sleep(1)

    safe_click_loc(driver, wait, REWARD_ALL, timeout=12); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_EARNINGS, timeout=12); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_USED, timeout=12); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_EXPIRED, timeout=12); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_CANCELED, timeout=12); time.sleep(0.8)

    safe_click_loc(driver, wait, BTN_POINTS_REPORT, timeout=12)
    visible(driver, POINTS_REPORT_FILTER, timeout=25)

    safe_click_loc(driver, wait, POINTS_REPORT_FILTER, timeout=12)
    safe_click_loc(driver, wait, POINTS_REPORT_FILTER_OPT2, timeout=12)

    visible(driver, POINTS_REPORT_FILTER, timeout=25)
    safe_click_loc(driver, wait, LINK_BACK_TO_MISSIONS, timeout=12)
    visible(driver, MISSIONS_READY, timeout=25)


def cadastro_redes_flow(driver, wait):
    safe_click_loc(driver, wait, NAV_CADASTRO_REDES, timeout=12)
    visible(driver, GRID_ASSIGNED_READY, timeout=25)

    safe_click_loc(driver, wait, TAB_AGRUPAR, timeout=12); time.sleep(0.6)
    safe_click_loc(driver, wait, TAB_INFO, timeout=12); time.sleep(0.6)
    safe_click_loc(driver, wait, TAB_REGRAS, timeout=12); time.sleep(0.6)


def cupons_flow(driver, wait):
    safe_click_loc(driver, wait, NAV_MEUS_CUPONS, timeout=12)
    visible(driver, COUPON_FIRST, timeout=25)

    safe_click_loc(driver, wait, COUPON_VER_MAIS_1, timeout=12)
    time.sleep(0.8)

    safe_click_loc(driver, wait, COUPON_COPY_1, timeout=12)
    time.sleep(0.8)

    safe_click_loc(driver, wait, COUPON_VER_MAIS_1, timeout=12)
    time.sleep(0.8)

    safe_click_loc(driver, wait, TAB_UNAVAILABLE, timeout=12)
    time.sleep(0.8)

    # ✅ GARANTIA: ainda estou na página de cupons
    visible(driver, COUPON_FIRST, timeout=10)


def misssoes_flow(driver, wait):
    scroll_and_safe_click_loc(driver, wait, NAV_MINHAS_MISSOES, timeout=12)
    visible(driver, MISSIONS_READY, timeout=25)


# ---------------------------
# INFO DA CONTA: WHATSAPP + EMAIL + SENHA
# ---------------------------
def account_whatsapp_toggle_flow(driver, wait):
    """
    - Entra em 'Informações da conta'
    - Clica em 'Definir como principal'
    - Confirma modal 'Definir'
    - Aguarda mensagem de sucesso
    - Alterna o WhatsApp 2x aguardando loader AJAX sumir
    """

    # entra na página
    scroll_and_safe_click_loc(driver, wait, NAV_INFO_CONTA, timeout=12)
    time.sleep(1)

    # definir como principal
    visible(driver, BTN_DEFINIR_COMO_PRINCIPAL, timeout=15)
    safe_click_loc(driver, wait, BTN_DEFINIR_COMO_PRINCIPAL, timeout=12)

    # confirmar modal
    visible(driver, BTN_MODAL_DEFINIR, timeout=15)
    safe_click_loc(driver, wait, BTN_MODAL_DEFINIR, timeout=12)

    # aguarda sucesso
    visible(driver, ALERT_SUCCESS_PHONE, timeout=20)
    time.sleep(0.6)

    # WhatsApp toggle 2x
    visible(driver, WHATSAPP_SWITCH, timeout=15)

    safe_click_loc(driver, wait, WHATSAPP_SWITCH, timeout=12)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))

    safe_click_loc(driver, wait, WHATSAPP_SWITCH, timeout=12)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))


def account_change_email_flow(driver, wait, new_email, current_password):
    """
    - Entra em 'Informações da conta'
    - Edita e-mail (e confirma)
    - Informa senha atual
    - Salva e valida alerta de sucesso
    """

    scroll_and_safe_click_loc(driver, wait, BTN_EDIT_EMAIL, timeout=12)
    visible(driver, CURRENT_PASSWORD, timeout=12)

    fill_input(driver, wait, CURRENT_EMAIL, new_email, timeout=12)
    fill_input(driver, wait, CONFIRM_EMAIL, new_email, timeout=12)
    fill_input(driver, wait, CURRENT_PASSWORD, current_password, timeout=12)

    scroll_and_safe_click_loc(driver, wait, BTN_SAVE_ACCOUNT_INFO, timeout=12)
    visible(driver, ALERT_SUCCESS, timeout=20)

    # cancelar (volta estado)
    scroll_and_safe_click_loc(driver, wait, BTN_CANCEL_ACCOUNT, timeout=12)
    visible(driver, BTN_EDIT_PASSWORD, timeout=12)


def change_password_flow(driver, wait, current_password, new_password):
    scroll_and_safe_click_loc(driver, wait, BTN_EDIT_PASSWORD, timeout=12)
    visible(driver, CURRENT_PASSWORD, timeout=12)

    fill_input(driver, wait, CURRENT_PASSWORD, current_password, timeout=12)
    fill_input(driver, wait, NEW_PASSWORD, new_password, timeout=12)
    fill_input(driver, wait, CONFIRM_NEW_PASSWORD, new_password, timeout=12)

    scroll_and_safe_click_loc(driver, wait, BTN_SAVE_ACCOUNT_INFO, timeout=12)
    visible(driver, ALERT_SUCCESS, timeout=20)
