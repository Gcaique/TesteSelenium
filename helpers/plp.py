import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException)
from selenium.webdriver.support.ui import Select

from locators.plp import FILTER_CLEAR_ALL, SORTER_SELECT, SORT_OPTION
from locators.plp import PAGE_NUMBER, PAGES_UL

from helpers.actions import try_click
from helpers.waiters import try_visible
from helpers.actions import scroll_to, click_when_clickable



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


#TESTE_1
def try_go_to_page(wait, driver, page_number: str, timeout=3) -> bool:
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
