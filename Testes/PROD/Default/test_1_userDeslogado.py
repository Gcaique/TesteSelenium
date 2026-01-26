import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait



# ====== Locators (endereços dos elementos na tela) ======
BTN_TERMS = (By.ID, "login-terms")
BTN_CLOSE_MODAL = (By.XPATH, "//button[@class='close-modal']")

BTN_QUERO_SER_CLIENTE = (By.XPATH, "//button[@id='modal-customer-open']//span[normalize-space()='Quero ser cliente']")
BTN_CLOSE_QUERO_SER_CLIENTE = (By.XPATH, "(//*[@class='modal-inner-wrap']//button[contains(@class,'action-close')])[2]")

SEARCH_INPUT = (By.ID, "minisearch-input-top-search")
SEARCH_BUTTON = (By.XPATH, "//button[@title='Buscar']//span[normalize-space()='Buscar']")

PAGES_UL = (By.XPATH, "//div[contains(@class,'pages')]//ul")
PAGE_NUMBER = lambda n: (By.XPATH, f"//div[contains(@class,'pages')]//span[normalize-space()='{n}']")

# ====== Filtros ======
FILTER_NACIONALIDADE = (By.XPATH, "//*[@id='narrow-by-list']/div[3]/div[1]/span")
FILTER_NACIONALIDADE_OPTION_1 = (By.XPATH, "//*[@id='narrow-by-list']/div[3]/div[2]/div/ol/li[1]/a/label/span[1]")

FILTER_CONSERVACAO = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[1]/span")
FILTER_CONSERVACAO_OPTION_2 = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]")

FILTER_CLEAR_ALL = (By.XPATH, "//div[contains(@class,'filter-actions')]//*[normalize-space()='Limpar Tudo']")

# ====== Ordenação ======
SORTER_SELECT = (By.ID, "sorter")
SORT_OPTION = lambda v: (By.XPATH, f"//*[@id='sorter']/option[@value='{v}']")

# ====== Login / ações protegidas ======
LOGIN_USERNAME = (By.ID, "username")

LOGO = (By.XPATH, "//a[contains(@class,'hj-header-logo')]")
LAST_ORDERS = (By.ID, "last-orders-action")
LAST_ITEMS = (By.ID, "last-items-action")

# ====== Região ======
BTN_OPEN_REGION_MODAL = (
    By.CSS_SELECTOR,
    "a.change-region-action.hj-header_change-region-action-desktop"
)
REGION_MODAL = (By.CSS_SELECTOR, "div.modal-select-region")
BTN_DEFAULT_REGION = (By.ID, "other-regions")     # visão default
BTN_SUL_REGION = (By.ID, "southern-region")

# ====== Categorias =====
CATEGORY_MENU = lambda name: (
    By.XPATH,
    f"//*[@id='nav-menu-desktop']//span[normalize-space()='{name}']"
)

# ====== Lista e PDP (login required) =====
BTN_ENTRAR_LISTA = (
    By.XPATH,
    "//a[contains(@class,'loggin-btn') and .//span[normalize-space()='Entrar']]"
)

BTN_ENTRAR_PDP = (
    By.XPATH,
    "//button[contains(@class,'loggin-btn') and contains(@class,'tget-btn-buy')]"
)


