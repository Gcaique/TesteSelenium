import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from helpers.waiters import _effective_timeout
from helpers.waiters import *
from helpers.actions import *
from helpers.popups import *
from helpers.minicart import minicart_visible

from locators.header import *



def ensure_logged_in(driver, user: str, passwd: str, wait=None, timeout=None):
    """Garante login (idempotente)"""
    t = _effective_timeout(wait, timeout)
    # abre login
    click(driver, LOGIN_MENU, timeout=t, wait=wait)
    visible(driver, USERNAME_INPUT, wait=wait, timeout=t)

    # username
    fill(driver, USERNAME_INPUT, user, timeout=t, wait=wait)
    click(driver, BTN_AVANCAR, timeout=t, wait=wait)

    # senha
    visible(driver, PASSWORD_INPUT, wait=wait, timeout=t)
    fill(driver, PASSWORD_INPUT, passwd, timeout=t, wait=wait)
    click(driver, BTN_AVANCAR, timeout=t, wait=wait)

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


def expect_login_popup(driver, wait, label="login_popup", timeout=None, retries=2, sleep_between=0.6):
    """
    Confirma que o pop-up de login do header abriu.
    Critério: aparecer USERNAME_INPUT ou BTN_AVANCAR (depende do estado do modal).
    Faz pequenas tentativas antes de falhar.
    """
    last_exc = None

    for attempt in range(retries + 1):
        try:
            eff = _effective_timeout(wait, timeout)
            end = time.time() + eff
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


def open_login(driver, wait=None, timeout=None):
    """Abre o modal de login e garante que o campo username apareceu."""
    t = _effective_timeout(wait, timeout, default=10)
    click(driver, LOGIN_MENU, timeout=t, wait=wait)
    visible(driver, USERNAME_INPUT, wait=wait, timeout=t)


def click_avancar(driver):
    """Clica no botão Avançar do modal."""
    click(driver, BTN_AVANCAR)


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


def wait_username_result(driver, timeout=None):
    """
    Após clicar Avançar na etapa USERNAME, detecta o estado:
    - password -> campo de senha abriu
    - error    -> erro Magento apareceu
    - native   -> validação nativa do browser apareceu
    - none     -> site não reagiu dentro do timeout
    """
    eff = timeout if timeout is not None else _effective_timeout(None, None, default=DEFAULT_TIMEOUT)
    end = time.time() + eff
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


def wait_password_result(driver, timeout=None):
    """
    Após clicar Avançar na etapa SENHA, detecta o estado:
    - success  -> mini-cart apareceu (logou)
    - error    -> erro Magento apareceu
    - password -> continuou no campo senha sem erro até o timeout
    """
    eff = timeout if timeout is not None else  _effective_timeout(None, None, default=DEFAULT_TIMEOUT)
    end = time.time() + eff
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

    kind, msg = wait_username_result(driver, timeout=_effective_timeout(wait, None))

    assert kind != "password", f"[{context}] Não era para abrir senha, mas abriu."

    if tokens and msg:
        low = msg.lower()
        assert any(t.lower() in low for t in tokens), f"[{context}] msg inesperada: '{msg}'"


def submit_username_valid(driver, username, context):
    """Envia username válido e exige que o campo de senha apareça."""
    fill(driver, USERNAME_INPUT, username)
    click_avancar(driver)

    kind, msg = wait_username_result(driver, timeout=_effective_timeout(wait, None))
    assert kind == "password", f"[{context}] Era para abrir senha, veio: {kind} / '{msg}'"


def login_password(driver, password, context, expect_success: bool):
    """
    Submete senha:
    - expect_success=True  -> exige login (mini-cart visível)
    - expect_success=False -> exige erro de senha (Magento)
    """
    fill(driver, PASSWORD_INPUT, password)
    click_avancar(driver)

    eff = _effective_timeout(wait, None)
    kind, msg = wait_password_result(driver, timeout=eff)

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


def logout(driver, wait=None, timeout=None):
    """Faz logout e espera mini-cart sumir."""
    t = _effective_timeout(wait, timeout, default=10)
    click(driver, LOGIN_NAME_CONTAINER, timeout=t, wait=wait)
    time.sleep(1)
    click(driver, BTN_LOGOUT, timeout=t, wait=wait)

    end = time.time() + 15
    while time.time() < end:
        if not minicart_visible(driver):
            return
        time.sleep(0.1)

    assert_logged_out(driver, "logout")


