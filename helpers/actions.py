import time
from selenium.common.exceptions import (StaleElementReferenceException, ElementClickInterceptedException,TimeoutException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from helpers.waiters import clickable, visible


def click(driver, locator, timeout=10):
    """Clique robusto com fallback JS"""
    el = clickable(driver, locator, timeout)
    try:
        el.click()
    except (ElementClickInterceptedException, StaleElementReferenceException):
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", el
            )
        except Exception:
            pass
        driver.execute_script("arguments[0].click();", el)


def fill(driver, locator, value: str):
    """Preenche input com fallback JS para clear"""
    el = visible(driver, locator, timeout=10)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)

    el.send_keys(value)


def scroll_into_view(driver, locator, timeout=10):
    """Scroll até elemento e retorna ele"""
    el = visible(driver, locator, timeout=timeout)
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center', inline:'center'});",
        el,
    )
    return el


def scroll_and_click(driver, element):
    """Scroll + click direto em WebElement"""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element,)
    time.sleep(0.3)
    element.click()


def try_click(driver, locator, timeout=2.0) -> bool:
    """Tenta clicar sem quebrar o teste"""
    try:
        click(driver, locator, timeout=timeout)
        return True
    except Exception:
        return False


def click_when_clickable(wait, locator):
    driver = wait._driver
    el = wait.until(EC.element_to_be_clickable(locator))
    try:
        el.click()
    except (ElementClickInterceptedException, StaleElementReferenceException):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        driver.execute_script("arguments[0].click();", el)

def safe_click(driver, wait, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    try:
        # mais forte do que displayed/enabled
        wait.until(lambda d: element.is_displayed() and element.is_enabled())
        try:
            element.click()
        except Exception:
            driver.execute_script("arguments[0].click();", element)
    except (StaleElementReferenceException, ElementClickInterceptedException):
        driver.execute_script("arguments[0].click();", element)


def safe_click_loc(driver, wait, locator, timeout=10):
    """
    Pega o WebElement (clicável) e clica usando seu safe_click.
    (já tinha sido sugerido; mantemos)
    """
    w = WebDriverWait(driver, timeout)
    el = w.until(EC.element_to_be_clickable(locator))
    safe_click(driver, w, el)
    return el


def scroll_and_safe_click_loc(driver, wait, locator, timeout=10):
    """
    1) Faz scroll até o elemento ficar visível
    2) Clica usando seu safe_click (que recebe WebElement)
    3) Fallback: scroll_and_click direto
    """
    # 1) scroll + pega elemento visível
    el = scroll_into_view(driver, locator, timeout=timeout)

    # 2) tenta clicar “do seu jeito”
    try:
        safe_click(driver, wait, el)
        return el
    except Exception:
        # 3) fallback: scroll + click direto
        try:
            scroll_and_click(driver, el)
            return el
        except Exception:
            # último fallback: JS click
            driver.execute_script("arguments[0].click();", el)
            return el


def scroll_to(driver, xpath):
    """Faz scroll até uma seção específica da home."""
    locator = (By.XPATH, xpath)
    el = visible(driver, locator, timeout=8)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)


def fill_input(driver, wait, locator, value: str, timeout=10):
    el = visible(driver, locator, timeout=timeout)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)
    el.send_keys(value)

