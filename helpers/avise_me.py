import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

from helpers.waiters import visible, wait, wait_any_visible, wait_visible_any
from helpers.actions import safe_click_loc, mobile_click_strict

from locators.plp import (
    SORTER_SELECT,
    AVISE_DISABLED_ANY,
    AVISE_ENABLED_ANY,
)


def open_pdp_from_first_avise_in_plp(driver):
    visible(driver, SORTER_SELECT, timeout=25)

    avise = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=5)
    if not avise:
        avise = wait_any_visible(driver, AVISE_ENABLED_ANY, timeout=2)

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
    w = wait(driver, timeout)
    def _pred(d):
        try:
            el = d.find_element(*locator)
            return el if _has_classes(el, *tokens) else False
        except StaleElementReferenceException:
            return False
    return w.until(_pred)

def _wait_class_not_contains(driver, locator, timeout, *tokens):
    w = wait(driver, timeout)
    def _pred(d):
        try:
            el = d.find_element(*locator)
            cls = (el.get_attribute("class") or "")
            return el if all(t not in cls for t in tokens) else False
        except StaleElementReferenceException:
            return False
    return w.until(_pred)

def toggle_avise_me_requires_refresh(driver, page_ready_locator=None, timeout=25, wait_click_class=False,):
    # garante página pronta
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(driver, [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY], timeout=timeout)

    # encontra o botão DESATIVADO
    w = wait(driver, timeout)
    w.until(EC.presence_of_element_located(AVISE_DISABLED_ANY))

    # clica no botão do avise-me
    safe_click_loc(driver, w, AVISE_DISABLED_ANY, timeout=timeout)

    # 3) espera AJAX: virar "alert-active clicked" no botão disabled
    _wait_class_contains(driver, AVISE_DISABLED_ANY, timeout, "alert-active", "clicked")

    # 4) refresh
    driver.refresh()

    # 5) aguarda página pronta de novo
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        w.until(EC.presence_of_element_located(AVISE_ENABLED_ANY))

    # 6) valida que o ENABLED está ativo após refresh
    _wait_class_contains(driver, AVISE_ENABLED_ANY, timeout, "alert-active", "clicked")

    # 7) clica para desativar
    safe_click_loc(driver, w, AVISE_ENABLED_ANY, timeout=timeout)

    # 8) espera AJAX: remover "alert-active clicked"
    _wait_class_not_contains(driver, AVISE_ENABLED_ANY, timeout, "alert-active", "clicked")

    return True


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def toggle_avise_me_requires_refresh_mobile(driver, page_ready_locator=None, timeout=25, wait_click_class=False,):
    # garante página pronta
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(driver, [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY], timeout=timeout)

    # encontra o botão DESATIVADO
    w = wait(driver, timeout)
    w.until(EC.presence_of_element_located(AVISE_DISABLED_ANY))

    # clica no botão do avise-me
    mobile_click_strict(driver, AVISE_DISABLED_ANY, timeout=timeout, retries=4, sleep_between=0.25)

    # 3) espera AJAX: virar "alert-active clicked" no botão disabled
    _wait_class_contains(driver, AVISE_DISABLED_ANY, timeout, "alert-active", "clicked")

    # 4) refresh
    driver.refresh()

    # 5) aguarda página pronta de novo
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        w.until(EC.presence_of_element_located(AVISE_ENABLED_ANY))

    # 6) valida que o ENABLED está ativo após refresh
    _wait_class_contains(driver, AVISE_ENABLED_ANY, timeout, "alert-active", "clicked")

    # 7) clica para desativar
    mobile_click_strict(driver, AVISE_ENABLED_ANY, timeout=timeout, retries=4, sleep_between=0.25)

    # 8) espera AJAX: remover "alert-active clicked"
    _wait_class_not_contains(driver, AVISE_ENABLED_ANY, timeout, "alert-active", "clicked")

    return True