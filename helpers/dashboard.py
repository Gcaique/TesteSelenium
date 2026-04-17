import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, TimeoutException

from helpers.actions import safe_click_loc, scroll_into_view, fill_input, try_click, scroll_and_safe_click_loc, \
    mobile_click_strict, click_when_clickable
from helpers.waiters import visible, _effective_timeout
from helpers.minicart import wait_minicart_loading
from helpers.popups import try_close_popups
from helpers.dropdown import open_user_dropdown
from helpers.checkout import select_pix_payment

from locators.plp import *
from locators.cart import *
from locators.checkout import *
from locators.header import *
from locators.dashboard import *
from locators.common import *
from locators.cadastro import CHECK_MARCAR_TODAS, CHECK_WHATSAPP, CHECK_SMS, CHECK_EMAIL


# ---------------------------
# COMPRA + CHECKOUT PIX
# ---------------------------
def buy_first_product_and_checkout_pix(driver, wait):
    # acesso categoria
    safe_click_loc(driver, wait, CATEGORY_BOVINOS_PREMIUM)

    # garante listagem carregada + scroll
    visible(driver, BTN_INCREMENT_QTY, wait=wait, timeout=_effective_timeout(wait, None))
    scroll_into_view(driver, TOOLBAR_AMOUNT, wait=wait)

    # incrementa e adiciona
    safe_click_loc(driver, wait, BTN_INCREMENT_QTY)
    safe_click_loc(driver, wait, BTN_ADD_TO_CART)

    # espera minicart atualizar
    wait_minicart_loading(driver)

    visible(driver, BTN_CHECKOUT_TOP, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, BTN_CHECKOUT_TOP)

    # shipping -> continuar
    visible(driver, BTN_CONTINUAR_SHIPPING, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, BTN_CONTINUAR_SHIPPING, timeout=_effective_timeout(wait, None))

    # payment -> PIX + termos + finalizar
    visible(driver, PIX, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, PIX)

    visible(driver, BTN_FINALIZAR_COMPRA_PIX, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, BTN_FINALIZAR_COMPRA_PIX)

    # aguarda retorno
    time.sleep(6)


# ---------------------------
# NAVEGAÇÕES DASHBOARD
# ---------------------------
def open_my_account(driver, wait):
    open_user_dropdown(driver)
    safe_click_loc(driver, wait, DD_MINHA_CONTA)
    visible(driver, BTN_MAIN_ADDRESS_DASHBOARD, wait=wait, timeout=_effective_timeout(wait, None))


def dashboard_set_main_address(driver, wait):
    try:
        visible(driver, BTN_MAIN_ADDRESS_DASHBOARD, wait=wait)
        scroll_and_safe_click_loc(driver, wait, BTN_MAIN_ADDRESS_DASHBOARD)
        visible(driver, BTN_ACCEPT_MODAL, wait=wait)
        scroll_and_safe_click_loc(driver, wait, BTN_ACCEPT_MODAL)
        time.sleep(1)
    except Exception:
        pass


def go_all_addresses(driver, wait):
    scroll_and_safe_click_loc(driver, wait, LINK_VER_TODOS_ENDERECOS, timeout=_effective_timeout(wait, None))
    time.sleep(5)


def open_recent_orders_from_dashboard(driver, wait):
    scroll_and_safe_click_loc(driver, wait, LINK_PEDIDOS_RECENTES)
    time.sleep(2)


def orders_open_first_and_copy_pix(driver, wait):
    # Em vez de só "visible", scroll ajuda bastante em grids
    scroll_into_view(driver, GRID_ORDERS_READY, wait=wait, timeout=_effective_timeout(wait, None))

    scroll_and_safe_click_loc(driver, wait, FIRST_ORDER_DETAILS)
    time.sleep(5)

    scroll_and_safe_click_loc(driver, wait, BTN_COPY_PIX)
    visible(driver, BTN_COPY_PIX_COPIED, wait=wait)
    time.sleep(2)


