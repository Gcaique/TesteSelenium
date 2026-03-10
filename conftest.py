import os
import re
import pytest
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


# =============================================================================
# Utils
# =============================================================================
def sanitize_test_name(s: str, max_len: int = 180) -> str:
    """
    O que faz:
    - Gera um nome "seguro" para sessão/teste em grids remotos e xdist no Windows.
    - Remove caracteres problemáticos (surrogates/acentos estranhos que quebram encoding).
    - Troca separadores por underscore e limita o tamanho.

    Por que existe:
    - Alguns grids (e o xdist) podem falhar com caracteres fora do padrão.
    - Também evita nomes muito longos em providers.
    """
    if not s:
        return "test"

    # Remove caracteres surrogate/ inválidos para evitar erros do tipo \udc81
    s = s.encode("utf-8", "ignore").decode("utf-8", "ignore")

    # Substitui qualquer coisa que não seja letra/número/_/./- por underscore
    s = re.sub(r"[^\w\-.]+", "_", s, flags=re.UNICODE)

    # Limita o tamanho do nome para evitar limites de providers
    return s[:max_len]


# =============================================================================
# CLI Options (pytest)
# =============================================================================
def pytest_addoption(parser):
    """
    O que faz:
    - Adiciona parâmetros via linha de comando para controlar ambiente/driver
      sem precisar alterar o código.
    """
    parser.addoption("--ambiente", action="store", default="desktop", help="desktop|mobile")
    parser.addoption("--navegador", action="store", default="chrome", help="chrome|firefox|edge|safari")
    parser.addoption("--so", action="store", default="Windows 11", help="Sistema operacional (LT/BS)")
    parser.addoption("--device", action="store", default="", help='Device name (mobile). Ex: "iPhone 14"')
    parser.addoption("--base-url", action="store", default=os.getenv("URL"), help="URL base")
    parser.addoption("--region", action="store", default="outras", help="outras|sul")
    parser.addoption("--username", action="store", default=os.getenv("USERNAME", ""), help="Login")
    parser.addoption("--password", action="store", default=os.getenv("PASSWORD", ""), help="Senha")
    parser.addoption("--timeout", action="store", default=10, type=int, help="Timeout padrão do WebDriverWait")
    parser.addoption("--grid", action="store", default="lt", help="lt|bs|local")
    parser.addoption("--headless", action="store_true", help="Executa browser local em modo headless")
    parser.addoption("--resolution", action="store", default="1920x1080", help='Resolução desktop no formato LARGURAxALTURA. Ex: 1920x1080')


# =============================================================================
# Fixtures base
# =============================================================================
@pytest.fixture(scope="session")
def base_url(request):
    """
    O que faz:
    - Disponibiliza a URL base para os testes.
    """
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def timeout(request):
    """
    O que faz:
    - Disponibiliza o timeout padrão do WebDriverWait.
    """
    return request.config.getoption("--timeout")


@pytest.fixture
def wait(driver, timeout):
    """
    O que faz:
    - Cria um WebDriverWait padrão para o driver atual.
    """
    return WebDriverWait(driver, timeout)


@pytest.fixture
def driver(request):
    """
    O que faz:
    - Cria o driver (local/LambdaTest/BrowserStack) baseado nos parâmetros CLI.
    - Aplica lógica "mobile inteligente":
        - se ambiente == mobile e navegador não informado -> define chrome ou safari (iOS).
        - NÃO força plataforma Android automaticamente (isso era do pCloudy).
    - Gera nome de sessão seguro.
    - Faz cleanup (quit) no final.
    """
    ambiente = request.config.getoption("--ambiente")
    navegador = request.config.getoption("--navegador")
    sistema_operacional = request.config.getoption("--so")
    device_name = request.config.getoption("--device")
    grid = (request.config.getoption("--grid") or "lt").strip().lower()
    headless = request.config.getoption("--headless")

    # -------------------------
    # MOBILE "inteligente"
    # -------------------------
    if ambiente == "mobile":
        # Se usuário não especificou --so direito, ele precisa escolher:
        # - iOS (Safari real): --so ios --device "iPhone 14" --navegador safari
        # - Android (Chrome): --so android --device "Pixel 7" --navegador chrome
        # Aqui a gente só ajusta defaults para reduzir erro de CLI.

        so_norm = (sistema_operacional or "").strip().lower()

        # Se o cara deixou default "Windows 11" mas quer mobile, não dá pra inferir.
        # Então escolhemos um padrão prático: Android (porque Safari real exige iOS + device).
        if so_norm in ("windows 11", "windows", "win11", "win"):
            sistema_operacional = "Android"
            so_norm = "android"

        # Device padrão (opcional) — você pode deixar vazio e passar via CLI sempre
        if not device_name:
            if so_norm == "ios":
                device_name = "iPhone 14"
            else:
                device_name = "Pixel 7"

        # Navegador padrão conforme SO
        if not navegador or navegador == "chrome":
            if so_norm == "ios":
                navegador = "safari"
            else:
                navegador = "chrome"

    # Nome de sessão/teste (bom para provider e para log)
    worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
    raw_name = f"{worker}::{request.node.nodeid}"
    nome_teste = sanitize_test_name(raw_name)

    driver = config.criar_driver(
        ambiente=ambiente,
        nome_teste=nome_teste,
        navegador=navegador,
        sistema_operacional=sistema_operacional,
        device_name=device_name,
        grid=grid,
        headless=headless
    )
    driver.maximize_window()

    yield driver
    driver.quit()


