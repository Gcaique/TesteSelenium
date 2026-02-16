import pytest
from selenium.webdriver.support import expected_conditions as EC

from locators.header import *
from locators.home import LAST_ORDERS, LAST_ITEMS
from locators.plp import *
from locators.pdp import BTN_ENTRAR_PDP, PRODUCT_TITLES

from helpers.actions import safe_click, click_when_clickable
from helpers.waiters import visible, wait_category_loaded
from helpers.plp import clear_filters_strict, sort_strict, mobile_open_category_parent_and_see_all, apply_filter_conservacao_congelado_mobile, try_go_to_page_mobile
from helpers.region import open_region_modal, select_region
from helpers.auth import expect_login_popup
from helpers.home import header_requires_login
from helpers.dropdown import  mobile_open_quero_ser_cliente_from_dropdown, mobile_open_login_modal_from_dropdown


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.deslogado
@pytest.mark.mobile
def test_1_userDeslogado_mobile(driver, setup_site, wait):

    # 1) Termos de uso (mobile: dropdown -> Acesso -> Termos)
    mobile_open_login_modal_from_dropdown(driver)
    click_when_clickable(wait, BTN_TERMS)
    click_when_clickable(wait, BTN_CLOSE_MODAL)

    # 2) Quero ser cliente (mobile: dropdown -> Quero ser cliente)
    mobile_open_quero_ser_cliente_from_dropdown(driver)
    click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)

    # 3) Scroll home e valida seções (mesmo do desktop)
    sections_xpaths = [
        "(//div[contains(@class, 'slider-products')])[1]",
        "//div[@class='brands-carousel']",
        "(//div[contains(@class, 'slider-products')])[2]",
        "//*[@class='cutting-map __home-section']",
        "//div[@class='footer-content']"
    ]
    for xp in sections_xpaths:
        el = visible(driver, (("xpath", xp)[0], xp), timeout=10)  # se seu visible aceita string/xpath, pode simplificar
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    # 4) Busca -> paginação -> filtro congelado -> limpar -> ordenação A-Z e Z-A
    wait.until(EC.visibility_of_element_located(SEARCH_INPUT)).click()
    driver.find_element(*SEARCH_INPUT).send_keys("angus")
    click_when_clickable(wait, SEE_ALL_LINK)
    wait_category_loaded(wait, driver)

    # Paginação
    assert try_go_to_page_mobile(driver, wait, "2")
    assert try_go_to_page_mobile(driver, wait, "3")

    # no mobile, antes de aplicar filtros, abre o painel “Filtro”
    assert apply_filter_conservacao_congelado_mobile(driver, wait)

    wait.until(EC.visibility_of_element_located(SORTER_SELECT))
    wait.until(EC.visibility_of_element_located(FILTER_CLEAR_ALL))

    # Limpar filtros
    assert clear_filters_strict(driver, wait, FILTER_CLEAR_ALL, timeout=15, retries=5), \
        "Busca: não consegui limpar os filtros."

    # Ordenação A-Z / Z-A
    assert sort_strict(driver, wait, SORTER_SELECT, "name_asc", timeout=12, retries=4), \
        "Busca: não consegui ordenação A-Z."
    assert sort_strict(driver, wait, SORTER_SELECT, "name_desc", timeout=12, retries=4), \
        "Busca: não consegui ordenação Z-A."

    # 5) Categoria Bovinos Premium (mobile: hambúrguer -> categoria -> Ver todos)
    mobile_open_category_parent_and_see_all(driver, wait, slug="bovinos-premium")

    wait_category_loaded(wait, driver)
    assert try_go_to_page_mobile(driver, wait, "2")
    assert try_go_to_page_mobile(driver, wait, "3")

    # abre painel “Filtro” no mobile antes de filtrar
    assert apply_filter_conservacao_congelado_mobile(driver, wait)

    # 5.3) Pescados: ordenação
    mobile_open_category_parent_and_see_all(driver, wait, slug="pescados")
    wait_category_loaded(wait, driver)
    wait.until(EC.visibility_of_element_located(SORTER_SELECT))
    assert sort_strict(driver, wait, SORTER_SELECT, "name_asc", timeout=12, retries=4)
    assert sort_strict(driver, wait, SORTER_SELECT, "name_desc", timeout=12, retries=4)

    # 6) Bovinos: acessar e tentar comprar na lista (exige login)
    mobile_open_category_parent_and_see_all(driver, wait, slug="bovinos")
    wait_category_loaded(wait, driver)

    botoes_entrar = driver.find_elements(*BTN_ENTRAR_LISTA)
    assert botoes_entrar, "Não encontrei botões 'Entrar' na listagem atual."
    btn = botoes_entrar[0]

    safe_click(driver, wait, btn)
    try:
        expect_login_popup(driver, wait, label="listagem_mobile", timeout=8, retries=0)
    except Exception:
        safe_click(driver, wait, btn)
        expect_login_popup(driver, wait, label="listagem_mobile_retry", timeout=8, retries=0)

    # fecha dropdown/modal do header (no mobile, normalmente o mesmo LOGIN_MENU fecha)
    click_when_clickable(wait, LOGIN_MENU)

    # 7) PDP (10º item) e tentar Entrar
    produtos = driver.find_elements(*PRODUCT_TITLES)
    if len(produtos) >= 10:
        safe_click(driver, wait, produtos[9])
        btn_pdp = wait.until(EC.visibility_of_element_located(BTN_ENTRAR_PDP))
        safe_click(driver, wait, btn_pdp)
        try:
            expect_login_popup(driver, wait, label="pdp_mobile", timeout=8, retries=0)
        except Exception:
            safe_click(driver, wait, btn_pdp)
            expect_login_popup(driver, wait, label="pdp_mobile_retry", timeout=8, retries=0)

    # 8) Últimos pedidos/produtos exigem login
    click_when_clickable(wait, LOGO)
    header_requires_login(driver, wait, LAST_ORDERS, label="last_orders_mobile")
    header_requires_login(driver, wait, LAST_ITEMS, label="last_items_mobile")

    # 9) Trocar região: default -> sul -> default
    open_region_modal(driver)
    select_region(wait, "sul")
    open_region_modal(driver)
    select_region(wait, "default")

    wait.until(EC.visibility_of_element_located(LOGO))
