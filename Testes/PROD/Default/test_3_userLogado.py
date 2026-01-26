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
VALID_USER = "hub.teste2-bruno-popup@minervafoods.com"
VALID_PASS = "Min@1234"

# =========================
# Locators (base)
# =========================

# Cookies / Região
COOKIE_ACCEPT = (By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")
BTN_DEFAULT_REGION = (By.ID, "other-regions")
BTN_SUL_REGION = (By.ID, "southern-region")

# Login (modal no header)
LOGIN_MENU = (By.XPATH, "//div[@id='login-name']/span")
LOGIN_NAME_CONTAINER = (By.ID, "login-name")  # área do usuário (logado)
USERNAME_INPUT = (By.ID, "username")
PASSWORD_INPUT = (By.XPATH, "//*[@name='login[password]']")
BTN_AVANCAR = (By.ID, "send2")

# Indicador de LOGADO (fonte da verdade)
MINICART_WRAPPER = (By.XPATH, "//*[@data-block='minicart' and contains(@class,'minicart-wrapper')]")

# Spin to win / Hotjar (pode variar)
SPIN_CLOSE = (By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button")
HOTJAR_CLOSE = (By.XPATH, "//dialog//button")  # fallback (se aparecer)

# Header / região / minicart
REGION_OPEN = (By.XPATH, "//a[contains(@class,'change-region-action') and contains(@class,'hj-header_change-region-action-desktop')]")
MINICART_ICON = (By.XPATH, "//*[@class='action showcart']")
MINICART_ACTIVE = (By.XPATH, "//*[@class='action showcart active']")
MINICART_CLOSE = (By.ID, "btn-minicart-close")

# Busca
SEARCH_INPUT = (By.ID, "minisearch-input-top-search")
SEE_ALL_LINK = (By.XPATH, "//a[@class='see-all-link']")
SEARCH_SUGGEST_ADD_2 = (By.XPATH, "(//div[@class='product-add-to-cart ']//button)[2]")

# Paginação / filtros / ordenação
PAGINA_2 = (By.XPATH, "//div[@class='pages']//ul//span[normalize-space(text())='2']")
FILTER_CONSERVACAO_OPEN = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[1]/span")
FILTER_CONSERVACAO_RESFRIADO = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]")
FILTER_MARCA_OPEN = (By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[1]")
FILTER_MARCA_OPT1 = (By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[2]/div/ol/li[1]/a/label/span[1]")
FILTER_CLEAR_ALL = (By.XPATH, "//div[@class='block-actions filter-actions']//*[normalize-space(text())='Limpar Tudo']")

SORTER_SELECT = (By.ID, "sorter")
SORT_LOW_TO_HIGH = (By.XPATH, "//*[@id='sorter']/option[@value='low_to_high']")
SORT_HIGH_TO_LOW = (By.XPATH, "//*[@id='sorter']/option[@value='high_to_low']")

# Categorias
CATEGORY_PROMOCOES = (By.XPATH, "//*[@id='nav-menu-desktop']//span[contains(normalize-space(text()), 'Promo')]")
CATEGORY_PESCADOS = (By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Pescados']")
CATEGORY_CORDEIROS = (By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Cordeiros']")

# Produto / carrossel / adicionar (home)
CAROUSEL_1 = (By.XPATH, "(//div[contains(@class, 'slider-products')])[1]")
QTY_INPUT_FIRST = (By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]")
ADD_BTN_FIRST_CAROUSEL = (By.XPATH, "(//*[@class='slick-slide slick-current slick-active']//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]")

# Loading minicart
MINICART_LOADING_1 = (By.XPATH, "//*[@class='minicart-wrapper is-loading active']")
MINICART_LOADING_2 = (By.XPATH, "//*[@class='minicart-wrapper active is-loading']")

# PDP pescados
PESCADOS_FIRST_PRODUCT = (By.XPATH, "(//*[contains(@id,'product-item-info')]//span[@class='product-image-wrapper'])[1]")
PDP_INCREMENT = (By.XPATH, "(//button[@class='increment-qty hj-product_card-increment_qty'])[1]")
PDP_ADD_TO_CART = (By.ID, "product-addtocart-button")

# Previsão de entrega (PDP)
ADDRESSES_SELECT = (By.ID, "addresses")
ADDRESSES_OPT2 = (By.XPATH, "//*[@id='addresses']/option[2]")
BTN_VERIFY_FORECAST = (By.ID, "verify-delivery-forecast")
FORECAST_RESULT = (By.XPATH, "//*[@class='shipping-rate-result']")

# Avise-me (vale para PLP e PDP) - no site é <a id="button_disabled_XXXX"> / <a id="button_enabled_XXXX">
AVISE_DISABLED_ANY = (By.CSS_SELECTOR, "a[id^='button_disabled_']")
AVISE_ENABLED_ANY  = (By.CSS_SELECTOR, "a[id^='button_enabled_']")

# Carrinho
VIEWCART = (By.XPATH, "//a[@class='action viewcart']")
EMPTY_CART_BTN = (By.XPATH, "//button[@id='empty_cart_button']/span")
EMPTY_CART_CONFIRM = (By.XPATH, "//button[@class='action-primary action-accept']")
VER_CATALOGO = (By.XPATH, "//a[@class='action primary']")

# Dropdown do usuário (links)
DD_MINHA_CONTA = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Minha conta']")
DD_COMPARAR = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Comparar produtos']")
DD_MEUS_PEDIDOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pedidos']")
DD_FAVORITOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Lista de favoritos']")
DD_MEUS_PONTOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pontos']")
DD_MEUS_CUPONS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus cupons']")
DD_MINHAS_MISSOES = (By.XPATH, "//*[@id='login-dropdown']//a[contains(normalize-space(text()), 'Minhas miss')]")


# =========================
# Helpers (mesma lógica; só removido o que não era usado)
# =========================

# Cria WebDriverWait padrão com polling rápido
def wait(driver, timeout=10, poll=0.1):
    return WebDriverWait(driver, timeout, poll_frequency=poll)

# Espera um elemento ficar visível
def visible(driver, locator, timeout=10):
    return wait(driver, timeout).until(EC.visibility_of_element_located(locator))

# Espera um elemento ficar clicável
def clickable(driver, locator, timeout=10):
    return wait(driver, timeout).until(EC.element_to_be_clickable(locator))

# Clique robusto (normal -> fallback JS em intercept/stale)
def click(driver, locator, timeout=10):
    el = clickable(driver, locator, timeout)
    try:
        el.click()
    except (ElementClickInterceptedException, StaleElementReferenceException):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        driver.execute_script("arguments[0].click();", el)

# Preenche input (clear -> send_keys; fallback JS para limpar)
def fill(driver, locator, value: str):
    el = visible(driver, locator, timeout=10)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)
    el.send_keys(value)

# Faz scroll até um elemento (por locator) e retorna o elemento
def scroll_into_view(driver, locator, timeout=10):
    el = visible(driver, locator, timeout=timeout)
    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", el)
    return el

# Tenta clicar sem quebrar o teste (usado para fechar popups)
def try_click(driver, locator, timeout=2.0) -> bool:
    try:
        click(driver, locator, timeout=timeout)
        return True
    except Exception:
        return False

# Fecha popups ocasionais (spin/hotjar)
def try_close_popups(driver):
    try_click(driver, SPIN_CLOSE, timeout=1.5)
    try_click(driver, HOTJAR_CLOSE, timeout=1.5)

# Fonte da verdade para LOGADO: minicart visível
def minicart_visible(driver) -> bool:
    try:
        el = wait(driver, 1.5).until(EC.visibility_of_element_located(MINICART_WRAPPER))
        return el.is_displayed()
    except Exception:
        return False


# Garante login (se já estiver logado, só fecha popups)
def ensure_logged_in(driver, user: str, passwd: str):
    if minicart_visible(driver):
        try_close_popups(driver)
        return

    # abre login
    click(driver, LOGIN_MENU, timeout=10)
    visible(driver, USERNAME_INPUT, timeout=10)

    # username -> avançar
    fill(driver, USERNAME_INPUT, user)
    click(driver, BTN_AVANCAR, timeout=10)

    # senha -> avançar
    visible(driver, PASSWORD_INPUT, timeout=10)
    fill(driver, PASSWORD_INPUT, passwd)
    click(driver, BTN_AVANCAR, timeout=10)

    # confirma login pela "fonte da verdade"
    end = time.time() + 20
    while time.time() < end:
        if minicart_visible(driver):
            try_close_popups(driver)
            return
        time.sleep(0.2)

    driver.save_screenshot("debug_login_failed.png")
    raise TimeoutException("Login não confirmou: mini-cart não ficou visível.")

# Abre dropdown do usuário (área do login-name)
def open_user_dropdown(driver):
    click(driver, LOGIN_NAME_CONTAINER, timeout=10)
    time.sleep(0.5)  # dropdown render

# Abre um item do dropdown (Minha conta, Comparar, etc.)
def open_dropdown_item(driver, locator, timeout=10):
    open_user_dropdown(driver)
    click(driver, locator, timeout=timeout)

# Abre modal de troca de região
def open_region_modal(driver):
    click(driver, REGION_OPEN, timeout=10)
    visible(driver, BTN_SUL_REGION, timeout=10)  # garante modal ok (um dos botões)

# Troca região (default <-> sul) e espera header estabilizar
def switch_region(driver, to: str):
    open_region_modal(driver)
    if to == "sul":
        click(driver, BTN_SUL_REGION, timeout=10)
    elif to == "default":
        click(driver, BTN_DEFAULT_REGION, timeout=10)
    else:
        raise ValueError("to deve ser 'sul' ou 'default'")
    visible(driver, SEARCH_INPUT, timeout=15)

# Espera loading do minicart (duas variações de classe no site)
def wait_minicart_loading(driver):
    try:
        wait(driver, 8).until(EC.visibility_of_element_located(MINICART_LOADING_2))
    except Exception:
        pass
    try:
        wait(driver, 20).until(EC.invisibility_of_element_located(MINICART_LOADING_2))
    except Exception:
        pass

    try:
        wait(driver, 8).until(EC.visibility_of_element_located(MINICART_LOADING_1))
    except Exception:
        pass
    try:
        wait(driver, 20).until(EC.invisibility_of_element_located(MINICART_LOADING_1))
    except Exception:
        pass

# Espera "algum" elemento visível de um locator (sem exception; retorna None se não achar)
def wait_any_visible(driver, locator, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        els = driver.find_elements(*locator)
        for e in els:
            try:
                if e.is_displayed():
                    return e
            except Exception:
                pass
        time.sleep(0.2)
    return None

# Scroll até um elemento já encontrado e clica nele
def scroll_and_click(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    time.sleep(0.3)
    el.click()

# Abre a PDP a partir do PRIMEIRO Avise-me visível na PLP (usa closest card + querySelector)
def open_pdp_from_first_avise_in_plp(driver):
    visible(driver, SORTER_SELECT, timeout=25)

    avise = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=5)
    if not avise:
        avise = wait_any_visible(driver, AVISE_ENABLED_ANY, timeout=2)
    if not avise:
        return False

    # sobe até o card do produto
    card = driver.execute_script("return arguments[0].closest('[id^=\"product-item-info_\"]');", avise)
    if not card:
        return False

    # tenta clicar no link do nome do produto / foto
    link = driver.execute_script(
        "return arguments[0].querySelector('a.product-item-link, a.product-item-photo');",
        card
    )
    if not link:
        # fallback: imagem
        link = driver.execute_script("return arguments[0].querySelector('span.product-image-wrapper');", card)
        if not link:
            return False

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", link)
    return True

def wait_visible_any(driver, locators, timeout=25, poll=0.2):
    """
    Espera até QUALQUER um dos locators ficar visível.
    Retorna o WebElement visível encontrado.
    """
    end = time.time() + timeout
    while time.time() < end:
        for loc in locators:
            els = driver.find_elements(*loc)
            for el in els:
                try:
                    if el.is_displayed():
                        return el
                except Exception:
                    pass
        time.sleep(poll)
    raise TimeoutException(f"Nenhum locator ficou visível: {locators}")

def toggle_avise_me_requires_refresh(driver, page_ready_locator=None, timeout=25, wait_click_class=False):
    # READY da página
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(driver, [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY], timeout=timeout)

    # 1) clica no disabled
    disabled = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=timeout)
    if not disabled:
        return False

    scroll_and_click(driver, disabled)

    # Só espera a classe mudar se você pedir (PDP)
    if wait_click_class:
        wait(driver, timeout).until(
            lambda d: any(
                ("alert-active" in (e.get_attribute("class") or "") and "clicked" in (e.get_attribute("class") or ""))
                for e in d.find_elements(*AVISE_DISABLED_ANY)
            )
        )

    # 2) refresh e espera enabled aparecer
    driver.refresh()
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(driver, [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY], timeout=timeout)

    enabled = wait_any_visible(driver, AVISE_ENABLED_ANY, timeout=timeout)
    if not enabled:
        return False

    scroll_and_click(driver, enabled)

    if wait_click_class:
        wait(driver, timeout).until(
            lambda d: any(
                ("alert-active" in (e.get_attribute("class") or "") and "clicked" in (e.get_attribute("class") or ""))
                for e in d.find_elements(*AVISE_ENABLED_ANY)
            )
        )

    # 4) refresh e espera disabled voltar
    driver.refresh()
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(driver, [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY], timeout=timeout)

    disabled2 = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=timeout)
    return bool(disabled2)


def wait_minicart_ready(driver, timeout=20):
    # espera qualquer loading sumir (você já tem essa função)
    wait_minicart_loading(driver)

    # garante que o minicart esteja aberto (active), senão abre
    if not driver.find_elements(*MINICART_ACTIVE):
        click(driver, MINICART_ICON, timeout=10)
        visible(driver, MINICART_ACTIVE, timeout=10)

    # garante que o link "Ver carrinho" esteja visível
    visible(driver, VIEWCART, timeout=timeout)


# =========================
# TESTE
# =========================
@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.logado
def test_3_userLogado(driver, setup_site):
    """
    Usuário LOGADO (default):
    - login
    - navega itens do dropdown do usuário
    - troca região (default <-> sul)
    - abre/fecha minicart
    - interações de compra/busca/categoria/pdp/filtros/ordenacao
    - avise-me (PLP e PDP, com refresh obrigatório)
    - limpa carrinho
    """

    visible(driver, SEARCH_INPUT, timeout=20)

    # 1) Login (fonte da verdade = mini-cart)
    ensure_logged_in(driver, VALID_USER, VALID_PASS)

    # 2) Dropdown do usuário (seus itens)
    open_dropdown_item(driver, DD_MINHA_CONTA, timeout=15)
    visible(driver, SEARCH_INPUT, timeout=20)

    open_dropdown_item(driver, DD_COMPARAR, timeout=15)
    open_dropdown_item(driver, DD_MEUS_PEDIDOS, timeout=15)
    open_dropdown_item(driver, DD_FAVORITOS, timeout=15)
    open_dropdown_item(driver, DD_MEUS_PONTOS, timeout=15)
    open_dropdown_item(driver, DD_MEUS_CUPONS, timeout=15)
    open_dropdown_item(driver, DD_MINHAS_MISSOES, timeout=15)

    # 3) Troca de região: default -> sul -> default
    switch_region(driver, "sul")
    switch_region(driver, "default")

    # 4) Mini-cart abre/fecha
    click(driver, MINICART_ICON, timeout=10)
    visible(driver, MINICART_ACTIVE, timeout=10)
    click(driver, MINICART_CLOSE, timeout=10)
    visible(driver, MINICART_ICON, timeout=10)

    # 5) Carrossel 1: tenta alterar qty e adicionar
    scroll_into_view(driver, CAROUSEL_1, timeout=15)
    click(driver, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "0")
    scroll_into_view(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    click(driver, ADD_BTN_FIRST_CAROUSEL, timeout=10)
    wait_minicart_loading(driver)

    # 6) Busca: "suino" e add pelo suggestion
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "suino")
    visible(driver, SEARCH_SUGGEST_ADD_2, timeout=20)
    click(driver, SEARCH_SUGGEST_ADD_2, timeout=10)
    wait_minicart_loading(driver)

    # 7) Busca: pack -> carne -> ver todos
    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "pack")
    visible(driver, SEE_ALL_LINK, timeout=20)

    click(driver, SEARCH_INPUT, timeout=10)
    fill(driver, SEARCH_INPUT, "carne")
    visible(driver, SEE_ALL_LINK, timeout=20)
    click(driver, SEE_ALL_LINK, timeout=10)

    # paginação e filtros / ordenação
    click(driver, PAGINA_2, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    click(driver, FILTER_CONSERVACAO_OPEN, timeout=10)
    click(driver, FILTER_CONSERVACAO_RESFRIADO, timeout=10)
    visible(driver, SORTER_SELECT, timeout=20)

    # filtro marca (se existir)
    if driver.find_elements(*FILTER_MARCA_OPEN):
        click(driver, FILTER_MARCA_OPEN, timeout=8)
        if driver.find_elements(*FILTER_MARCA_OPT1):
            click(driver, FILTER_MARCA_OPT1, timeout=8)

    # limpar filtros
    click(driver, FILTER_CLEAR_ALL, timeout=15)

    # ordenação (low -> high -> high -> low)
    click(driver, SORTER_SELECT, timeout=10)
    click(driver, SORT_LOW_TO_HIGH, timeout=10)
    click(driver, SORTER_SELECT, timeout=10)
    click(driver, SORT_HIGH_TO_LOW, timeout=10)

    # add primeiro da lista
    click(driver, (By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]"), timeout=10)
    wait_minicart_loading(driver)

    # 8) Promoções: adicionar item
    click(driver, CATEGORY_PROMOCOES, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    click(driver, QTY_INPUT_FIRST, timeout=10)
    fill(driver, QTY_INPUT_FIRST, "2")
    click(driver, (By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]"), timeout=10)
    wait_minicart_loading(driver)

    # 9) Pescados -> PDP -> add -> previsão entrega
    click(driver, CATEGORY_PESCADOS, timeout=15)
    visible(driver, PESCADOS_FIRST_PRODUCT, timeout=20)
    click(driver, PESCADOS_FIRST_PRODUCT, timeout=15)

    visible(driver, PDP_ADD_TO_CART, timeout=20)
    click(driver, PDP_INCREMENT, timeout=10)
    click(driver, PDP_ADD_TO_CART, timeout=10)
    wait_minicart_loading(driver)

    # previsão entrega
    click(driver, ADDRESSES_SELECT, timeout=10)
    click(driver, ADDRESSES_OPT2, timeout=10)
    click(driver, BTN_VERIFY_FORECAST, timeout=10)
    visible(driver, FORECAST_RESULT, timeout=20)

    # 10) Cordeiros -> página 2
    click(driver, CATEGORY_CORDEIROS, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    click(driver, PAGINA_2, timeout=15)
    visible(driver, SORTER_SELECT, timeout=20)

    # PLP: toggle avise-me (ready = sorter)
    ok_plp = toggle_avise_me_requires_refresh(driver, page_ready_locator=SORTER_SELECT)
    if not ok_plp:
        print("[WARN] PLP: não achei Avise-me para testar.")

    # PDP: abrir PDP do primeiro produto que tenha avise-me e repetir o teste
    if open_pdp_from_first_avise_in_plp(driver):
        ok_pdp = toggle_avise_me_requires_refresh(driver, page_ready_locator=None, wait_click_class=True)
        if not ok_pdp:
            print("[WARN] PDP: não consegui alternar Avise-me.")
    else:
        print("[WARN] Não consegui abrir PDP a partir de um produto com Avise-me.")

    # 12) Limpar carrinho (view cart -> empty -> confirm -> ver catálogo)
    wait_minicart_ready(driver, timeout=25)
    click(driver, VIEWCART, timeout=15)
    # carrinho às vezes demora renderizar
    visible(driver, EMPTY_CART_BTN, timeout=25)
    click(driver, EMPTY_CART_BTN, timeout=10)
    visible(driver, EMPTY_CART_CONFIRM, timeout=10)
    click(driver, EMPTY_CART_CONFIRM, timeout=10)
    visible(driver, VER_CATALOGO, timeout=15)
    click(driver, VER_CATALOGO, timeout=10)

    # assert final: ainda logado
    assert minicart_visible(driver), "Era para terminar o teste logado, mas mini-cart não está visível."
