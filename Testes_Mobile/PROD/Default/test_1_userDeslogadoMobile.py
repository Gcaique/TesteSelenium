import time

import pytest
from selenium.webdriver.support import expected_conditions as EC

from locators.header import *
from locators.home import LAST_ORDERS, LAST_ITEMS
from locators.plp import *
from locators.pdp import BTN_ENTRAR_PDP, PRODUCT_TITLES

from helpers.actions import safe_click, click_when_clickable, safe_click_loc_retry, scroll_into_view
from helpers.waiters import visible, wait_category_loaded
from helpers.plp import clear_filters_strict, sort_strict, apply_filter_conservacao_congelado_mobile, try_go_to_page_mobile
from helpers.region import open_region_modal_mobile, select_region
from helpers.auth import expect_login_popup_mobile
from helpers.home import header_requires_login_mobile, go_home
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
    time.sleep(3)
    assert sort_strict(driver, wait, SORTER_SELECT, "name_desc", timeout=12, retries=4), \
        "Busca: não consegui ordenação Z-A."
    time.sleep(3)

    # 5) Categoria Bovinos Premium (mobile: hambúrguer -> categoria -> Ver todos)
    go_home(driver)
    time.sleep(5)
    safe_click_loc_retry(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    safe_click_loc_retry(driver, MOBILE_MENU_PARENT_NEXT("bovinos-premium"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    safe_click_loc_retry(driver, MOBILE_MENU_SEE_ALL, retries=4, sleep_between=0.25)

    # paginação
    wait_category_loaded(wait, driver)
    assert try_go_to_page_mobile(driver, wait, "2")
    assert try_go_to_page_mobile(driver, wait, "3")

    # abre painel “Filtro” no mobile antes de filtrar
    assert apply_filter_conservacao_congelado_mobile(driver, wait)

    wait.until(EC.visibility_of_element_located(SORTER_SELECT))
    wait.until(EC.visibility_of_element_located(FILTER_CLEAR_ALL))

    assert clear_filters_strict(driver, wait, FILTER_CLEAR_ALL, timeout=15, retries=5), \
        "Não consegui limpar os filtros."

    # 6) Pescados: ordenação
    safe_click_loc_retry(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    safe_click_loc_retry(driver, MOBILE_MENU_PARENT_NEXT("pescados"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    safe_click_loc_retry(driver, MOBILE_MENU_SEE_ALL, retries=4, sleep_between=0.25)
    wait_category_loaded(wait, driver)
    wait.until(EC.visibility_of_element_located(SORTER_SELECT))
    assert sort_strict(driver, wait, SORTER_SELECT, "name_asc", timeout=12, retries=4)
    time.sleep(3)
    assert sort_strict(driver, wait, SORTER_SELECT, "name_desc", timeout=12, retries=4)
    time.sleep(3)

    # 7) Bovinos: acessar e tentar comprar na lista (exige login)
    safe_click_loc_retry(driver, MOBILE_MENU_HAMBURGER, timeout=10, retries=4, sleep_between=0.25)
    time.sleep(2)
    safe_click_loc_retry(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), timeout=10, retries=4, sleep_between=0.25)
    time.sleep(1)
    safe_click_loc_retry(driver, MOBILE_MENU_SEE_ALL, retries=4, sleep_between=0.25)
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, MOBILE_BTN_ENTRAR_LISTA(1), timeout=10)

    safe_click_loc_retry(driver, MOBILE_BTN_ENTRAR_LISTA(1), retries=4, sleep_between=0.25)
    expect_login_popup_mobile(driver, wait, timeout=8)

    # fecha dropdown/modal do header (no mobile, normalmente o mesmo LOGIN_MENU fecha)
    click_when_clickable(wait, LOGIN_MENU)

    # 8) PDP (10º item) e tentar Entrar
    scroll_into_view(driver, PLP_PRODUCT_IMAGE_WRAPPER_BY_INDEX(9), timeout=8)
    safe_click_loc_retry(driver, PLP_PRODUCT_IMAGE_WRAPPER_BY_INDEX(9), timeout=10, retries=4, sleep_between=0.25)
    btn_pdp = wait.until(EC.visibility_of_element_located(BTN_ENTRAR_PDP))
    safe_click_loc_retry(driver, btn_pdp, timeout=10, retries=4, sleep_between=0.25)
    try:
        expect_login_popup_mobile(driver, wait, timeout=8)
    except Exception:
        safe_click_loc_retry(driver, btn_pdp, timeout=10, retries=4, sleep_between=0.25)
        expect_login_popup_mobile(driver, wait, timeout=8)

    # 9) Últimos pedidos/produtos exigem login
    click_when_clickable(wait, LOGO)
    header_requires_login_mobile(driver, wait, LAST_ORDERS, label="last_orders_mobile")
    header_requires_login_mobile(driver, wait, LAST_ITEMS, label="last_items_mobile")

    # 10) Trocar região: default -> sul -> default
    open_region_modal_mobile(driver)
    select_region(wait, "sul")
    open_region_modal_mobile(driver)
    select_region(wait, "default")

    wait.until(EC.visibility_of_element_located(LOGO))
