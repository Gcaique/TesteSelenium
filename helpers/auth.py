import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from helpers.waiters import *
from helpers.actions import *
from helpers.popups import *
from helpers.minicart import minicart_visible

from locators.header import *



def ensure_logged_in(driver, user: str, passwd: str):
    """Garante login (idempotente)"""

    if minicart_visible(driver):
        try_close_popups(driver)
        return

    # abre login
    click(driver, LOGIN_MENU, timeout=10)
    visible(driver, USERNAME_INPUT, timeout=10)

    # username
    fill(driver, USERNAME_INPUT, user)
    click(driver, BTN_AVANCAR, timeout=10)

    # senha
    visible(driver, PASSWORD_INPUT, timeout=10)
    fill(driver, PASSWORD_INPUT, passwd)
    click(driver, BTN_AVANCAR, timeout=10)

    # confirmação via minicart
    end = time.time() + 60

    while time.time() < end:
        if minicart_visible(driver):
            try_close_popups(driver)
            return
        time.sleep(0.5)

    # fallback LT
    driver.refresh()
    time.sleep(3)
    try_close_popups(driver)

    if minicart_visible(driver):
        return

    raise TimeoutException("Login não confirmou: mini-cart não ficou visível.")


def expect_login_popup(driver, wait, label="login_popup", timeout=12, retries=2, sleep_between=0.6):
    """
    Confirma que o pop-up de login do header abriu.
    Critério: aparecer USERNAME_INPUT ou BTN_AVANCAR (depende do estado do modal).
    Faz pequenas tentativas antes de falhar.
    """
    last_exc = None

    for attempt in range(retries + 1):
        try:
            end = time.time() + timeout
            while time.time() < end:
                # qualquer um dos dois já prova que o popup abriu
                if driver.find_elements(*USERNAME_INPUT) or driver.find_elements(*BTN_AVANCAR):
                    # garante visibilidade real
                    if driver.find_elements(*USERNAME_INPUT):
                        wait.until(EC.visibility_of_element_located(USERNAME_INPUT))
                    else:
                        wait.until(EC.visibility_of_element_located(BTN_AVANCAR))
                    return True

                time.sleep(0.2)

            raise TimeoutException("Popup não apareceu dentro do timeout.")
        except (TimeoutException, StaleElementReferenceException) as e:
            last_exc = e
            time.sleep(sleep_between)

    raise last_exc


def open_login(driver):
    """Abre o modal de login e garante que o campo username apareceu."""
    click(driver, LOGIN_MENU, timeout=10)
    visible(driver, USERNAME_INPUT, timeout=10)


def click_avancar(driver):
    """Clica no botão Avançar do modal."""
    click(driver, BTN_AVANCAR, timeout=10)


def read_error(driver) -> str:
    """Lê o texto do erro Magento (caixa vermelha). Retorna '' se não houver."""
    try:
        el = visible(driver, ERROR_LOGIN_MESSAGE , timeout=1.5)
        return (el.text or "").strip()
    except Exception:
        return ""


def native_validation(driver, locator) -> str:
    """Lê mensagem nativa do navegador. Retorna '' se não houver."""
    try:
        el = driver.find_element(*locator)
        msg = driver.execute_script("return arguments[0].validationMessage;", el)
        return (msg or "").strip()
    except Exception:
        return ""


def wait_username_result(driver, timeout=3):
    """
    Após clicar Avançar na etapa USERNAME, detecta o estado:
    - password -> campo de senha abriu
    - error    -> erro Magento apareceu
    - native   -> validação nativa do browser apareceu
    - none     -> site não reagiu dentro do timeout
    """
    end = time.time() + timeout
    while time.time() < end:
        # Senha abriu?
        try:
            pw = driver.find_elements(*PASSWORD_INPUT)
            if pw and pw[0].is_displayed():
                return "password", ""
        except Exception:
            pass

        # Erro Magento?
        err = read_error(driver)
        if err:
            return "error", err

        # Validação nativa?
        nat = native_validation(driver, USERNAME_INPUT)
        if nat:
            return "native", nat

        time.sleep(0.1)

    return "none", ""