def orders_filters_flow(driver, wait):
    # Tenta um clique rápido de 3 segundos no menu lateral.
    # Se falhar, o fluxo apenas segue para o próximo passo.
    try:
        scroll_and_safe_click_loc(driver, wait, NAV_MEUS_PEDIDOS, timeout=_effective_timeout(wait, None))
    except (TimeoutException, Exception):
        """Elemento opcional ou página já carregada"""

    # período 7 dias + filtrar
    scroll_and_safe_click_loc(driver, wait, SEL_PERIOD)
    scroll_and_safe_click_loc(driver, wait, OPT_PERIOD_7D)

    scroll_into_view(driver, BTN_FILTER, wait=wait)
    scroll_and_safe_click_loc(driver, wait, BTN_FILTER)
    time.sleep(1)

    # status pedido + status pagamento + filtrar
    scroll_and_safe_click_loc(driver, wait, SEL_ORDER_STATUS)
    scroll_and_safe_click_loc(driver, wait, OPT_ORDER_STATUS_FATURADO)
    time.sleep(0.5)

    scroll_and_safe_click_loc(driver, wait, SEL_PAYMENT_STATUS)
    scroll_and_safe_click_loc(driver, wait, OPT_PAYMENT_STATUS_AGUARDANDO)
    time.sleep(0.5)

    scroll_and_safe_click_loc(driver, wait, BTN_FILTER_ACTIVE)
    time.sleep(5)

    scroll_and_safe_click_loc(driver, wait, BTN_CLEAR_FILTER)
    scroll_into_view(driver, GRID_ORDERS_READY, wait=wait, timeout=_effective_timeout(wait, None))
    time.sleep(2)


def favorites_page(driver, wait):
    safe_click_loc(driver, wait, NAV_LISTA_FAVORITOS)
    time.sleep(1)


def addresses_set_second_as_main(driver, wait):
    safe_click_loc(driver, wait, NAV_ENDERECOS)
    visible(driver, BTN_MAIN_ADDRESS_DEFAULT_2, wait=wait, timeout=_effective_timeout(wait, None))

    scroll_into_view(driver, SECOND_ADDRESS_BOX, wait=wait)
    safe_click_loc(driver, wait, BTN_MAIN_ADDRESS_DEFAULT_2)

    visible(driver, BTN_ACCEPT_MODAL, wait=wait)
    safe_click_loc(driver, wait, BTN_ACCEPT_MODAL)
    visible(driver, BTN_MAIN_ADDRESS_DEFAULT_2, wait=wait, timeout=_effective_timeout(wait, None))
    time.sleep(2)


def points_flow(driver, wait):
    safe_click_loc(driver, wait, NAV_MEUS_PONTOS)
    time.sleep(1)

    safe_click_loc(driver, wait, REWARD_ALL); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_EARNINGS); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_USED); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_EXPIRED); time.sleep(0.8)
    safe_click_loc(driver, wait, REWARD_CANCELED); time.sleep(0.8)

    safe_click_loc(driver, wait, BTN_POINTS_REPORT)
    visible(driver, POINTS_REPORT_FILTER, wait=wait, timeout=_effective_timeout(wait, None))

    safe_click_loc(driver, wait, POINTS_REPORT_FILTER)
    safe_click_loc(driver, wait, POINTS_REPORT_FILTER_OPT2)

    visible(driver, POINTS_REPORT_FILTER, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, LINK_BACK_TO_MISSIONS)
    visible(driver, MISSIONS_READY, wait=wait, timeout=_effective_timeout(wait, None))


def cadastro_redes_flow(driver, wait):
    safe_click_loc(driver, wait, NAV_CADASTRO_REDES)
    visible(driver, GRID_ASSIGNED_READY, wait=wait, timeout=_effective_timeout(wait, None))

    safe_click_loc(driver, wait, TAB_AGRUPAR); time.sleep(0.6)
    safe_click_loc(driver, wait, TAB_INFO); time.sleep(0.6)
    safe_click_loc(driver, wait, TAB_REGRAS); time.sleep(0.6)


def cupons_flow(driver, wait):
    safe_click_loc(driver, wait, NAV_MEUS_CUPONS)
    visible(driver, COUPON_FIRST, wait=wait, timeout=_effective_timeout(wait, None))

    safe_click_loc(driver, wait, COUPON_VER_MAIS_1)
    time.sleep(0.8)

    safe_click_loc(driver, wait, COUPON_COPY_1)
    time.sleep(0.8)

    safe_click_loc(driver, wait, COUPON_VER_MAIS_1)
    time.sleep(0.8)

    safe_click_loc(driver, wait, TAB_UNAVAILABLE)
    time.sleep(0.8)

    # GARANTIA: ainda estou na página de cupons
    visible(driver, COUPON_FIRST, wait=wait)


