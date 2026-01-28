import time
from selenium.common.exceptions import (StaleElementReferenceException, ElementClickInterceptedException,TimeoutException)
from helpers.waiters import clickable, visible
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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

#TESTE_1
def scroll_to(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

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
    """Clica com mais robustez (viewport + fallback JS)"""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    try:
        wait.until(lambda d: element.is_displayed() and element.is_enabled())
        element.click()
    except (StaleElementReferenceException, ElementClickInterceptedException):
        driver.execute_script("arguments[0].click();", element)

'''def try_click(wait, locator, timeout=3) -> bool:
    driver = wait._driver
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()
        return True
    except (TimeoutException, StaleElementReferenceException):
        return False'''


