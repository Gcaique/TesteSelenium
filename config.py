from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from dotenv import load_dotenv
import os
import re

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def _sanitize_lt_name(s: str, max_len: int = 180) -> str:
    """
    Garante que o nome do teste enviado ao LambdaTest não vai quebrar encoding.
    Remove surrogates e normaliza caracteres.
    """
    if not s:
        return "test"

    s = s.encode("utf-8", "ignore").decode("utf-8", "ignore")
    s = re.sub(r"[^\w\-.]+", "_", s, flags=re.UNICODE)
    return s[:max_len]


# ============================
# 🔐 CREDENCIAIS LAMBDATEST
# ============================
load_dotenv()  # carrega o .env automaticamente


def _get_lt_credentials():
    """
    Busca credenciais apenas quando necessário.
    Isso permite rodar local sem ter .env configurado.
    """
    lt_user = os.getenv("LT_USERNAME")
    lt_key = os.getenv("LT_ACCESS_KEY")
    if not lt_user or not lt_key:
        raise RuntimeError("Variáveis de ambiente LT_USERNAME e LT_ACCESS_KEY não definidas.")
    return lt_user, lt_key


# ======================
# LOCAL
# ======================
def driver_local(navegador="chrome", headless=False):
    if navegador == "chrome":
        options = ChromeOptions()

        # Flags importantes para estabilidade
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if headless:
            options.add_argument("--headless=new")
            # ESSENCIAL: define tamanho da janela no headless
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

        # Garantia extra (caso headless ignore maximize)
        driver.set_window_size(1920, 1080)
        return driver

    if navegador == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

        driver.set_window_size(1920, 1080)
        return driver

    raise Exception("Navegador local não suportado")


# ============================
# 🚀 DRIVER PRINCIPAL (LOCAL + LT)
# ============================
def criar_driver(
    ambiente,
    nome_teste,
    navegador,
    sistema_operacional,
    device_name="",
    grid="lt",          # <- novo (conftest passa isso)
    headless=False      # <- novo (conftest passa isso)
):
    """
    grid:
      - "local"      -> webdriver local
      - "lt" / "lambdatest" -> LambdaTest remoto
    """
    nome_teste = _sanitize_lt_name(nome_teste)
    grid = (grid or "lt").strip().lower()

    if grid == "local":
        return driver_local(navegador=navegador, headless=headless)

    # default: LambdaTest
    if ambiente == "desktop":
        return driver_desktop(nome_teste, navegador, sistema_operacional)
    else:
        return driver_mobile(nome_teste, navegador, sistema_operacional, device_name)


# ============================
# 💻 DESKTOP (LAMBDATEST)
# ============================
def driver_desktop(nome_teste, navegador, sistema_operacional, resolucao="1920x1080"):
    lt_user, lt_key = _get_lt_credentials()

    if navegador == "chrome":
        options = ChromeOptions()
    elif navegador == "firefox":
        options = FirefoxOptions()
    elif navegador == "safari":
        options = webdriver.SafariOptions()
    else:
        raise Exception("Navegador desktop não suportado")

    options.set_capability("browserName", navegador)
    options.set_capability("browserVersion", "latest")

    options.set_capability("LT:Options", {
        "platformName": sistema_operacional,
        "resolution": resolucao,
        "build": "Smoke - Desktop",
        "name": nome_teste,
        "selenium_version": "4.21.0",
    })

    return webdriver.Remote(
        command_executor=f"https://{lt_user}:{lt_key}@hub.lambdatest.com/wd/hub",
        options=options
    )


# ============================
# 📱 MOBILE (LAMBDATEST)
# ============================
def driver_mobile(nome_teste, navegador, sistema_operacional, device_name):
    lt_user, lt_key = _get_lt_credentials()

    so = (sistema_operacional or "").strip().lower()
    nav_in = (navegador or "").strip().lower()

    # --- normalização de nomes (LambdaTest mobile) ---
    if so == "ios":
        # iOS: Safari
        browser_name = "safari" if nav_in in ("", "chrome", "chromium", "safari") else nav_in
    else:
        # Android: LambdaTest NÃO aceita "chromium" aqui -> use "chrome"
        if nav_in in ("", "chromium"):
            browser_name = "chrome"
        elif nav_in in ("edge", "microsoftedge"):
            browser_name = "MicrosoftEdge"
        else:
            browser_name = nav_in

    # --- escolher Options compatível com o browser ---
    if browser_name in ("chrome", "brave", "duckduckgo"):
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    elif browser_name == "safari":
        options = webdriver.SafariOptions()
    else:
        raise Exception(
            f"Navegador mobile não suportado: {browser_name}. "
            "Use: chrome|firefox|safari|brave|duckduckgo|MicrosoftEdge"
        )

    options.set_capability("browserName", browser_name)
    options.set_capability("browserVersion", "latest")

    options.set_capability("LT:Options", {
        "platformName": sistema_operacional,   # "Android" ou "iOS"
        "deviceName": device_name,
        "isRealMobile": False,
        "build": "Smoke - Mobile",
        "name": nome_teste,
        "selenium_version": "4.21.0",
    })

    return webdriver.Remote(
        command_executor=f"https://{lt_user}:{lt_key}@hub.lambdatest.com/wd/hub",
        options=options
    )