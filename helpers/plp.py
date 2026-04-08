import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException, WebDriverException)
from selenium.webdriver.support.ui import Select

from locators.plp import *
from locators.wishlist import *
from locators.header import SEARCH_INPUT, SEARCH_BUTTON, SEARCH_SUGGEST_ADD_2, MOBILE_SEARCH_SUGGEST_ADD_1, MOBILE_SEARCH_BUTTON


from helpers.actions import (
    try_click,
    safe_click_loc,
    scroll_to,
    click_when_clickable,
    scroll_into_view,
    mobile_click_strict,
    _resolve_wait)
from helpers.waiters import try_visible, visible, DEFAULT_TIMEOUT, _effective_timeout
from helpers.wishlist import wait_favorite_status
from helpers.avise_me import open_pdp_from_first_avise_in_plp



def try_apply_filter(driver, wait, open_locator, option_locator, timeout=None) -> bool:
    w = _resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT)
    opened = try_click(driver, open_locator, timeout=timeout, wait=w)
    if not opened:
        return False

    chosen = try_click(driver, option_locator, timeout=timeout, wait=w)
    return chosen


def try_clear_filters(driver, wait, timeout=None) -> bool:
    w = _resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT)
    return try_click(driver, FILTER_CLEAR_ALL, timeout=timeout, wait=w)


def try_sort(driver, wait, value: str, timeout=None) -> bool:
    # sorter existe?
    if not try_visible(wait, SORTER_SELECT, timeout=timeout or DEFAULT_TIMEOUT):
        return False

    option_locator = SORT_OPTION(value)
    if not driver.find_elements(*option_locator):
        return False

    return try_click(driver, option_locator, timeout=timeout, wait=_resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT))


def try_go_to_page(driver, wait, page_number: str, timeout=None) -> bool:
    """Tenta paginar (sem travar). Retorna True/False."""
    effective = timeout or getattr(wait, "_timeout", DEFAULT_TIMEOUT)
    locator = PAGE_NUMBER(page_number)
    try:
        pages = driver.find_elements(*PAGES_UL)
        if pages:
            scroll_to(driver, pages[0])

        WebDriverWait(driver, effective).until(EC.element_to_be_clickable(locator)).click()
        WebDriverWait(driver, effective).until(EC.visibility_of_element_located(locator))
        return True
    except (TimeoutException, StaleElementReferenceException):
        return False

def apply_filter_strict(driver, wait, open_locator, option_locator, timeout=None, retries=4) -> bool:
    """
    Abre um filtro e clica na opção, garantindo que a opção ficou visível antes do clique.
    Não altera locators. Não depende do try_apply_filter().
    """
    last_exc = None

    for _ in range(retries):
        try:
            # garante que o "open" está na tela
            el_open = _resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT).until(EC.visibility_of_element_located(open_locator))
            scroll_to(driver, el_open)

            # abre o acordeão
            click_when_clickable(wait, open_locator)

            # garante que a opção apareceu
            local_wait = _resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT)
            local_wait.until(EC.visibility_of_element_located(option_locator))
            click_when_clickable(local_wait, option_locator)

            return True
        except Exception as e:
            last_exc = e
            time.sleep(0.6)

    return False


def clear_filters_strict(driver, wait, clear_locator, timeout=None, retries=4) -> bool:
    """
    Clica em 'Limpar Tudo' e espera o clear realmente acontecer (botão sumir).
    Não depende do try_clear_filters().
    """
    for _ in range(retries):
        try:
            # garante visível + scroll
            local_wait = _resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT)
            el = local_wait.until(EC.visibility_of_element_located(clear_locator))
            scroll_to(driver, el)

            # clique robusto (seu click_when_clickable já tem fallback JS)
            click_when_clickable(local_wait, clear_locator)

            # confirmação: o botão some (ou fica invisível) após limpar
            local_wait.until(EC.invisibility_of_element_located(clear_locator))
            return True

        except TimeoutException:
            # ou não clicou, ou clicou mas não confirmou ainda
            time.sleep(0.6)
        except Exception:
            time.sleep(0.6)

    return False


