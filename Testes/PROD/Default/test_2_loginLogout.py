import time
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)

# =========================
# Credenciais (ajuste aqui)
# =========================
VALID_USER = "caique.oliveira@infobase.com.br"
VALID_PASS = "Min@1234"

# =========================
# Locators
# =========================
LOGIN_MENU = (By.XPATH, "//div[@id='login-name']/span")     # "Faça seu login"
LOGIN_NAME_CONTAINER = (By.ID, "login-name")               # área do usuário (logado)
USERNAME_INPUT = (By.ID, "username")                       # input e-mail/cnpj/cpf
PASSWORD_INPUT = (By.XPATH, "//*[@name='login[password]']")# input senha
BTN_AVANCAR = (By.ID, "send2")                             # botão "Avançar"

ERROR_BOX = (By.XPATH, "//*[@class='message-error error message']")  # erro Magento
HOTJAR_CLOSE = (By.XPATH, "//dialog//button")                        # popup hotjar (às vezes)

# Indicador de LOGADO (fonte da verdade)
MINICART_WRAPPER = (By.XPATH, "//*[@data-block='minicart' and contains(@class,'minicart-wrapper')]")

# Navegação / Busca / Últimos
LOGO = (By.XPATH, "//a[contains(@class,'hj-header-logo')]")
BTN_LAST_ORDERS = (By.ID, "last-orders-action")
BTN_LAST_ITEMS = (By.ID, "last-items-action")
EMPTY_GRID_VER_PRODUTOS = (By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a")

CATEGORY_MENU = lambda name: (By.XPATH, f"//*[@id='nav-menu-desktop']//span[normalize-space()='{name}']")
SEARCH_INPUT = (By.ID, "minisearch-input-top-search")
SEARCH_BUTTON = (By.XPATH, "//button[@title='Buscar']//span[normalize-space()='Buscar']")

# Logout
BTN_LOGOUT = (By.ID, "action-logout")

# Seções home (scroll)
HOME_SECTIONS = [
    "(//div[contains(@class, 'slider-products')])[1]",
    "//div[@class='brands-carousel']",
    "(//div[contains(@class, 'slider-products')])[2]",
    "//*[@class='cutting-map __home-section']",
    "//div[@class='footer-content']"
]


# =========================
# Helpers
# =========================
def wait(driver, timeout=10, poll=0.1):
    """Cria um WebDriverWait padrão com polling rápido."""
    return WebDriverWait(driver, timeout, poll_frequency=poll)


def visible(driver, locator, timeout=10):
    """Espera até o elemento estar visível na tela."""
    return wait(driver, timeout).until(EC.visibility_of_element_located(locator))


def clickable(driver, locator, timeout=10):
    """Espera até o elemento estar clicável (visível + habilitado)."""
    return wait(driver, timeout).until(EC.element_to_be_clickable(locator))


def click(driver, locator, timeout=10):
    """
    Clique robusto:
    - tenta click normal
    - se interceptado/stale, usa fallback JS click
    """
    el = clickable(driver, locator, timeout)
    try:
        el.click()
    except (ElementClickInterceptedException, StaleElementReferenceException):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        driver.execute_script("arguments[0].click();", el)


def fill(driver, locator, value: str):
    """Preenche input com clear + send_keys, com fallback via JS se clear falhar."""
    el = visible(driver, locator, timeout=10)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)
    el.send_keys(value)


def try_close_hotjar(driver):
    """Fecha popup do Hotjar se aparecer (não falha se não existir)."""
    try:
        click(driver, HOTJAR_CLOSE, timeout=1.5)
    except Exception:
        pass


def read_error(driver) -> str:
    """Lê o texto do erro Magento (caixa vermelha). Retorna '' se não houver."""
    try:
        el = visible(driver, ERROR_BOX, timeout=1.5)
        return (el.text or "").strip()
    except Exception:
        return ""


def native_validation(driver, locator) -> str:
    """Lê mensagem nativa do navegador (HTML5 validation). Retorna '' se não houver."""
    try:
        el = driver.find_element(*locator)
        msg = driver.execute_script("return arguments[0].validationMessage;", el)
        return (msg or "").strip()
    except Exception:
        return ""


def minicart_visible(driver) -> bool:
    """Fonte da verdade de LOGADO: mini-cart visível no header."""
    try:
        el = wait(driver, 1.5).until(EC.visibility_of_element_located(MINICART_WRAPPER))
        return el.is_displayed()
    except Exception:
        return False


def assert_logged_out(driver, context=""):
    """Assert de DESLOGADO via mini-cart."""
    assert not minicart_visible(driver), f"[{context}] Era para estar DESLOGADO, mas mini-cart está visível."


def open_login(driver):
    """Abre o modal de login e garante que o campo username apareceu."""
    click(driver, LOGIN_MENU, timeout=10)
    visible(driver, USERNAME_INPUT, timeout=10)


def click_avancar(driver):
    """Clica no botão Avançar do modal."""
    click(driver, BTN_AVANCAR, timeout=10)


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
    click(driver, BTN_LOGOUT, timeout=10)

    end = time.time() + 15
    while time.time() < end:
        if not minicart_visible(driver):
            return
        time.sleep(0.1)

    assert_logged_out(driver, "logout")


def go_home(driver):
    """Volta para a home clicando na logo."""
    click(driver, LOGO, timeout=10)