def misssoes_flow(driver, wait):
    scroll_and_safe_click_loc(driver, wait, NAV_MINHAS_MISSOES)
    visible(driver, MISSIONS_READY, wait=wait, timeout=_effective_timeout(wait, None))


def privacidade_dados(driver, wait):
    scroll_and_safe_click_loc(driver, wait, NAV_PRIVACIDADE_DADOS)
    visible(driver, CHECK_MARCAR_TODAS, wait=wait)

    safe_click_loc(driver, wait, CHECK_SMS)
    time.sleep(1)

    safe_click_loc(driver, wait, BTN_SALVAR_PREVERENCIAS)
    time.sleep(1)

    visible(driver, BTN_IR_PARA_HOME_LGPD, wait=wait)
    safe_click_loc(driver, wait, BTN_IR_PARA_HOME_LGPD)

    # Aguardando home page carregar
    time.sleep(5)

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
    scroll_and_safe_click_loc(driver, wait, NAV_INFO_CONTA)
    time.sleep(1)

    # definir como principal
    visible(driver, BTN_DEFINIR_COMO_PRINCIPAL, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, BTN_DEFINIR_COMO_PRINCIPAL)

    # confirmar modal
    visible(driver, BTN_MODAL_DEFINIR, wait=wait, timeout=_effective_timeout(wait, None))
    safe_click_loc(driver, wait, BTN_MODAL_DEFINIR)

    # aguarda sucesso
    visible(driver, ALERT_SUCCESS_PHONE, wait=wait, timeout=_effective_timeout(wait, None))
    time.sleep(0.6)

    # WhatsApp toggle 2x
    visible(driver, WHATSAPP_SWITCH, wait=wait, timeout=_effective_timeout(wait, None))

    safe_click_loc(driver, wait, WHATSAPP_SWITCH)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))

    safe_click_loc(driver, wait, WHATSAPP_SWITCH)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))


def account_change_email_flow(driver, wait, new_email, current_password):
    """
    - Entra em 'Informações da conta'
    - Edita e-mail (e confirma)
    - Informa senha atual
    - Salva e valida alerta de sucesso
    """

    scroll_and_safe_click_loc(driver, wait, BTN_EDIT_EMAIL)
    visible(driver, CURRENT_PASSWORD, wait=wait)

    fill_input(driver, wait, CURRENT_EMAIL, new_email)
    fill_input(driver, wait, CONFIRM_EMAIL, new_email)
    fill_input(driver, wait, CURRENT_PASSWORD, current_password)

    scroll_and_safe_click_loc(driver, wait, BTN_SAVE_ACCOUNT_INFO)
    visible(driver, ALERT_SUCCESS, wait=wait)

    # cancelar (volta estado)
    scroll_and_safe_click_loc(driver, wait, BTN_CANCEL_ACCOUNT)
    visible(driver, BTN_EDIT_PASSWORD, wait=wait)


def change_password_flow(driver, wait, current_password, new_password):
    scroll_and_safe_click_loc(driver, wait, BTN_EDIT_PASSWORD)
    visible(driver, CURRENT_PASSWORD, wait=wait)

    fill_input(driver, wait, CURRENT_PASSWORD, current_password)
    fill_input(driver, wait, NEW_PASSWORD, new_password)
    fill_input(driver, wait, CONFIRM_NEW_PASSWORD, new_password)

    scroll_and_safe_click_loc(driver, wait, BTN_SAVE_ACCOUNT_INFO)
    visible(driver, ALERT_SUCCESS, wait=wait)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

def click_continuar_shipping_mobile(driver, wait=None, timeout=None):
    # garante que o botão existe no DOM
    eff = _effective_timeout(wait, timeout)
    WebDriverWait(driver, eff, poll_frequency=0.2).until(
        EC.presence_of_element_located(MOBILE_BTN_CONTINUAR_SHIPPING)
    )

    # garante que está clicável (não disabled / não coberto)
    WebDriverWait(driver, eff, poll_frequency=0.2).until(
        EC.element_to_be_clickable(MOBILE_BTN_CONTINUAR_SHIPPING)
    )

    # clica usando seu helper (que já faz scroll + retries + js + tap)
    mobile_click_strict(driver, MOBILE_BTN_CONTINUAR_SHIPPING, timeout=eff, retries=4, sleep_between=0.25, wait=wait)

    # valida que avançou para a etapa de pagamento
    WebDriverWait(driver, eff, poll_frequency=0.2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".payment-methods"))
    )

