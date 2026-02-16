import os
import re
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


# ---------- util: deixa nome do teste "seguro" p/ xdist/execnet no Windows ----------
def sanitize_test_name(s: str, max_len: int = 180) -> str:
    """
    Remove caracteres que podem quebrar encoding no Windows/xdist (surrogates, acentos estranhos, etc.)
    e deixa um identificador estável para relatórios.
    """
    if not s:
        return "test"

    # 1) remove caracteres surrogate (causa do erro \udc81 etc)
    s = s.encode("utf-8", "ignore").decode("utf-8", "ignore")

    # 2) troca espaços e separadores por underscore e remove o resto que pode dar dor de cabeça
    s = re.sub(r"[^\w\-.]+", "_", s, flags=re.UNICODE)

    # 3) evita nomes gigantes (alguns grids/serviços têm limite)
    return s[:max_len]


# ---------- CLI options ----------
def pytest_addoption(parser):
    parser.addoption("--ambiente", action="store", default="desktop", help="desktop|mobile")
    parser.addoption("--navegador", action="store", default="chrome", help="chrome|firefox|edge")
    parser.addoption("--so", action="store", default="Windows 11", help="Sistema operacional para grid/LT")
    parser.addoption("--device", action="store", default="", help="Device name (se mobile)")
    parser.addoption("--base-url", action="store", default="https://meuminerva.com/", help="URL base")
    parser.addoption("--region", action="store", default="outras", help="outras|sul")
    parser.addoption("--username", action="store", default=os.getenv("USERNAME", ""), help="Login")
    parser.addoption("--password", action="store", default=os.getenv("PASSWORD", ""), help="Senha")
    parser.addoption("--timeout", action="store", default=10, type=int, help="Timeout padrão do WebDriverWait")
    parser.addoption("--grid", action="store", default="lt", help="lt|local")
    parser.addoption("--headless", action="store_true", help="Executa browser local em modo headless")


# ---------- fixtures base ----------
@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def timeout(request):
    return request.config.getoption("--timeout")


@pytest.fixture
def wait(driver, timeout):
    return WebDriverWait(driver, timeout)


@pytest.fixture
def driver(request):
    ambiente = request.config.getoption("--ambiente")
    navegador = request.config.getoption("--navegador")
    sistema_operacional = request.config.getoption("--so")
    device_name = request.config.getoption("--device")
    grid = request.config.getoption("--grid")
    headless = request.config.getoption("--headless")

    # 🔥 MOBILE INTELIGENTE
    if ambiente == "mobile":
        grid = "lt"  # mobile sempre no Lambda

        # Se não informou SO, define padrão Android
        if sistema_operacional == "Windows 11":
            sistema_operacional = "Android"

        # Se não informou device, define padrão por SO
        if not device_name:
            if sistema_operacional.lower() == "android":
                device_name = "Samsung Galaxy S20 Ultra"
            elif sistema_operacional.lower() == "ios":
                device_name = "iPhone 14 Pro"

        # Se não informou navegador (ou deixou default), define por SO
        # (mesmo que você passe "chrome", o config.py normaliza pra chromium)
        if not navegador or navegador == "chrome":
            if sistema_operacional.lower() == "ios":
                navegador = "safari"
            else:
                navegador = "chromium"

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

    yield driver
    driver.quit()


# ---------- helpers (sem POM, mas padronizados) ----------
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
    try:
        WebDriverWait(driver, seconds).until(EC.element_to_be_clickable(locator)).click()
        return True
    except Exception:
        return False


@pytest.fixture
def open_home(driver, base_url):
    """Abre a home sempre que chamado."""
    driver.get(base_url)
    return driver


@pytest.fixture
def region(request):
    """Região padrão via --region, mas pode ser sobrescrita por marker."""
    # marker tem prioridade
    if request.node.get_closest_marker("sul"):
        return "sul"
    if request.node.get_closest_marker("default"):
        return "outras"
    return request.config.getoption("--region")


@pytest.fixture
def setup_site(open_home, driver, region):
    w = WebDriverWait(driver, 30)

    # 1) Espera body carregar
    w.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 2) Cookies
    click_if_present(driver, BTN_ACCEPT_COOKIES, seconds=20)

    # 3) Região
    if region == "sul":
        click_if_present(driver, BTN_REGION_SUL, seconds=15)
    else:
        click_if_present(driver, BTN_REGION_OUTRAS, seconds=15)

    # 4) Fecha modais ocasionais
    click_if_present(driver, BTN_CLOSE_SPIN, seconds=8)
    click_if_present(driver, BTN_CLOSE_MODAL_GENERIC, seconds=8)

    # 5) Espera algo fixo da home
    w.until(EC.presence_of_element_located((By.XPATH, "//a[@id='last-orders-action']")))

    return driver



@pytest.fixture
def creds(request):
    username = request.config.getoption("--username")
    password = request.config.getoption("--password")
    return username, password


@pytest.fixture
def login(driver, setup_site, creds):
    """
    Faz login (quando o teste precisar).
    Uso: def test_x(login): ...
    """
    username, password = creds
    if not username or not password:
        pytest.skip("Credenciais não informadas. Use --username/--password ou .env")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(LOGIN_NAME)).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(USERNAME)).send_keys(username)
    driver.find_element(*PASSWORD).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(BTN_SEND2)).click()

    return driver