# ====== Helpers simples ======
def scroll_to(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def click_when_clickable(wait, locator):
    wait.until(EC.element_to_be_clickable(locator)).click()


def scroll_and_confirm(wait, driver, xpath: str):
    locator = (By.XPATH, xpath)
    try:
        element = wait.until(EC.visibility_of_element_located(locator))
    except TimeoutException:
        assert False, f"Elemento NÃO encontrado (ou não visível) para o XPath: {xpath}"

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    assert element.is_displayed(), f"Elemento encontrado, mas NÃO visível após scroll. XPath: {xpath}"


def try_click(wait, locator, timeout=3) -> bool:
    driver = wait._driver
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()
        return True
    except (TimeoutException, StaleElementReferenceException):
        return False


def try_visible(wait, locator, timeout=3) -> bool:
    driver = wait._driver
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        return False


def try_go_to_page(wait, driver, page_number: str, timeout=3) -> bool:
    locator = PAGE_NUMBER(page_number)
    try:
        pages = driver.find_elements(*PAGES_UL)
        if pages:
            scroll_to(driver, pages[0])

        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return True
    except (TimeoutException, StaleElementReferenceException):
        return False


def try_apply_filter(wait, open_locator, option_locator, timeout=3) -> bool:
    opened = try_click(wait, open_locator, timeout=timeout)
    if not opened:
        return False

    chosen = try_click(wait, option_locator, timeout=timeout)
    return chosen


def try_clear_filters(wait, timeout=3) -> bool:
    return try_click(wait, FILTER_CLEAR_ALL, timeout=timeout)


def try_sort(wait, driver, value: str, timeout=3) -> bool:
    # sorter existe?
    if not try_visible(wait, SORTER_SELECT, timeout=timeout):
        return False

    option_locator = SORT_OPTION(value)
    if not driver.find_elements(*option_locator):
        return False

    return try_click(wait, option_locator, timeout=timeout)


def open_region_modal(wait, driver):
    driver.execute_script("window.scrollTo(0, 0);")
    click_when_clickable(wait, BTN_OPEN_REGION_MODAL)
    wait.until(EC.visibility_of_element_located(REGION_MODAL))


def select_region(wait, region: str):
    if region == "default":
        click_when_clickable(wait, BTN_DEFAULT_REGION)
    elif region == "sul":
        click_when_clickable(wait, BTN_SUL_REGION)
    else:
        raise ValueError("region deve ser 'default' ou 'sul'")

    wait.until(EC.invisibility_of_element_located(REGION_MODAL))


def wait_category_loaded(wait, driver):
    # validação simples: campo de busca visível (página carregou)
    wait.until(EC.visibility_of_element_located(SEARCH_INPUT))


def safe_click(driver, wait, element):
    """Clica com mais robustez (viewport + fallback JS)"""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    try:
        wait.until(lambda d: element.is_displayed() and element.is_enabled())
        element.click()
    except (StaleElementReferenceException, ElementClickInterceptedException):
        driver.execute_script("arguments[0].click();", element)



def expect_login_popup(driver, wait, label="login_popup"):
    """
       Confirma que o pop-up de login abriu.
       Como você usa ID 'username', esperamos ele aparecer.
       Se falhar, salva screenshot pra você enxergar o estado real da tela.
       """
    try:
        wait.until(EC.visibility_of_element_located(LOGIN_USERNAME))
    except TimeoutException:
        driver.save_screenshot(f"debug_{label}_timeout.png")
        raise


# =========================
# TESTE
# =========================
@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.deslogado
def test_1_userDeslogado(driver, setup_site, wait):
    """
    Usuário deslogado (visão default).
    Passa por modais, scroll, busca e cenários por categoria.
    """

    # 1) Termos de uso
    click_when_clickable(wait, (By.XPATH, "//div[@id='login-name']/span"))
    click_when_clickable(wait, BTN_TERMS)
    click_when_clickable(wait, BTN_CLOSE_MODAL)

    # 2) Quero ser cliente
    click_when_clickable(wait, BTN_QUERO_SER_CLIENTE)
    click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)

    # 3) Scroll home e valida seções
    sections_xpaths = [
        "(//div[contains(@class, 'slider-products')])[1]",
        "//div[@class='brands-carousel']",
        "(//div[contains(@class, 'slider-products')])[2]",
        "//*[@class='cutting-map __home-section']",
        "//div[@class='footer-content']"
    ]
    for xp in sections_xpaths:
        scroll_and_confirm(wait, driver, xp)

    # 4) Busca simples
    wait.until(EC.visibility_of_element_located(SEARCH_INPUT)).click()
    driver.find_element(*SEARCH_INPUT).send_keys("angus")
    click_when_clickable(wait, SEARCH_BUTTON)
    try_visible(wait, PAGES_UL, timeout=5)


    # 5) Cenários por categoria
    # 5.1 Bovinos Premium: paginação 2 e 3 (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Bovinos Premium"))
    wait_category_loaded(wait, driver)
    try_go_to_page(wait, driver, "2", timeout=4)
    try_go_to_page(wait, driver, "3", timeout=4)

    # 5.2 Promo: filtros Nacionalidade + Conservação (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Promoções"))
    wait_category_loaded(wait, driver)

    try_apply_filter(wait, FILTER_NACIONALIDADE, FILTER_NACIONALIDADE_OPTION_1, timeout=5)
    try_apply_filter(wait, FILTER_CONSERVACAO, FILTER_CONSERVACAO_OPTION_2, timeout=5)

    # se aplicar filtro, tenta limpar (sem travar)
    try_clear_filters(wait, timeout=4)

    # 5.3 Pescados: ordenação (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Pescados"))
    wait_category_loaded(wait, driver)

    try_sort(wait, driver, "name_asc", timeout=4)
    try_sort(wait, driver, "name_desc", timeout=4)

    # 5.4 Bovinos: apenas acessar
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    # 6) Tentativa de compra na lista (exige login) — sem travar se não existir botão
    botoes_entrar = driver.find_elements(*BTN_ENTRAR_LISTA)

    if not botoes_entrar:
        raise AssertionError("Não encontrei botões 'Entrar' na listagem atual.")

    abriu = False

    # tenta alguns botões (evita depender do índice 9 que pode estar fora do viewport)
    for btn in botoes_entrar[:10]:
        safe_click(driver, wait, btn)

        try:
            expect_login_popup(driver, wait, "listagem")  # ou "pdp"
            abriu = True
            break
        except TimeoutException:
            # não abriu com esse botão, tenta o próximo
            continue

    if not abriu:
        driver.save_screenshot("debug_entrar_nao_abriu_login.png")
        raise AssertionError("Cliquei em botões 'Entrar', mas o pop-up do header com #username não apareceu.")

    # segue o fluxo
    click_when_clickable(wait, (By.XPATH, "//div[@id='login-name']/span"))

    # 7) PDP de um produto (se houver produtos suficientes)
    produtos = driver.find_elements(By.XPATH, "//*[contains(@id,'product-item-info')]//strong")
    if len(produtos) >= 10:
        produtos[9].click()
        wait.until(EC.visibility_of_element_located(BTN_ENTRAR_PDP))
        click_when_clickable(wait, BTN_ENTRAR_PDP)
        expect_login_popup(driver, wait, "pdp")

    else:
        print("[WARN] Não há produtos suficientes para abrir a PDP (10º item).")

    # 8) Últimos pedidos/produtos exigem login
    click_when_clickable(wait, LOGO)

    for item in [LAST_ORDERS, LAST_ITEMS]:
        if try_click(wait, item, timeout=5):
            expect_login_popup(driver, wait, label="header_last_orders_items")
            click_when_clickable(wait, (By.XPATH, "//div[@id='login-name']/span"))

    # 9) Trocar região: default -> sul -> default (obrigatório)
    open_region_modal(wait, driver)
    select_region(wait, "sul")

    open_region_modal(wait, driver)
    select_region(wait, "default")

    # Assert final
    wait.until(EC.visibility_of_element_located(LOGO))
