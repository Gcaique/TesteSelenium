from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from locators.redefinir_senha import *


# =========================
# Logout
# =========================

BTN_LOGOUT = (By.XPATH, "//a[contains(@href,'logout')]")

def ensure_logged_out(driver):
    """
    Garante que o usuário está deslogado.
    Se botão de logout existir → clica.
    Se não existir → já está deslogado.
    """
    try:
        driver.find_element(*BTN_LOGOUT).click()
    except:
        pass


# =========================
# Navegação
# =========================

def abrir_login(driver, wait):
    wait.until(EC.element_to_be_clickable(BTN_LOGIN_HEADER)).click()


def clicar_esqueci_senha(driver, wait):
    wait.until(EC.element_to_be_clickable(LINK_ESQUECI_SENHA)).click()


# =========================
# Ações
# =========================

def preencher_email(driver, wait, email):
    campo = wait.until(EC.visibility_of_element_located(INPUT_EMAIL))
    campo.clear()
    campo.send_keys(email)


def clicar_enviar(driver, wait):
    wait.until(EC.element_to_be_clickable(BTN_ENVIAR)).click()


# =========================
# Validação
# =========================

def mensagem_sucesso_visivel(driver, wait):
    try:
        wait.until(EC.visibility_of_element_located(MSG_SUCESSO))
        return True
    except:
        return False


# =========================
# Fluxo completo
# =========================

def fluxo_completo_redefinir_senha(driver, wait, email):
    ensure_logged_out(driver)
    abrir_login(driver, wait)
    clicar_esqueci_senha(driver, wait)
    preencher_email(driver, wait, email)
    clicar_enviar(driver, wait)