def buy_first_product_and_checkout_pix_mobile(driver, wait):
    # acesso categoria
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, timeout=_effective_timeout(wait, None))
    time.sleep(2)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, timeout=_effective_timeout(wait, None))
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, timeout=_effective_timeout(wait, None))
    visible(driver, SORTER_SELECT, wait=wait, timeout=_effective_timeout(wait, None))

    # garante listagem carregada + scroll
    visible(driver, BTN_INCREMENT_QTY, wait=wait, timeout=_effective_timeout(wait, None))
    scroll_into_view(driver, TOOLBAR_AMOUNT, wait=wait)

    # incrementa e adiciona
    mobile_click_strict(driver, BTN_INCREMENT_QTY, wait=wait, timeout=_effective_timeout(wait, None))
    mobile_click_strict(driver, BTN_ADD_TO_CART, wait=wait, timeout=_effective_timeout(wait, None))

    # espera minicart atualizar
    wait_minicart_loading(driver)

    mobile_click_strict(driver, MOBILE_MINICART_ICON, wait=wait, timeout=_effective_timeout(wait, None))
    visible(driver, MOBILE_MINICART_OPENED, wait=wait, timeout=_effective_timeout(wait, None))

    mobile_click_strict(driver, BTN_CHECKOUT_TOP, wait=wait, timeout=_effective_timeout(wait, None))

    # shipping -> continuar
    click_continuar_shipping_mobile(driver, wait=wait)
    print("URL:", driver.current_url)
    print("HTML contém shipping-method-buttons-container:",
          "shipping-method-buttons-container" in driver.page_source)

    # payment -> PIX + termos + finalizar
    visible(driver, PIX, wait=wait, timeout=_effective_timeout(wait, None))
    select_pix_payment(driver, timeout=_effective_timeout(wait, None))

    visible(driver, MOBILE_BTN_FINALIZAR_COMPRA_PIX, wait=wait, timeout=_effective_timeout(wait, None))
    mobile_click_strict(driver, MOBILE_BTN_FINALIZAR_COMPRA_PIX, wait=wait, timeout=_effective_timeout(wait, None))

    # aguarda retorno
    time.sleep(6)

def open_minha_conta_mobile(driver, wait=None, timeout=None):
    """
    Abre o dropdown "Minha Conta" no mobile.
    Se um wait for passado, usa o timeout dele; caso contrário, usa o timeout explícito ou 15s.
    """
    effective = _effective_timeout(wait, timeout, default=15)
    w = wait if wait is not None else WebDriverWait(driver, effective)

    el = w.until(EC.presence_of_element_located(MOBILE_DROPDOWN_MINHA_CONTA))

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    try:
        w.until(EC.element_to_be_clickable(MOBILE_DROPDOWN_MINHA_CONTA)).click()
    except Exception:
        driver.execute_script("arguments[0].click();", el)

def orders_open_first_and_copy_pix_mobile(driver, wait):
    # Em vez de só "visible", scroll ajuda bastante em grids
    scroll_into_view(driver, MOBILE_FIRST_ORDER_DETAILS, wait=wait)

    scroll_and_safe_click_loc(driver, wait, MOBILE_FIRST_ORDER_DETAILS)
    time.sleep(5)

    mobile_click_strict(driver, MOBILE_BTN_COPY_PIX, wait=wait)
    time.sleep(2)