def login_expect_email_not_found(driver, wait, email):
    safe_click_loc(driver, wait, LOGIN_MENU)
    fill_input(driver, wait, USERNAME_INPUT, email)
    safe_click_loc(driver, wait, BTN_AVANCAR)
    visible(driver, ERROR_EMAIL_NOT_FOUND, wait=wait)

def login_expect_wrong_password(driver, wait, email, wrong_password):
    fill_input(driver, wait, USERNAME_INPUT, email)
    safe_click_loc(driver, wait, BTN_AVANCAR)

    fill_input(driver, wait, PASSWORD_INPUT, wrong_password)
    safe_click_loc(driver, wait, BTN_AVANCAR)

    visible(driver, ERROR_WRONG_PASSWORD, wait=wait)


def clicar_esqueci_senha(driver, wait):
    """Clica no link 'Esqueci minha senha'."""
    wait.until(EC.element_to_be_clickable(LINK_ESQUECI_SENHA)).click()
    time.sleep(3)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def expect_login_popup_mobile(driver, wait, timeout=None):
    """
    Mobile: apenas confirma que o popup apareceu após 1 clique.
    Critério: USERNAME_INPUT OU BTN_AVANCAR visível.
    """

    eff = _effective_timeout(wait, timeout)
    WebDriverWait(driver, eff).until(
        lambda d: d.find_elements(*MOBILE_LOGIN_DROPDOWN_OPENED)
    )

    return True

def logout_mobile(driver, wait=None, timeout=None):
    """Faz logout e espera mini-cart sumir."""
    t = _effective_timeout(wait, timeout, default=10)
    mobile_click_strict(driver, LOGIN_NAME_CONTAINER, t, 4, 0.25, wait=wait)
    time.sleep(2)
    mobile_click_strict(driver, BTN_LOGOUT, t, 4, 0.25, wait=wait)
    time.sleep(2)

    end = time.time() + 15
    while time.time() < end:
        if not minicart_visible(driver):
            return
        time.sleep(0.1)

    assert_logged_out(driver, "logout")

def ensure_logged_in_mobile(driver, user: str, passwd: str, wait=None, timeout=None):
    """Garante login (idempotente)"""
    t = _effective_timeout(wait, timeout, default=10)

    # abre login
    click(driver, LOGIN_MENU, timeout=t, wait=wait)
    visible(driver, MOBILE_LOGIN_DROPDOWN_OPENED, wait=wait, timeout=t)
    click(driver, MOBILE_LOGIN_ACESSO, timeout=t, wait=wait)
    visible(driver, USERNAME_INPUT, wait=wait, timeout=t)

    # username
    fill(driver, USERNAME_INPUT, user, timeout=t, wait=wait)
    click(driver, BTN_AVANCAR, timeout=t, wait=wait)

    # senha
    visible(driver, PASSWORD_INPUT, wait=wait, timeout=t)
    fill(driver, PASSWORD_INPUT, passwd, timeout=t, wait=wait)
    click(driver, BTN_AVANCAR, timeout=t, wait=wait)

    # confirmação via minicart
    end = time.time() + 60

    while time.time() < end:
        if minicart_visible(driver):
            try_close_popups(driver)
            return
        time.sleep(0.5)

    # fallback
    driver.refresh()
    time.sleep(3)
    try_close_popups(driver)

    if minicart_visible(driver):
        return

    raise TimeoutException("Login não confirmou: mini-cart não ficou visível.")

def login_expect_email_not_found_mobile(driver, wait, email):
    safe_click_loc(driver, wait, LOGIN_MENU)
    expect_login_popup_mobile(driver, wait, timeout=None)
    safe_click_loc(driver, wait, MOBILE_LOGIN_ACESSO)
    visible(driver, USERNAME_INPUT, wait=wait)
    fill_input(driver, wait, USERNAME_INPUT, email)
    safe_click_loc(driver, wait, BTN_AVANCAR)
    visible(driver, ERROR_EMAIL_NOT_FOUND, wait=wait)