def scroll_to(driver, xpath):
    """Faz scroll até uma seção específica da home."""
    locator = (By.XPATH, xpath)
    el = visible(driver, locator, timeout=8)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)


def run_public_flows(driver, logged: bool):
    """
    Fluxos públicos (reutilizável para logado/deslogado):
    - scroll em seções
    - navegar categorias
    - busca
    - últimos pedidos e últimos itens
    """
    # scroll seções
    for xp in HOME_SECTIONS:
        scroll_to(driver, xp)

    # categorias
    for categoria in ["Promoções"]:
        click(driver, CATEGORY_MENU(categoria), timeout=10)
        visible(driver, SEARCH_INPUT, timeout=10)

    # busca
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "peixe")
    click(driver, SEARCH_BUTTON, timeout=10)
    visible(driver, SEARCH_INPUT, timeout=10)

    # últimos pedidos
    go_home(driver)
    click(driver, BTN_LAST_ORDERS, timeout=10)

    if logged:
        visible(driver, EMPTY_GRID_VER_PRODUTOS, timeout=20)
        try_close_hotjar(driver)
        click(driver, EMPTY_GRID_VER_PRODUTOS, timeout=10)
    else:
        visible(driver, USERNAME_INPUT, timeout=10)
        click(driver, LOGIN_MENU, timeout=5)  # fecha modal

    # últimos produtos comprados
    click(driver, BTN_LAST_ITEMS, timeout=10)

    if logged:
        visible(driver, EMPTY_GRID_VER_PRODUTOS, timeout=20)
        click(driver, EMPTY_GRID_VER_PRODUTOS, timeout=10)
    else:
        visible(driver, USERNAME_INPUT, timeout=10)
        click(driver, LOGIN_MENU, timeout=5)  # fecha modal


# =========================
# TESTE
# =========================
@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.loginLogout
def test_2_loginLogout(driver, setup_site):
    """
    Fluxo Login/Logout (otimizado e estável):
    01) Garantir estado inicial DESLOGADO
    02) Abrir modal de login
    03) Username inválido: email não encontrado
    04) Username inválido: cnpj mismatch/não encontrado
    05) Username inválido: formato inválido
    06) Username inválido: cnpj fake
    07) Username válido: abrir senha
    08) Senha inválida: erro
    09) Senha válida: login OK (mini-cart visível)
    10) Fluxos públicos LOGADO
    11) Logout
    12) Fluxos públicos DESLOGADO
    13) Últimos pedidos deslogado -> loga -> ver produtos
    14) Logout final
    """

    # 01) Garantir estado inicial DESLOGADO
    if minicart_visible(driver):
        try:
            logout(driver)
        except Exception:
            driver.delete_all_cookies()
            driver.get("https://meuminerva.com.br/")
            time.sleep(1.5)

    assert_logged_out(driver, "01) estado inicial")

    # 02) Abrir modal de login
    open_login(driver)

    # 03) Username inválido: email não encontrado
    submit_username_invalid(
        driver,
        "teste.12345@teste.com",
        "03) email não encontrado",
        tokens=["verifique", "cpf", "cnpj", "e-mail", "email"],
    )

    # 04) Username inválido: cnpj mismatch/não encontrado
    submit_username_invalid(
        driver,
        "42.765.782/0001-08",
        "04) cnpj não encontrado",
        tokens=["verifique", "e-mail", "email", "cpf", "cnpj"],
    )

    # 05) Username inválido: formato inválido
    submit_username_invalid(
        driver,
        "teste.teste",
        "05) formato inválido",
        tokens=["insira", "e-mail", "email", "cpf", "cnpj", "invál", "inval"],
    )

    # 06) Username inválido: cnpj fake
    submit_username_invalid(
        driver,
        "11.222.333/4444-55",
        "06) cnpj fake",
        tokens=["insira", "e-mail", "email", "cpf", "cnpj", "invál", "inval"],
    )

    # 07) Username válido: abrir senha
    submit_username_valid(driver, VALID_USER, "07) usuário válido")

    # 08) Senha inválida: erro
    login_password(driver, "SenhaErrada_", "08) senha inválida", expect_success=False)

    # 09) Senha válida: login OK
    login_password(driver, VALID_PASS, "09) senha válida", expect_success=True)

    # 10) Fluxos públicos LOGADO
    run_public_flows(driver, logged=True)

    # 11) Logout
    logout(driver)
    assert_logged_out(driver, "11) após logout")

    # 12) Fluxos públicos DESLOGADO
    run_public_flows(driver, logged=False)

    # 13) Últimos pedidos deslogado -> loga -> ver produtos
    go_home(driver)
    click(driver, BTN_LAST_ORDERS, timeout=10)

    visible(driver, USERNAME_INPUT, timeout=10)
    submit_username_valid(driver, VALID_USER, "13) login via últimos pedidos (username)")
    login_password(driver, VALID_PASS, "13) login via últimos pedidos (senha)", expect_success=True)

    visible(driver, EMPTY_GRID_VER_PRODUTOS, timeout=20)
    try_close_hotjar(driver)
    click(driver, EMPTY_GRID_VER_PRODUTOS, timeout=10)

    # 14) Logout final
    logout(driver)
    assert_logged_out(driver, "14) fim do teste")
