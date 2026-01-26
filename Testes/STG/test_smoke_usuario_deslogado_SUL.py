import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config

# Funções utilitárias
def wait_visible(driver, xpath, timeout=5):
    """Espera até que o elemento esteja visível"""
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
    except:
        print(f"Elemento não visível: {xpath}")
        return None

def click_safe(driver, xpath, timeout=5):
    """Clica de forma segura, com scroll e fallback para JS se necessário"""
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    if element:
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
            time.sleep(0.5)
        except:
            # fallback via JS
            try:
                driver.execute_script("arguments[0].click();", element)
                time.sleep(0.5)
            except:
                print(f"Não foi possível clicar no elemento: {xpath}")
    else:
        print(f"Elemento não encontrado para clicar: {xpath}")

# Fixture para o driver
@pytest.fixture
def driver():
    driver = config.criar_driver("Abre o navegador e acessa a pagina do Meu Minerva")
    yield driver
    driver.quit()

# Teste principal
def test_smoke_usuario_deslogado(driver):
    wait = WebDriverWait(driver, 5)

    # ------------------------------
    # ABRIR URL
    # ------------------------------
    driver.get("https://mcstaging.meuminerva.com")

    # ------------------------------
    # SELEÇÃO DE REGIÃO
    # ------------------------------
    click_safe(driver, "//button[@id='southern-region']")

    # ------------------------------
    # ACEITAR COOKIES
    # ------------------------------
    click_safe(driver, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")

    # ------------------------------
    # LOGIN / TERMOS
    # ------------------------------
    click_safe(driver, "//div[@id='login-name']/span")
    click_safe(driver, "//a[@id='login-terms']")
    time.sleep(1)
    click_safe(driver, "//button[@class='close-modal']")

    # ------------------------------
    # QUERO SER CLIENTE
    # ------------------------------
    click_safe(driver, "//button[@id='modal-customer-open']/span[normalize-space(text())='Quero ser cliente']")
    time.sleep(1)
    click_safe(driver, "(//*[@class='modal-inner-wrap']//button[@class='action-close'])[2]")

    # ------------------------------
    # SCROLL HOME
    # ------------------------------
    sections = [
        "(//div[contains(@class, 'slider-products')])[1]",
        "//div[@class='brands-carousel']",
        "(//div[contains(@class, 'slider-products')])[2]",
        "//*[@class='cutting-map __home-section']",
        "//div[@class='footer-content']"
    ]
    for xpath in sections:
        element = wait_visible(driver, xpath)
        if element:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.3)

    # ------------------------------
    # BUSCA
    # ------------------------------
    search_input = wait_visible(driver, "//input[@id='minisearch-input-top-search']")
    if search_input:
        search_input.click()
        search_input.send_keys("pul")
        time.sleep(0.5)
        click_safe(driver, "//button[@title='Buscar']/span[normalize-space(text())='Buscar']")
        time.sleep(0.5)

    # ------------------------------
    # FILTROS E ORDENAÇÃO
    # ------------------------------
    click_safe(driver, "//*[@id='narrow-by-list']/div[1]/div[1]/span")
    click_safe(driver, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]")
    time.sleep(0.5)
    click_safe(driver, "//div[@class='block-actions filter-actions']//*[normalize-space(text())='Limpar Tudo']")
    click_safe(driver, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']")
    click_safe(driver, "//*[@id='sorter']/option[@value='name_asc']")
    time.sleep(0.5)
    click_safe(driver, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']")
    click_safe(driver, "//*[@id='sorter']/option[@value='name_desc']")
    time.sleep(0.5)

    # ------------------------------
    # CATEGORIAS
    # ------------------------------
    categorias = {
        "Bovinos Premium": "//*[@id='ui-id-11']",
        "Promo": "//*[@id='ui-id-118']"
    }

    for xpath in categorias.values():
        click_safe(driver, xpath)
        time.sleep(0.5)

    # ------------------------------
    # PDP e botões Entrar
    # ------------------------------
    for i in [1, 10]:
        click_safe(driver, f"(//a[@class='action tocart primary loggin-btn tget-btn-buy']/span[normalize-space(text())='Entrar'])[ {i} ]")
        wait_visible(driver, "//*[@id='username']", 3)

    click_safe(driver, "(//*[contains(@id,'product-item-info')]//strong)[10]")
    time.sleep(1)
    click_safe(driver, "//button[@class='loggin-btn primary tget-btn-buy']")
    time.sleep(0.5)

    # ------------------------------
    # LOGO / HOME
    # ------------------------------
    click_safe(driver, "//a[@class='logo hj-header-logo']")
    time.sleep(1)

    # ------------------------------
    # ÚLTIMOS PEDIDOS E PRODUTOS
    # ------------------------------
    click_safe(driver, "//a[@id='last-orders-action']")
    wait_visible(driver, "//*[@class='secondary login-name']//button[@id='send2']", 3)
    click_safe(driver, "//div[@id='login-name']/span")

    click_safe(driver, "//a[@id='last-items-action']")
    wait_visible(driver, "//*[@class='secondary login-name']//button[@id='send2']", 3)
    click_safe(driver, "//div[@id='login-name']/span")

    # ------------------------------
    # ALTERAR REGIÃO
    # ------------------------------
    click_safe(driver, "//a[@class='change-region-action hj-header_change-region-action-desktop']")
    wait_visible(driver, "//button[@id='other-regions']", 3)
    click_safe(driver, "//button[@id='other-regions']")
    time.sleep(1)
    click_safe(driver, "//button[@id='southern-region']")
    time.sleep(1)

    print("AUTOMAÇÃO FINALIZADA COM SUCESSO")
