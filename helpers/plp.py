import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException)
from selenium.webdriver.support.ui import Select

from locators.plp import *
from locators.wishlist import *
from locators.header import SEARCH_INPUT, SEARCH_BUTTON,SEARCH_SUGGEST_ADD_2


from helpers.actions import try_click, safe_click_loc, scroll_to, click_when_clickable, scroll_into_view, mobile_click
from helpers.waiters import try_visible, visible
from helpers.wishlist import wait_favorite_status
from helpers.avise_me import open_pdp_from_first_avise_in_plp



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


def try_go_to_page(wait, driver, page_number: str, timeout=10) -> bool:
    """Tenta paginar (sem travar). Retorna True/False."""
    locator = PAGE_NUMBER(page_number)
    try:
        pages = driver.find_elements(*PAGES_UL)
        if pages:
            scroll_to(driver, pages[0])

        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator)).click()
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        return True
    except (TimeoutException, StaleElementReferenceException):
        return False

def apply_filter_strict(driver, wait, open_locator, option_locator, timeout=10, retries=4) -> bool:
    """
    Abre um filtro e clica na opção, garantindo que a opção ficou visível antes do clique.
    Não altera locators. Não depende do try_apply_filter().
    """
    last_exc = None

    for _ in range(retries):
        try:
            # garante que o "open" está na tela
            el_open = wait.until(EC.visibility_of_element_located(open_locator))
            scroll_to(driver, el_open)

            # abre o acordeão
            click_when_clickable(wait, open_locator)

            # garante que a opção apareceu
            wait.until(EC.visibility_of_element_located(option_locator))
            click_when_clickable(wait, option_locator)

            return True
        except Exception as e:
            last_exc = e
            time.sleep(0.6)

    # se quiser, você pode printar last_exc aqui, mas não é obrigatório
    return False


def clear_filters_strict(driver, wait, clear_locator, timeout=12, retries=4) -> bool:
    """
    Clica em 'Limpar Tudo' e espera o clear realmente acontecer (botão sumir).
    Não depende do try_clear_filters().
    """
    for _ in range(retries):
        try:
            # garante visível + scroll
            el = wait.until(EC.visibility_of_element_located(clear_locator))
            scroll_to(driver, el)

            # clique robusto (seu click_when_clickable já tem fallback JS)
            click_when_clickable(wait, clear_locator)

            # confirmação: o botão some (ou fica invisível) após limpar
            wait.until(EC.invisibility_of_element_located(clear_locator))
            return True

        except TimeoutException:
            # ou não clicou, ou clicou mas não confirmou ainda
            time.sleep(0.6)
        except Exception:
            time.sleep(0.6)

    return False


def sort_strict(driver, wait, select_locator, value: str, timeout=12, retries=4) -> bool:
    """
    Ordena usando Select().select_by_value() e confirma que o value foi aplicado.
    Ideal para quando try_sort (clicando option) falha.
    """
    for _ in range(retries):
        try:
            sel_el = wait.until(EC.visibility_of_element_located(select_locator))
            scroll_to(driver, sel_el)

            Select(sel_el).select_by_value(value)

            # confirma que aplicou (value do <select> mudou)
            end = time.time() + timeout
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
    safe_click_loc(driver, wait, category_locator, timeout=15)
    time.sleep(5)
    safe_click_loc(driver, wait, PLP_WISHLIST_BTN_BY_INDEX(1), timeout=12)
    assert wait_favorite_status(driver), "Não confirmou status de favorito na PLP categoria."


def search_and_add_favorite_by_index(driver, wait, term: str, index: int):
    '''Favoritar item da lista (BUSCA)'''
    safe_click_loc(driver, wait, SEARCH_INPUT, timeout=12)
    el = visible(driver, SEARCH_INPUT, timeout=12)
    el.clear()
    el.send_keys(term)

    visible(driver, SEARCH_SUGGEST_ADD_2, timeout=20)

    safe_click_loc(driver, wait, SEARCH_BUTTON, timeout=12)
    time.sleep(2)

    # scroll até card do índice e favorita
    scroll_into_view(driver, (By.XPATH, f"(//*[@class='product-item-info'])[{index}]"), timeout=20)
    safe_click_loc(driver, wait, PLP_WISHLIST_BTN_BY_INDEX(index), timeout=12)
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
    safe_click_loc(driver, wait, category_locator, timeout=15)
    time.sleep(2)

    visible(driver, SORTER_SELECT, timeout=25)

    for page in pages:
        try:
            safe_click_loc(driver, wait, PAGINATION_BY_PAGE(page), timeout=6)
            visible(driver, SORTER_SELECT, timeout=20)
        except Exception:
            pass

        # reutiliza sua função existente
        if open_pdp_from_first_avise_in_plp(driver):
            return True

    return False


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

def _html_has_open_menu_class(driver) -> bool:
    cls = driver.find_element(By.TAG_NAME, "html").get_attribute("class") or ""
    cls_low = cls.lower()
    return ("wrapper_opened" in cls_low) or ("mm-wrapper_opened" in cls_low) or ("mm-wrapper-opened" in cls_low)


def mobile_open_hamburger_menu(driver, wait, timeout=20):
    w = WebDriverWait(driver, timeout, poll_frequency=0.3,
                      ignored_exceptions=(StaleElementReferenceException,))

    # se já estiver aberto, não faz nada
    if _html_has_open_menu_class(driver):
        return True

    # garante topo (no iOS ajuda MUITO)
    driver.execute_script("window.scrollTo(0,0);")

    # clica no hambúrguer (robusto)
    mobile_click(driver, wait, MOBILE_MENU_HAMBURGER, timeout=timeout, retries=4)

    # espera pelo "sinal" correto: classe do <html> mudou
    try:
        w.until(lambda d: _html_has_open_menu_class(d))
        return True
    except TimeoutException:
        return False


def mobile_open_category_parent_and_see_all(driver, wait, slug: str, timeout=25):
    assert mobile_open_hamburger_menu(driver, wait, timeout=timeout), "Não abriu o menu hambúrguer."

    mobile_click(driver, wait, MOBILE_MENU_PARENT_NEXT(slug), timeout=timeout, retries=4)
    mobile_click(driver, wait, MOBILE_MENU_SEE_ALL, timeout=timeout, retries=4)
    return True


def apply_filter_conservacao_congelado_mobile(driver, wait):
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_OPEN_PANEL)).click()
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_CONSERVACAO_OPEN)).click()
    wait.until(EC.element_to_be_clickable(MOBILE_FILTER_CONSERVACAO_CONGELADO)).click()

    wait.until(lambda d: "conservacao=Congelado" in d.current_url)

    return True


def try_go_to_page_mobile(driver, wait, page_number: str, timeout=15, retries=3):
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