def wait_password_result(driver, timeout=10):
    """
    Após clicar Avançar na etapa SENHA, detecta o estado:
    - success  -> mini-cart apareceu (logou)
    - error    -> erro Magento apareceu
    - password -> continuou no campo senha sem erro até o timeout
    """
    end = time.time() + timeout
    while time.time() < end:
        if minicart_visible(driver):
            return "success", ""

        err = read_error(driver)
        if err:
            return "error", err

        time.sleep(0.1)

    if minicart_visible(driver):
        return "success", ""
    err = read_error(driver)
    if err:
        return "error", err
    return "password", ""


def submit_username_invalid(driver, username, context, tokens=None):
    """
    Envia username inválido e garante que NÃO abre senha.
    Se houver msg (Magento/nativa), valida tokens se informado.
    """
    fill(driver, USERNAME_INPUT, username)
    click_avancar(driver)

    kind, msg = wait_username_result(driver, timeout=2.5)

    assert kind != "password", f"[{context}] Não era para abrir senha, mas abriu."

    if tokens and msg:
        low = msg.lower()
        assert any(t.lower() in low for t in tokens), f"[{context}] msg inesperada: '{msg}'"


def submit_username_valid(driver, username, context):
    """Envia username válido e exige que o campo de senha apareça."""
    fill(driver, USERNAME_INPUT, username)
    click_avancar(driver)

    kind, msg = wait_username_result(driver, timeout=8)
    assert kind == "password", f"[{context}] Era para abrir senha, veio: {kind} / '{msg}'"


def login_password(driver, password, context, expect_success: bool):
    """
    Submete senha:
    - expect_success=True  -> exige login (mini-cart visível)
    - expect_success=False -> exige erro de senha (Magento)
    """
    fill(driver, PASSWORD_INPUT, password)
    click_avancar(driver)

    kind, msg = wait_password_result(driver, timeout=12 if expect_success else 8)

    if expect_success:
        assert kind == "success", f"[{context}] Era para LOGAR, veio: {kind} / '{msg}'"
        return

    # Caso inválido: deve dar erro
    if kind == "error":
        return

    # fallback: erro pode aparecer até ~2s depois, ainda no campo senha
    end = time.time() + 2.0
    while time.time() < end:
        err = read_error(driver)
        if err:
            return
        time.sleep(0.1)

    raise AssertionError(f"[{context}] Era para dar erro de senha inválida, veio: {kind} / '{msg}'")


def logout(driver):
    """Faz logout e espera mini-cart sumir."""
    click(driver, LOGIN_NAME_CONTAINER, timeout=10)
    time.sleep(1)
    click(driver, BTN_LOGOUT, timeout=10)

    end = time.time() + 15
    while time.time() < end:
        if not minicart_visible(driver):
            return
        time.sleep(0.1)

    assert_logged_out(driver, "logout")


def login_expect_email_not_found(driver, wait, email):
    safe_click_loc(driver, wait, LOGIN_MENU, timeout=12)
    fill_input(driver, wait, USERNAME_INPUT, email, timeout=12)
    safe_click_loc(driver, wait, BTN_AVANCAR, timeout=12)
    visible(driver, ERROR_EMAIL_NOT_FOUND, timeout=12)

def login_expect_wrong_password(driver, wait, email, wrong_password):
    fill_input(driver, wait, USERNAME_INPUT, email, timeout=12)
    safe_click_loc(driver, wait, BTN_AVANCAR, timeout=12)

    fill_input(driver, wait, PASSWORD_INPUT, wrong_password, timeout=12)
    safe_click_loc(driver, wait, BTN_AVANCAR, timeout=12)

    visible(driver, ERROR_WRONG_PASSWORD, timeout=12)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def expect_login_popup_mobile(driver, wait, timeout=8):
    """
    Mobile: apenas confirma que o popup apareceu após 1 clique.
    Critério: USERNAME_INPUT OU BTN_AVANCAR visível.
    """

    WebDriverWait(driver, timeout).until(
        lambda d: d.find_elements(*MOBILE_LOGIN_DROPDOWN_OPENED)
    )

    return True


def logout_mobile(driver):
    """Faz logout e espera mini-cart sumir."""
    safe_click_loc_retry(driver, LOGIN_NAME_CONTAINER, 10, 4, 0.25)
    time.sleep(2)
    safe_click_loc_retry(driver, BTN_LOGOUT, 10, 4, 0.25)
    time.sleep(2)

    end = time.time() + 15
    while time.time() < end:
        if not minicart_visible(driver):
            return
        time.sleep(0.1)

    assert_logged_out(driver, "logout")