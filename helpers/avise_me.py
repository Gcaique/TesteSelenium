import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.waiters import visible, wait, wait_any_visible, wait_visible_any, _effective_timeout
from helpers.actions import safe_click_loc, mobile_click_strict

from locators.plp import (
    SORTER_SELECT,
    AVISE_DISABLED_ANY,
    AVISE_ENABLED_ANY, MOBILE_PAGE_NUMBER
)


def open_pdp_from_first_avise_in_plp(driver, wait=None, timeout=None):
    t = _effective_timeout(wait, timeout)
    w = wait if wait is not None else None
    visible(driver, SORTER_SELECT, timeout=t, wait=w)

    avise = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=t)
    if not avise:
        avise = wait_any_visible(driver, AVISE_ENABLED_ANY, timeout=t)

    if not avise:
        return False

    card = driver.execute_script(
        "return arguments[0].closest('[id^=\"product-item-info_\"]');",
        avise,
    )

    if not card:
        return False

    link = driver.execute_script(
        "return arguments[0].querySelector('a.product-item-link, a.product-item-photo');",
        card,
    )

    if not link:
        link = driver.execute_script(
            "return arguments[0].querySelector('span.product-image-wrapper');",
            card,
        )
        if not link:
            return False

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        link,
    )

    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", link)

    return True


def _has_classes(el, *tokens):
    cls = (el.get_attribute("class") or "")
    return all(t in cls for t in tokens)

def _wait_class_contains(driver, locator, timeout, *tokens):
    w = WebDriverWait(driver, timeout)
    def _pred(d):
        try:
            el = d.find_element(*locator)
            return el if _has_classes(el, *tokens) else False
        except StaleElementReferenceException:
            return False
    return w.until(_pred)

def _wait_class_not_contains(driver, locator, timeout, *tokens):
    w = WebDriverWait(driver, timeout)
    def _pred(d):
        try:
            el = d.find_element(*locator)
            cls = (el.get_attribute("class") or "")
            return el if all(t not in cls for t in tokens) else False
        except StaleElementReferenceException:
            return False
    return w.until(_pred)

def toggle_avise_me_requires_refresh(driver, page_ready_locator=None, timeout=None, wait_click_class=False, wait_obj=None):
    # garante página pronta
    t = _effective_timeout(wait_obj, timeout)
    w = wait_obj if wait_obj is not None else wait(driver, t)
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=t, wait=wait_obj)
    else:
        wait_visible_any(driver, [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY], timeout=t)

    # encontra o botão DESATIVADO
    w.until(EC.presence_of_element_located(AVISE_DISABLED_ANY))

    # clica no botão do avise-me
    safe_click_loc(driver, w, AVISE_DISABLED_ANY, timeout=t)

    # 3) espera AJAX: virar "alert-active clicked" no botão disabled
    _wait_class_contains(driver, AVISE_DISABLED_ANY, t, "alert-active", "clicked")

    # 4) refresh
    driver.refresh()

    # 5) aguarda página pronta de novo
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=t, wait=wait_obj)
    else:
        w.until(EC.presence_of_element_located(AVISE_ENABLED_ANY))

    # 6) valida que o ENABLED está ativo após refresh
    _wait_class_contains(driver, AVISE_ENABLED_ANY, t, "alert-active", "clicked")

    # 7) clica para desativar
    safe_click_loc(driver, w, AVISE_ENABLED_ANY, timeout=t)

    # 8) espera AJAX: remover "alert-active clicked"
    _wait_class_not_contains(driver, AVISE_ENABLED_ANY, t, "alert-active", "clicked")

    return True


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def find_avise_me_plp_mobile(driver, page_ready_locator, max_pages=5, timeout=None, wait_obj=None):
    """Diferente de desktop, esse helper só garante achar o botão do avise-me na plp"""
    t = _effective_timeout(wait_obj, timeout)
    w = wait_obj if wait_obj is not None else None

    for page in range(1, max_pages + 1):

        # garante que a página carregou
        visible(driver, page_ready_locator, timeout=t, wait=w)

        # procura botões avise-me na página
        buttons = driver.find_elements(*AVISE_DISABLED_ANY)

        for btn in buttons:
            if btn.is_displayed():
                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btn
                )
                return True

        # tenta ir para próxima página
        try:
            next_page = MOBILE_PAGE_NUMBER(str(page + 1))
            mobile_click_strict(
                driver,
                next_page,
                timeout=_effective_timeout(wait, 10, default=10),
                retries=3,
                sleep_between=0.25
            )
        except Exception:
            break  # não tem próxima página ou falhou navegação

    return False
