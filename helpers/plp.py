from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, StaleElementReferenceException)

from locators.plp import FILTER_CLEAR_ALL, SORTER_SELECT, SORT_OPTION
from locators.plp import PAGE_NUMBER, PAGES_UL

from helpers.actions import try_click
from helpers.waiters import try_visible
from helpers.actions import scroll_to



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

