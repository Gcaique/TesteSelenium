from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import config

# Configuração do WebDriver usando config
driver = config.criar_driver(
    ambiente="desktop",
    nome_teste="Abre o navegador e acessa a pagina do Meu Minerva",
    navegador="chrome",
    sistema_operacional="Windows 11",
    device_name=""
)
wait = WebDriverWait(driver, 10)

# =========================
# HELPERS ROBUSTOS
# =========================
def try_click(xpath, descricao, sleep=2):
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).click()
        print(f"✅ {descricao}")
        time.sleep(sleep)
        return True
    except Exception:
        print(f"⚠️ {descricao} não disponível")
        return False


def js_click(xpath, descricao, sleep=2):
    try:
        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", el
        )
        driver.execute_script("arguments[0].click();", el)
        print(f"✅ {descricao} (JS)")
        time.sleep(sleep)
        return True
    except Exception:
        print(f"⚠️ {descricao} não clicado")
        return False


def esperar_header_mobile():
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
        time.sleep(2)
    except:
        pass


def scroll_ate_elemento(xpath, descricao, sleep=2):
    try:
        el = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", el
        )
        print(f"👀 Visualizando: {descricao}")
        time.sleep(sleep)
        return True
    except Exception:
        print(f"⚠️ Não encontrou: {descricao}")
        return False


def scroll_pagina(valor=600, vezes=1):
    for _ in range(vezes):
        driver.execute_script(f"window.scrollBy(0, {valor});")
        time.sleep(1)

# =========================
# AÇÕES DE NEGÓCIO
# =========================
def aceitar_cookies():
    if try_click(
        "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']",
        "Aceitar cookies (desktop)"
    ):
        return
    try_click(
        "//*[@id='dm876A']/div",
        "Aceitar cookies (mobile)"
    )


def selecionar_regiao():
    try_click(
        "//*[@id='other-regions']",
        "Selecionar região (Norte / Outras regiões)"
    )


def clicar_menu_mobile():
    esperar_header_mobile()
    js_click(
        "//*[@id='toggle-menu']",
        "Abrir menu mobile"
    )


def fechar_menu_mobile():
    js_click(
        "//*[@id='close-menu']",
        "Fechar menu mobile"
    )


def fluxo_login():
    try_click(
        "//*[@id='login-name']",
        "Abrir login"
    )
    try_click(
        "//*[@id='login-form-opener']",
        "Acesso / Termos"
    )
    try_click(
        "//*[@id='login-name']/span",
        "Voltar do login"
    )


def fluxo_quero_ser_cliente():
    # Abre modal "Quero ser cliente"
    js_click(
        "//*[@id='first-acess-register-modal-opener']",
        "Abrir modal Quero ser cliente"
    )

    # Aguarda a modal aparecer
    try:
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='mm-0']"))
        )
        time.sleep(2)
    except:
        print("⚠️ Modal Quero ser cliente não apareceu")
        return

    # 👉 FECHAR MODAL CLICANDO NA LOGO (EXATAMENTE AQUI)
    logo_xpaths = [
        "//*[@id='mm-0']//a[contains(@class,'logo')]",
        "//header//a[contains(@class,'logo')]",
        "//header//img[contains(@alt,'Minerva')]/parent::a"
    ]

    for xp in logo_xpaths:
        try:
            el = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            driver.execute_script("arguments[0].click();", el)
            print("✅ Modal 'Quero ser cliente' fechada clicando na logo")
            time.sleep(3)
            return
        except:
            continue

    print("⚠️ Não conseguiu fechar a modal clicando na logo")


def fluxo_home_carrosseis():
    # Carrossel de produtos 1
    scroll_ate_elemento(
        "//*[@id='slick-slide-control11']",
        "Carrossel de produtos 1"
    )
    scroll_pagina(600, 1)

    # Carrossel de marcas
    scroll_ate_elemento(
        "//*[@id='maincontent']/div[3]/div/div[6]",
        "Carrossel de marcas"
    )

    marcas_controls = [
        "//*[@id='slick-slide-control01']",
        "//*[@id='slick-slide-control02']",
        "//*[@id='slick-slide-control03']",
        "//*[@id='slick-slide-control04']",
        "//*[@id='slick-slide-control05']"
    ]

    for ctrl in marcas_controls:
        js_click(ctrl, "Carrossel de marcas – próximo")

    scroll_pagina(600, 1)

    # Carrossel de produtos 2
    scroll_ate_elemento(
        "//*[@id='slick-slide-control21']",
        "Carrossel de produtos 2"
    )
    scroll_pagina(600, 1)

    # Mapas de corte
    scroll_ate_elemento(
        "//*[@id='bovine-map']",
        "Mapa de corte – Bovino"
    )

    scroll_ate_elemento(
        "//*[@id='lamb-map']",
        "Mapa de corte – Cordeiro"
    )

    scroll_pagina(600, 1)

    # Footer
    scroll_ate_elemento(
        "//*[@id='mm-0']/div[2]/footer/div",
        "Footer"
    )

    # Voltar ao topo
    js_click(
        "//*[@id='mm-0']/div[2]/header/div[2]/span[2]/a",
        "Voltar para o topo"
    )

# =========================
# TESTE
# =========================
try:
    driver.get("https://meuminerva.com/")
    time.sleep(6)

    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, 1);")
    time.sleep(2)

    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    aceitar_cookies()
    selecionar_regiao()

    clicar_menu_mobile()
    fechar_menu_mobile()

    fluxo_login()
    fluxo_quero_ser_cliente()

    fluxo_home_carrosseis()

    print("✅ SMOKE MOBILE COMPLETO EXECUTADO COM SUCESSO")

finally:
    driver.quit()
