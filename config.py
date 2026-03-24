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


# ============================
# ✅ Utils
# ============================
def _sanitize_test_name(s: str, max_len: int = 180) -> str:
    """
    Sanitiza o nome do teste (evita caracteres que quebram encoding/serviços remotos).
    """
    if not s:
        return "test"
    s = s.encode("utf-8", "ignore").decode("utf-8", "ignore")
    s = re.sub(r"[^\w\-.]+", "_", s, flags=re.UNICODE)
    return s[:max_len]


# ============================
# 🔐 Credenciais (LT + BS + SAUCE)
# ============================
load_dotenv()  # carrega .env automaticamente


def _get_lt_credentials():
    """
    Lê LT_USERNAME e LT_ACCESS_KEY do ambiente (.env).
    """
    lt_user = os.getenv("LT_USERNAME")
    lt_key = os.getenv("LT_ACCESS_KEY")
    if not lt_user or not lt_key:
        raise RuntimeError("Variáveis LT_USERNAME e LT_ACCESS_KEY não definidas.")
    return lt_user, lt_key


def _get_bs_credentials():
    """
    Lê BROWSERSTACK_USERNAME e BROWSERSTACK_ACCESS_KEY do ambiente (.env).
    """
    user = os.getenv("BROWSERSTACK_USERNAME")
    key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    if not user or not key:
        raise RuntimeError("Variáveis BROWSERSTACK_USERNAME e BROWSERSTACK_ACCESS_KEY não definidas.")
    return user, key


def _get_bs_hub():
    """
    HUB Selenium do BrowserStack.
    """
    return "https://hub-cloud.browserstack.com/wd/hub"


def _get_sauce_credentials():
    """
    Lê SAUCE_USERNAME e SAUCE_ACCESS_KEY do ambiente (.env).
    """
    user = os.getenv("SAUCE_USERNAME")
    key = os.getenv("SAUCE_ACCESS_KEY")
    if not user or not key:
        raise RuntimeError("Variáveis SAUCE_USERNAME e SAUCE_ACCESS_KEY não definidas.")
    return user, key


def _get_sauce_hub():
    """
    Endpoint Selenium do Sauce Labs conforme região.
    Regiões suportadas:
      - us-west
      - us-east
      - eu-central
    """
    region = (os.getenv("SAUCE_REGION", "us-west") or "").strip().lower()

    hubs = {
        "us-west": "https://ondemand.us-west-1.saucelabs.com/wd/hub",
        "us-east": "https://ondemand.us-east-4.saucelabs.com/wd/hub",
        "eu-central": "https://ondemand.eu-central-1.saucelabs.com/wd/hub",
    }

    if region not in hubs:
        raise RuntimeError(
            "SAUCE_REGION inválida. Use: us-west, us-east ou eu-central."
        )

    return hubs[region]


# ======================
# 🖥️ Local
# ======================
def driver_local(navegador="chrome", headless=False):
    """
    Cria driver local (Chrome/Firefox).
    """
    nav = (navegador or "").strip().lower()

    if nav == "chrome":
        options = ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.set_window_size(1920, 1080)
        return driver

    if nav == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")

        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.set_window_size(1920, 1080)
        return driver

    raise Exception("Navegador local não suportado (use chrome|firefox).")


