import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.checkout import *
from helpers.actions import click_when_clickable, scroll_to_middle, mobile_click_strict


def avancar_shipping(driver, wait):
    """Aguarda shipping, fecha cupons e avanca."""
    wait.until(EC.element_to_be_clickable(BTN_CONTINUAR_SHIPPING))
    time.sleep(5)
    click_when_clickable(wait, CUPONS_EXPANDED)
    wait.until(EC.presence_of_element_located(CUPONS_COLLAPSED))
    click_when_clickable(wait, BTN_CONTINUAR_SHIPPING)

def selecionar_boleto_e_finalizar(driver, wait, condicao_locator):
    """Seleciona Boleto, condicao, aceita termos e finaliza."""

    wait.until(EC.presence_of_element_located(BODY_AJAX_LOADING))
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))
    time.sleep(3)

    # Seleciona Boleto
    click_when_clickable(wait, BOLETO)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))
    time.sleep(3)

    # Define qual botão de finalizar usar
    try:
        wait.until(EC.presence_of_element_located(BTN_FINALIZAR_COMPRA_BOLETO))
        btn_finalizar = BTN_FINALIZAR_COMPRA_BOLETO
    except TimeoutException:
        btn_finalizar = BTN_FINALIZAR_COMPRA_BOLETO_SUL

    # Scroll ate Finalizar
    scroll_to_middle(driver, wait, btn_finalizar)

    # Seleciona condicao
    click_when_clickable(wait, BOLETO_SELECT)

    wait.until(EC.element_to_be_clickable(condicao_locator))
    click_when_clickable(wait, condicao_locator)

    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))
    time.sleep(3)

    # Aceita termos
    click_when_clickable(wait, TERMS_BOLETO)

    # Finaliza compra
    click_when_clickable(wait, btn_finalizar)

    # Aguarda pagina de sucesso
    wait.until(EC.url_contains("success"))

def ir_para_home(driver, wait):
    """Clica Ir Para Home, aguarda e refresh."""
    click_when_clickable(wait, BTN_IR_PARA_HOME)
    time.sleep(5)
    driver.refresh()
    time.sleep(3)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def select_pix_payment(driver, timeout=20):
    """
    O que faz:
    - Garante que o método de pagamento PIX fique selecionado.
    - Clica preferencialmente no LABEL (área maior e mais estável no iOS Safari).
    - Faz scroll para o elemento antes de clicar.
    - Confirma que o radio ficou checked.
    """
    wait = WebDriverWait(driver, timeout)

    # 1) Espera a seção de pagamento existir
    wait.until(EC.presence_of_element_located((By.ID, "checkout-payment-method-load")))

    # 2) Primeiro tenta pelo LABEL (mais clicável)
    label = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='dux_pay_pix']")))

    # scroll pro centro
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)

    # tenta clique normal
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='dux_pay_pix']"))).click()
    except Exception:
        # fallback: clique via JS
        driver.execute_script("arguments[0].click();", label)

    # 3) Confirma que o input ficou checked
    wait.until(lambda d: d.find_element(By.ID, "dux_pay_pix").is_selected())

def avancar_shipping_mobile(driver, wait):
    """Aguarda shipping, abre e fecha o Resumo do pedido."""
    wait.until(EC.element_to_be_clickable(MOBILE_BTN_CONTINUAR_SHIPPING))

    mobile_click_strict(driver, MOBILE_OPEN_SUMARY, 10, 4, 0.25)
    wait.until(EC.presence_of_element_located(MOBILE_CLOSE_SUMARY))
    time.sleep(3)
    mobile_click_strict(driver, MOBILE_CLOSE_SUMARY, 10, 4, 0.25)

    mobile_click_strict(driver, MOBILE_BTN_CONTINUAR_SHIPPING, 10, 4, 0.25)

def selecionar_boleto_e_finalizar_mobile(driver, wait, condicao_locator):
    """Seleciona Boleto, condicao, aceita termos e finaliza."""

    time.sleep(3)

    # Seleciona Boleto
    mobile_click_strict(driver, BOLETO, 10, 4, 0.25)
    time.sleep(3)

    # Seleciona condicao
    mobile_click_strict(driver, BOLETO_SELECT, 10, 4, 0.25)

    wait.until(EC.element_to_be_clickable(condicao_locator))
    mobile_click_strict(driver, condicao_locator, 10, 4, 0.25)

    time.sleep(3)

    # Aceita termos
    mobile_click_strict(driver, TERMS_BOLETO, 10, 4, 0.25)

    # Finaliza compra
    mobile_click_strict(driver, BTN_FINALIZAR_COMPRA_BOLETO, 10, 4, 0.25)

    # Aguarda pagina de sucesso
    wait.until(EC.presence_of_element_located(SUCCESS_PAGE_BODY))