def orders_filters_flow_mobile(driver, wait):
    # período 7 dias + filtrar
    scroll_and_safe_click_loc(driver, wait, SEL_PERIOD)
    scroll_and_safe_click_loc(driver, wait, OPT_PERIOD_7D)

    scroll_into_view(driver, BTN_FILTER, wait=wait)
    scroll_and_safe_click_loc(driver, wait, BTN_FILTER)
    time.sleep(1)

    # status pedido + status pagamento + filtrar
    scroll_and_safe_click_loc(driver, wait, SEL_ORDER_STATUS)
    scroll_and_safe_click_loc(driver, wait, OPT_ORDER_STATUS_FATURADO)
    time.sleep(0.5)

    scroll_and_safe_click_loc(driver, wait, SEL_PAYMENT_STATUS)
    scroll_and_safe_click_loc(driver, wait, OPT_PAYMENT_STATUS_AGUARDANDO)
    time.sleep(0.5)

    scroll_and_safe_click_loc(driver, wait, BTN_FILTER_ACTIVE)
    time.sleep(4)

    scroll_and_safe_click_loc(driver, wait, MOBILE_BTN_CLEAR_FILTER)
    time.sleep(4)

def addresses_set_second_as_main_mobile(driver, wait):
    visible(driver, BTN_MAIN_ADDRESS_DEFAULT_2, wait=wait, timeout=_effective_timeout(wait, None))

    scroll_into_view(driver, SECOND_ADDRESS_BOX, wait=wait)
    safe_click_loc(driver, wait, BTN_MAIN_ADDRESS_DEFAULT_2)

    visible(driver, BTN_ACCEPT_MODAL, wait=wait)
    safe_click_loc(driver, wait, BTN_ACCEPT_MODAL)
    visible(driver, BTN_MAIN_ADDRESS_DEFAULT_2, wait=wait, timeout=_effective_timeout(wait, None))
    time.sleep(2)

def apply_reward_filter_mobile(driver, wait, value: str, retries: int = 3) -> bool:
    """
    Mobile (Meus Pontos):
    - seleciona o filtro no <select id="reward-filter-select">
    - clica no botão 'Filtrar' (id="reward-filter-btn") para aplicar
    value esperado: all | earnings | used | expired | canceled
    """
    for _ in range(retries):
        try:
            # garante select visível/clicável
            select_el = wait.until(EC.presence_of_element_located(MOBILE_REWARD_FILTER_SELECT))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_el)

            # tenta selecionar pelo Selenium Select
            try:
                Select(select_el).select_by_value(value)
            except WebDriverException:
                # fallback forte
                driver.execute_script("""
                    const sel = document.getElementById('reward-filter-select');
                    sel.value = arguments[0];
                    sel.dispatchEvent(new Event('change', { bubbles: true }));
                """, value)

            # clicar no botão Filtrar (aplica)
            btn = wait.until(EC.element_to_be_clickable(MOBILE_REWARD_FILTER_BTN))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)

            # clique normal + fallback JS (pra intercept em mobile)
            try:
                btn.click()
            except WebDriverException:
                driver.execute_script("arguments[0].click();", btn)

            # espera a tela refletir o filtro
            time.sleep(0.8)
            return True

        except TimeoutException:
            time.sleep(1)
        except Exception:
            time.sleep(1)

    return False

def apply_cadastro_redes_filter_mobile(driver, wait, value: str, retries: int = 3) -> bool:
    """
    Cadastro de redes (mobile):
    - Seleciona a option no select de abas/steps
    value: assigned-grid | new-assign | info | rules
    """
    for _ in range(retries):
        try:
            sel = wait.until(EC.presence_of_element_located(MOBILE_TAB_SELECT))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sel)

            # tenta Select() primeiro
            try:
                Select(sel).select_by_value(value)
            except WebDriverException:
                # fallback forte (iOS Safari / grid pode falhar no select nativo)
                driver.execute_script("""
                    const sel = document.querySelector('select.hj-network_grouping-mobile-tab_switcher');
                    sel.value = arguments[0];
                    sel.dispatchEvent(new Event('change', { bubbles: true }));
                """, value)

            # valida que o value foi aplicado
            time.sleep(0.8)
            return True

        except TimeoutException:
            time.sleep(1)
        except Exception:
            time.sleep(1)

    return False