# ============================
# 🚀 Driver principal (local + LT + BS)
# ============================
def criar_driver(
    ambiente,
    nome_teste,
    navegador,
    sistema_operacional,
    device_name="",
    grid="lt",
    headless=False,
    resolucao="1920x1080"
):
    """
    Decide qual provedor usar.

    grid:
      - local -> roda na sua máquina
      - lt    -> LambdaTest
      - bs    -> BrowserStack
    ambiente:
      - desktop
      - mobile
    """
    nome_teste = _sanitize_test_name(nome_teste)
    grid = (grid or "lt").strip().lower()
    ambiente = (ambiente or "desktop").strip().lower()

    if grid == "local":
        return driver_local(navegador=navegador, headless=headless)

    if grid in ("browserstack", "bs"):
        if ambiente == "desktop":
            return driver_desktop_browserstack(nome_teste, navegador, sistema_operacional, resolucao)
        else:
            so = (sistema_operacional or "").strip().lower()
            if so == "ios":
                return driver_mobile_browserstack_ios_safari(nome_teste, device_name)
            else:
                return driver_mobile_browserstack_android_chrome(nome_teste, device_name)

    if grid in ("sauce", "saucelabs", "sl"):
        if ambiente == "desktop":
            return driver_desktop_saucelabs(nome_teste, navegador, sistema_operacional, resolucao)
        else:
            so = (sistema_operacional or "").strip().lower()
            if so == "ios":
                return driver_mobile_saucelabs_ios_safari(nome_teste, device_name)
            else:
                return driver_mobile_saucelabs_android_chrome(nome_teste, device_name)

    # default: LambdaTest
    if ambiente == "desktop":
        return driver_desktop_lambdatest(nome_teste, navegador, sistema_operacional, resolucao)
    else:
        return driver_mobile_lambdatest(nome_teste, navegador, sistema_operacional, device_name)