def sort_strict(driver, wait, select_locator, value: str, timeout=None, retries=4) -> bool:
    """
    Ordena usando Select().select_by_value() e confirma que o value foi aplicado.
    Ideal para quando try_sort (clicando option) falha.
    """
    for _ in range(retries):
        try:
            local_wait = _resolve_wait(driver, wait, timeout or DEFAULT_TIMEOUT)
            sel_el = local_wait.until(EC.visibility_of_element_located(select_locator))
            scroll_to(driver, sel_el)

            Select(sel_el).select_by_value(value)

            # confirma que aplicou (value do <select> mudou)
            end = time.time() + (timeout or getattr(local_wait, "_timeout", DEFAULT_TIMEOUT))
            while time.time() < end:
                try:
                    current = sel_el.get_attribute("value")
                    if current == value:
                        return True
                except Exception:
                    pass
                time.sleep(0.2)

        except TimeoutException:
            time.sleep(0.6)
        except Exception:
            time.sleep(0.6)

    return False


# FAVORITAR ITENS (CATEGORIA/BUSCA)
def add_favorite_from_category_first_item(driver, wait, category_locator):
    '''Favoritar primeiro item da lista (PLP)'''
    safe_click_loc(driver, wait, category_locator)
    time.sleep(5)
    safe_click_loc(driver, wait, PLP_WISHLIST_BTN_BY_INDEX(1))
    assert wait_favorite_status(driver), "Não confirmou status de favorito na PLP categoria."


def search_and_add_favorite_by_index(driver, wait, term: str, index: int):
    '''Favoritar item da lista (BUSCA)'''
    safe_click_loc(driver, wait, SEARCH_INPUT)
    el = visible(driver, SEARCH_INPUT, wait=wait)
    el.clear()
    el.send_keys(term)

    visible(driver, SEARCH_SUGGEST_ADD_2, wait=wait)

    safe_click_loc(driver, wait, SEARCH_BUTTON)
    time.sleep(2)

    # scroll até card do índice e favorita
    scroll_into_view(driver, (By.XPATH, f"(//*[@class='product-item-info'])[{index}]"), wait=wait)
    safe_click_loc(driver, wait, PLP_WISHLIST_BTN_BY_INDEX(index))
    assert wait_favorite_status(driver), f"Não confirmou status de favorito na busca (idx={index})."


def open_product_with_avise_by_pagination(
    driver,
    wait,
    category_locator,
    pages=(1, 2, 3, 4, 5)
):
    """
    Entra na categoria e percorre páginas
    até encontrar produto com botão 'Avise-me'.
    """

    # entra na categoria
    safe_click_loc(driver, wait, category_locator)
    time.sleep(2)

    visible(driver, SORTER_SELECT, wait=wait)

    for page in pages:
        try:
            safe_click_loc(driver, wait, PAGINATION_BY_PAGE(page))
            visible(driver, SORTER_SELECT, wait=wait)
        except Exception:
            pass

        # reutiliza sua função existente
        if open_pdp_from_first_avise_in_plp(driver):
            return True

    return False


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

def apply_filter_conservacao_congelado_mobile(driver, wait):
    '''Abre painel dos filtros e aplica o filtro de congelado'''
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_OPEN_PANEL)).click()
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_CONSERVACAO_OPEN)).click()
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_CONSERVACAO_CONGELADO)).click()

    wait.until(lambda d: "conservacao=Congelado" in d.current_url)

    return True


def apply_filter_conservacao_resfriado_mobile(driver, wait):
    '''Abre painel dos filtros e aplica o filtro de resfriado'''
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_OPEN_PANEL)).click()
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_CONSERVACAO_OPEN)).click()
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_CONSERVACAO_RESFRIADO)).click()

    wait.until(lambda d: "conservacao=Resfriado" in d.current_url)

    return True

def try_go_to_page_mobile(driver, wait, page_number: str, retries=3):
    locator = MOBILE_PAGE_NUMBER(page_number)

    for _ in range(retries):
        try:
            el = wait.until(EC.element_to_be_clickable(locator))
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
            el.click()

            wait.until(lambda d: f"p={page_number}" in d.current_url)
            return True
        except:
            time.sleep(1)

    return False