# =============================================================================
# Helpers (locators e funções utilitárias de página)
# =============================================================================
BTN_ACCEPT_COOKIES = (By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")
BTN_REGION_SUL = (By.XPATH, "//button[@id='southern-region']")
BTN_REGION_OUTRAS = (By.XPATH, "//button[@id='other-regions']")
BTN_CLOSE_MODAL_GENERIC = (By.XPATH, "//button[@class='close-modal']")
BTN_CLOSE_SPIN = (By.XPATH, "//button[@class='action-close hj-spintowin-close_button']")

LOGIN_NAME = (By.XPATH, "//div[@id='login-name']/span")
USERNAME = (By.XPATH, "//*[@id='username']")
PASSWORD = (By.XPATH, "//*[@name='login[password]']")
BTN_SEND2 = (By.XPATH, "//*[@class='secondary login-name']//button[@id='send2']")


def click_if_present(driver, locator, seconds=2):
    """
    O que faz:
    - Tenta clicar em um elemento se ele aparecer e estiver clicável.
    - Se não aparecer dentro do tempo, ignora (não quebra o teste).

    Usos típicos:
    - cookies banner
    - modal eventual
    - popups intermitentes
    """
    try:
        WebDriverWait(driver, seconds).until(EC.element_to_be_clickable(locator)).click()
        return True
    except Exception:
        return False


@pytest.fixture
def open_home(driver, base_url):
    """
    O que faz:
    - Abre a URL base.
    - (Opcional) Se você quiser tratar prompts do Chrome aqui,
      basta descomentar o dismiss_chrome_prompts quando seu driver suportar.
    """
    driver.get(base_url)

    # Se você usar isso para BrowserStack mobile web (Selenium) pode dar erro
    # porque não existe contexto NATIVE_APP (isso é Appium).
    # Então só habilite se você tiver implementado com segurança.
    # dismiss_chrome_prompts(driver, timeout=3)

    return driver


@pytest.fixture
def region(request):
    """
    O que faz:
    - Define a região padrão do site.
    - Prioridade:
        1) marker @pytest.mark.sul
        2) marker @pytest.mark.default
        3) opção CLI --region
    """
    if request.node.get_closest_marker("sul"):
        return "sul"
    if request.node.get_closest_marker("default"):
        return "outras"
    return request.config.getoption("--region")


@pytest.fixture
def setup_site(open_home, driver, region):
    """
    O que faz:
    - Executa o "setup" padrão do site para começar um teste de forma estável:
        1) espera body
        2) aceita cookies
        3) seleciona região (sul/outras)
        4) fecha modais ocasionais
        5) espera um elemento fixo da home para garantir que carregou
    """
    w = WebDriverWait(driver, 30)

    # 1) Espera body carregar
    w.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 2) Região
    if region == "sul":
        click_if_present(driver, BTN_REGION_SUL, seconds=15)
    else:
        click_if_present(driver, BTN_REGION_OUTRAS, seconds=15)

    # 3) Cookies
    click_if_present(driver, BTN_ACCEPT_COOKIES, seconds=20)

    # 4) Fecha modais ocasionais
    click_if_present(driver, BTN_CLOSE_SPIN, seconds=8)
    click_if_present(driver, BTN_CLOSE_MODAL_GENERIC, seconds=8)

    # 5) Espera algo fixo da home
    w.until(EC.presence_of_element_located((By.XPATH, "//a[@id='last-orders-action']")))

    return driver


@pytest.fixture
def creds(request):
    """
    O que faz:
    - Lê credenciais de login a partir da CLI (--username/--password).
    """
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")
    return username, password


@pytest.fixture
def login(driver, setup_site, creds):
    """
    O que faz:
    - Realiza login no site, quando o teste precisar.
    - Se não tiver credenciais, pula o teste para não falhar à toa.

    Como usar:
    - def test_x(login): ...
    """
    username, password = creds
    if not username or not password:
        pytest.skip("Credenciais não informadas. Use --username/--password ou .env")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_NAME)).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(USERNAME)).send_keys(username)
    driver.find_element(*PASSWORD).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_SEND2)).click()

    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    driver = item.funcargs.get("driver")
    if not driver:
        return

    caps = getattr(driver, "capabilities", {}) or {}

    # Detecta BrowserStack de forma bem robusta:
    # 1) chave bstack:options
    # 2) user do browserstack
    # 3) URL do hub contém browserstack
    hub_url = ""
    try:
        hub_url = getattr(getattr(driver, "command_executor", None), "_url", "") or ""
    except Exception:
        pass

    is_bs = (
        ("bstack:options" in caps)
        or ("browserstack.user" in caps)
        or ("browserstack" in hub_url.lower())
    )

    # DEBUG (uma vez por teste) — você pode remover depois
    # print(f"[DEBUG] is_bs={is_bs} hub={hub_url} keys={list(caps.keys())[:15]}")

    if not is_bs:
        return

    # Marca status no final do CALL (quando o teste realmente passou/falhou)
    if rep.when != "call":
        return

    status = "passed" if rep.passed else "failed"
    reason = "OK" if rep.passed else (rep.longreprtext[:250] if hasattr(rep, "longreprtext") else "Falha")

    payload = {
        "action": "setSessionStatus",
        "arguments": {"status": status, "reason": reason}
    }

    try:
        driver.execute_script("browserstack_executor: " + json.dumps(payload))
    except Exception as e:
        print(f"[WARN] Não consegui marcar status no BrowserStack: {e}")
        print(f"[WARN] hub_url={hub_url}")
        print(f"[WARN] caps_keys={list(caps.keys())}")