# ============================
# 💻 Desktop (LambdaTest)
# ============================
def driver_desktop_lambdatest(nome_teste, navegador, sistema_operacional, resolucao="1920x1080"):
    """
    Desktop remoto no LambdaTest.
    """
    lt_user, lt_key = _get_lt_credentials()
    nav = (navegador or "chrome").strip().lower()

    if nav == "chrome":
        options = ChromeOptions()
    elif nav == "firefox":
        options = FirefoxOptions()
    elif nav == "edge":
        options = webdriver.EdgeOptions()
    elif nav == "safari":
        options = webdriver.SafariOptions()
    else:
        raise Exception("Navegador desktop não suportado no LT (chrome|firefox|edge|safari).")

    options.set_capability("browserName", nav)
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
# 📱 Mobile web (LambdaTest)
# ============================
def driver_mobile_lambdatest(nome_teste, navegador, sistema_operacional, device_name):
    """
    Mobile web remoto no LambdaTest (geralmente emulado / device cloud conforme conta).
    """
    lt_user, lt_key = _get_lt_credentials()

    so = (sistema_operacional or "").strip().lower()
    nav_in = (navegador or "").strip().lower()

    if so == "ios":
        browser_name = "safari" if nav_in in ("", "chrome", "chromium", "safari") else nav_in
    else:
        if nav_in in ("", "chromium"):
            browser_name = "chrome"
        elif nav_in in ("edge", "microsoftedge"):
            browser_name = "MicrosoftEdge"
        else:
            browser_name = nav_in

    if browser_name in ("chrome", "brave", "duckduckgo"):
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FirefoxOptions()
    elif browser_name == "safari":
        options = webdriver.SafariOptions()
    else:
        raise Exception("Navegador mobile não suportado no LT (chrome|firefox|safari|edge).")

    options.set_capability("browserName", browser_name)
    options.set_capability("browserVersion", "latest")

    options.set_capability("LT:Options", {
        "platformName": sistema_operacional,
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


# ============================
# 💻 Desktop (BrowserStack)
# ============================
def driver_desktop_browserstack(nome_teste, navegador, sistema_operacional, resolucao="1920x1080"):
    """
    Desktop web no BrowserStack (Windows/macOS + Chrome/Firefox/Edge/Safari).
    """
    bs_user, bs_key = _get_bs_credentials()
    hub = _get_bs_hub()

    nav = (navegador or "chrome").strip().lower()
    if nav == "chrome":
        options = ChromeOptions()
    elif nav == "firefox":
        options = FirefoxOptions()
    elif nav == "edge":
        options = webdriver.EdgeOptions()
    elif nav == "safari":
        options = webdriver.SafariOptions()
    else:
        raise Exception("Navegador desktop não suportado no BS (chrome|firefox|edge|safari).")

    # BuildName dinâmico (você pode setar no .env)
    build_name = os.getenv("BS_BUILD_NAME", "Smoke - Desktop")
    project_name = os.getenv("BS_PROJECT_NAME", "MeuMinerva")

    options.set_capability("browserName", nav)
    options.set_capability("browserVersion", "latest")

    # bstack:options é o padrão W3C do BrowserStack
    options.set_capability("bstack:options", {
        "os": "Windows" if "windows" in (sistema_operacional or "").lower() else "OS X",
        "osVersion": "11" if "windows" in (sistema_operacional or "").lower() else "Sonoma",
        "sessionName": nome_teste,
        "buildName": build_name,
        "projectName": project_name,
        "seleniumVersion": "4.21.0",
        "resolution": resolucao,
        "debug": True,
        "networkLogs": False,
        "consoleLogs": "errors",
    })

    return webdriver.Remote(
        command_executor=f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )


# ============================
# 📱 iOS REAL + Safari (BrowserStack)
# ============================
def driver_mobile_browserstack_ios_safari(nome_teste, device_name):
    """
    iOS REAL DEVICE + Safari (BrowserStack Automate Mobile Web).
    device_name: ex "iPhone 14", "iPhone 15", etc.
    """
    bs_user, bs_key = _get_bs_credentials()
    hub = _get_bs_hub()

    if not device_name:
        raise Exception('No BrowserStack iOS real, informe --device (ex: "iPhone 14").')

    build_name = os.getenv("BS_BUILD_NAME", "Smoke - iOS Safari")
    project_name = os.getenv("BS_PROJECT_NAME", "MeuMinerva")
    ios_version = os.getenv("BS_IOS_VERSION", "17")

    options = webdriver.SafariOptions()
    options.set_capability("browserName", "safari")

    options.set_capability("bstack:options", {
        "deviceName": device_name,
        "osVersion": ios_version,
        "realMobile": True,
        "sessionName": nome_teste,
        "buildName": build_name,
        "projectName": project_name,
        "debug": True,
        "networkLogs": False,
        "consoleLogs": "errors",
    })

    return webdriver.Remote(
        command_executor=f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )


# ============================
# 📱 Android REAL + Chrome (BrowserStack)
# ============================
def driver_mobile_browserstack_android_chrome(nome_teste, device_name):
    """
    Android REAL DEVICE + Chrome (BrowserStack Automate Mobile Web).
    device_name: ex "Samsung Galaxy S23", "Google Pixel 7", etc.
    """
    bs_user, bs_key = _get_bs_credentials()
    hub = _get_bs_hub()

    if not device_name:
        raise Exception('No BrowserStack Android real, informe --device (ex: "Google Pixel 7").')

    build_name = os.getenv("BS_BUILD_NAME", "Smoke - Android Chrome")
    project_name = os.getenv("BS_PROJECT_NAME", "MeuMinerva")
    android_version = os.getenv("BS_ANDROID_VERSION", "13")

    options = ChromeOptions()
    options.set_capability("browserName", "chrome")

    options.set_capability("bstack:options", {
        "deviceName": device_name,
        "osVersion": android_version,
        "realMobile": True,
        "sessionName": nome_teste,
        "buildName": build_name,
        "projectName": project_name,
        "debug": True,
        "networkLogs": False,
        "consoleLogs": "errors",
    })

    return webdriver.Remote(
        command_executor=f"https://{bs_user}:{bs_key}@hub-cloud.browserstack.com/wd/hub",
        options=options
    )


# ============================
# 💻 Desktop (Sauce Labs)
# ============================
def driver_desktop_saucelabs(nome_teste, navegador, sistema_operacional, resolucao="1920x1080"):
    """
    Desktop web no Sauce Labs.
    """
    sauce_user, sauce_key = _get_sauce_credentials()
    hub = _get_sauce_hub()

    nav = (navegador or "chrome").strip().lower()

    if nav == "chrome":
        options = ChromeOptions()
    elif nav == "firefox":
        options = FirefoxOptions()
    elif nav == "edge":
        options = webdriver.EdgeOptions()
    elif nav == "safari":
        options = webdriver.SafariOptions()
    else:
        raise Exception("Navegador desktop não suportado no Sauce (chrome|firefox|edge|safari).")

    build_name = os.getenv("SAUCE_BUILD_NAME", "Smoke - Desktop")
    project_name = os.getenv("SAUCE_PROJECT_NAME", "MeuMinerva")

    # Mapeamento básico de plataforma
    so_in = (sistema_operacional or "").strip().lower()
    if "windows" in so_in:
        platform_name = "Windows 11"
    elif "mac" in so_in or "os x" in so_in:
        platform_name = "macOS 14"
    else:
        platform_name = sistema_operacional

    options.set_capability("browserName", nav)
    options.set_capability("browserVersion", "latest")
    options.set_capability("platformName", platform_name)

    options.set_capability("sauce:options", {
        "name": nome_teste,
        "build": build_name,
        "project": project_name,
        "screenResolution": resolucao,
        "seleniumVersion": "4.21.0",
    })

    return webdriver.Remote(
        command_executor=f"https://{sauce_user}:{sauce_key}@{hub.replace('https://', '')}",
        options=options
    )


# ============================
# 📱 Android REAL + Chrome (Sauce Labs)
# ============================
def driver_mobile_saucelabs_android_chrome(nome_teste, device_name):
    """
    Android mobile web no Sauce Labs.
    """
    sauce_user, sauce_key = _get_sauce_credentials()
    hub = _get_sauce_hub()

    if not device_name:
        raise Exception('No Sauce Android, informe --device (ex: "Google Pixel 7").')

    build_name = os.getenv("SAUCE_BUILD_NAME", "Smoke - Android Chrome")
    project_name = os.getenv("SAUCE_PROJECT_NAME", "MeuMinerva")
    android_version = os.getenv("SAUCE_ANDROID_VERSION", "14")
    appium_version = os.getenv("SAUCE_APPIUM_VERSION", "latest")

    options = ChromeOptions()
    options.set_capability("browserName", "chrome")
    options.set_capability("platformName", "Android")
    options.set_capability("appium:deviceName", device_name)
    options.set_capability("appium:platformVersion", android_version)
    options.set_capability("appium:automationName", "UiAutomator2")

    options.set_capability("sauce:options", {
        "name": nome_teste,
        "build": build_name,
        "project": project_name,
        "appiumVersion": appium_version,
    })

    return webdriver.Remote(
        command_executor=f"https://{sauce_user}:{sauce_key}@{hub.replace('https://', '')}",
        options=options
    )


# ============================
# 📱 iOS REAL + Safari (Sauce Labs)
# ============================
def driver_mobile_saucelabs_ios_safari(nome_teste, device_name):
    sauce_user, sauce_key = _get_sauce_credentials()
    hub = _get_sauce_hub()

    if not device_name:
        raise Exception('No Sauce iOS, informe --device (ex: "iPhone 14").')

    build_name = os.getenv("SAUCE_BUILD_NAME", "Smoke - iOS Safari")
    project_name = os.getenv("SAUCE_PROJECT_NAME", "MeuMinerva")
    ios_version = os.getenv("SAUCE_IOS_VERSION", "").strip()
    appium_version = os.getenv("SAUCE_APPIUM_VERSION", "latest")

    options = webdriver.SafariOptions()
    options.set_capability("browserName", "safari")
    options.set_capability("platformName", "iOS")
    options.set_capability("appium:deviceName", device_name)
    options.set_capability("appium:automationName", "XCUITest")

    if ios_version:
        options.set_capability("appium:platformVersion", ios_version)

    options.set_capability("sauce:options", {
        "name": nome_teste,
        "build": build_name,
        "project": project_name,
        "appiumVersion": appium_version,
    })

    return webdriver.Remote(
        command_executor=f"https://{sauce_user}:{sauce_key}@{hub.replace('https://', '')}",
        options=options
    )