def open_filter_panel_mobile(driver, wait=None, tries=4):
    eff = _effective_timeout(wait, None)
    w = wait if wait is not None else WebDriverWait(driver, eff, poll_frequency=0.2)

    # garante que o toggle existe
    w.until(EC.presence_of_element_located(MOBILE_FILTER_TOGGLE))

    for _ in range(tries):
        # se já estiver aberto, ok
        if driver.find_elements(*MOBILE_FILTER_PANEL_OPENED):
            return True

        # tenta clicar no wrapper
        try:
            mobile_click_strict(driver, MOBILE_FILTER_TOGGLE, timeout=eff, retries=4, sleep_between=0.25, wait=wait)
        except Exception:
            pass

        # espera abrir rapidinho
        try:
            (wait if wait is not None else WebDriverWait(driver, eff, poll_frequency=0.2)).until(
                EC.presence_of_element_located(MOBILE_FILTER_PANEL_OPENED)
            )
            return True
        except Exception:
            pass

        # fallback: clica no strong/tab
        try:
            mobile_click_strict(driver, MOBILE_FILTER_TOGGLE_TAB, timeout=eff, retries=4, sleep_between=0.25, wait=wait)
        except Exception:
            pass

        try:
            (wait if wait is not None else WebDriverWait(driver, eff, poll_frequency=0.2)).until(
                EC.presence_of_element_located(MOBILE_FILTER_PANEL_OPENED)
            )
            return True
        except Exception:
            pass

        # fallback final: click via JS no tab (muito forte em iOS)
        try:
            el = driver.find_element(*MOBILE_FILTER_TOGGLE_TAB)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            driver.execute_script("arguments[0].click();", el)
        except Exception:
            pass

        try:
            (wait if wait is not None else WebDriverWait(driver, eff, poll_frequency=0.2)).until(
                EC.presence_of_element_located(MOBILE_FILTER_PANEL_OPENED)
            )
            return True
        except Exception:
            pass

    return False

def _first_visible(driver, locator):
    els = driver.find_elements(*locator)
    for el in els:
        try:
            if el.is_displayed():
                return el
        except:
            continue
    return None

def scroll_to_avise(driver, locator):
    wai = WebDriverWait(driver, 25)
    wai.until(EC.presence_of_element_located(locator))

    el = _first_visible(driver, locator)
    if not el:
        return None

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    return el

def add_favorite_from_category_first_item_mobile(driver, wait):
    '''Favoritar primeiro item da lista (PLP)'''
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(5)
    safe_click_loc(driver, wait, PLP_WISHLIST_BTN_BY_INDEX(1))
    assert wait_favorite_status(driver), "Não confirmou status de favorito na PLP categoria."

def search_and_add_favorite_by_index_mobile(driver, wait, term: str):
    """Favoritar item da lista (BUSCA) - MOBILE"""

    safe_click_loc(driver, wait, SEARCH_INPUT)
    el = visible(driver, SEARCH_INPUT, wait=wait)
    el.clear()
    el.send_keys(term)

    visible(driver, MOBILE_SEARCH_SUGGEST_ADD_1, wait=wait)

    safe_click_loc(driver, wait, MOBILE_SEARCH_BUTTON)
    time.sleep(5)

    mobile_click_strict(driver, PLP_WISHLIST_BTN_BY_INDEX(1), wait=wait, retries=4, sleep_between=0.25)
    assert wait_favorite_status(driver), "Não confirmou status de favorito na PLP categoria."


def open_product_with_avise_by_pagination_mobile(driver, wait, pages=(1, 2, 3, 4, 5)):
    """
    Entra na categoria e percorre páginas
    até encontrar produto com botão 'Avise-me'.
    """

    # entra na categoria
    mobile_click_strict(driver, MOBILE_MENU_HAMBURGER, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_PARENT_NEXT("bovinos"), wait=wait, retries=4, sleep_between=0.25) # Para alterar a categoria é só alterar a string
    time.sleep(1)
    mobile_click_strict(driver, MOBILE_MENU_SEE_ALL, wait=wait, retries=4, sleep_between=0.25)
    time.sleep(2)

    visible(driver, SORTER_SELECT, wait=wait)

    for page in pages:
        try:
            safe_click_loc(driver, wait, PAGINATION_BY_PAGE(page))
            visible(driver, SORTER_SELECT, wait=wait)
        except Exception:
            pass

        if open_pdp_from_first_avise_in_plp(driver):
            return True

    return False