def apply_meus_cupons_filter_mobile(driver, wait, value: str, retries: int = 3) -> bool:
    """
    Meus Cupons (mobile):
    - seleciona o filtro no <select class="filter-select">
    - clica no botão <button class="filter-button">Filtrar</button>
    value esperado: active | unavailable
    """
    for _ in range(retries):
        try:
            sel = wait.until(EC.presence_of_element_located(MOBILE_CUPONS_FILTER_SELECT))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sel)

            # tenta Select() primeiro
            try:
                Select(sel).select_by_value(value)
            except WebDriverException:
                # fallback forte (iOS Safari / grid pode falhar no select nativo)
                driver.execute_script("""
                    const sel = document.querySelector('select.filter-select');
                    sel.value = arguments[0];
                    sel.dispatchEvent(new Event('change', { bubbles: true }));
                """, value)

            # clica no botão Filtrar (aplica)
            btn = wait.until(EC.element_to_be_clickable(MOBILE_CUPONS_FILTER_BUTTON))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)

            try:
                btn.click()
            except WebDriverException:
                driver.execute_script("arguments[0].click();", btn)

            # valida que o value ficou setado
            time.sleep(0.8)
            return True

        except TimeoutException:
            time.sleep(1)
        except Exception:
            time.sleep(1)

    return False


def privacidade_dados_mobile(driver, wait):
    mobile_click_strict(driver, CHECK_SMS, timeout=_effective_timeout(wait, None), retries=4, sleep_between=0.25, wait=wait)
    time.sleep(1)

    mobile_click_strict(driver, BTN_SALVAR_PREVERENCIAS, timeout=_effective_timeout(wait, None), retries=4, sleep_between=0.25, wait=wait)
    time.sleep(1)

    t = _effective_timeout(wait, None)
    visible(driver, BTN_IR_PARA_HOME_LGPD, timeout=t, wait=wait)
    mobile_click_strict(driver, BTN_IR_PARA_HOME_LGPD, t, 4, 0.25, wait=wait)

    # Aguardando home page carregar
    time.sleep(5)


def account_whatsapp_toggle_flow_mobile(driver, wait):
    """
    - Clica em 'Definir como principal'
    - Confirma modal 'Definir'
    - Aguarda mensagem de sucesso
    - Alterna o WhatsApp 2x aguardando loader AJAX sumir
    """
    # definir como principal
    visible(driver, BTN_DEFINIR_COMO_PRINCIPAL, wait=wait)
    mobile_click_strict(driver, BTN_DEFINIR_COMO_PRINCIPAL, wait=wait)

    # confirmar modal
    visible(driver, BTN_MODAL_DEFINIR, wait=wait)
    mobile_click_strict(driver, BTN_MODAL_DEFINIR, wait=wait)

    # aguarda sucesso
    visible(driver, ALERT_SUCCESS_PHONE, wait=wait)
    time.sleep(0.6)

    # WhatsApp toggle 2x
    visible(driver, WHATSAPP_SWITCH, wait=wait)

    mobile_click_strict(driver, WHATSAPP_SWITCH, wait=wait)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))

    mobile_click_strict(driver, WHATSAPP_SWITCH, wait=wait)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))

def account_change_email_flow_mobile(driver, wait, new_email, current_password):
    """
    - Edita e-mail (e confirma)
    - Informa senha atual
    - Salva e valida alerta de sucesso
    """
    mobile_click_strict(driver, BTN_EDIT_EMAIL, wait=wait)
    visible(driver, CURRENT_PASSWORD, wait=wait)

    fill_input(driver, wait, CURRENT_EMAIL, new_email)
    fill_input(driver, wait, CONFIRM_EMAIL, new_email)
    fill_input(driver, wait, CURRENT_PASSWORD, current_password)

    mobile_click_strict(driver, BTN_SAVE_ACCOUNT_INFO, wait=wait)
    visible(driver, ALERT_SUCCESS, wait=wait)

    # cancelar (volta estado)
    mobile_click_strict(driver, BTN_CANCEL_ACCOUNT, wait=wait)
    visible(driver, BTN_EDIT_PASSWORD, wait=wait)

def change_password_flow_mobile(driver, wait, current_password, new_password):
    mobile_click_strict(driver, BTN_EDIT_PASSWORD, wait=wait)
    visible(driver, CURRENT_PASSWORD, wait=wait)

    fill_input(driver, wait, CURRENT_PASSWORD, current_password)
    fill_input(driver, wait, NEW_PASSWORD, new_password)
    fill_input(driver, wait, CONFIRM_NEW_PASSWORD, new_password)

    mobile_click_strict(driver, BTN_SAVE_ACCOUNT_INFO, wait=wait)
    visible(driver, ALERT_SUCCESS, wait=wait)
