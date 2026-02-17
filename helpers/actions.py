import time
from selenium.common.exceptions import (StaleElementReferenceException, ElementClickInterceptedException,TimeoutException, WebDriverException)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

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
    """
    w = WebDriverWait(driver, timeout)
    el = w.until(EC.element_to_be_clickable(locator))
    safe_click(driver, w, el)
    return el


def safe_click_loc_retry(driver, locator, timeout=10, retries=4, sleep_between=0.25):
    """
    Clica em um locator com retry REAL contra Stale/Intercept.
    Diferença do safe_click_loc: ele re-encontra o elemento a cada tentativa.
    """
    last_exc = None
    for _ in range(retries):
        try:
            w = WebDriverWait(driver, timeout)
            el = w.until(EC.element_to_be_clickable(locator))
            safe_click(driver, w, el)  # usa seu safe_click atual
            return el
        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            last_exc = e
            time.sleep(sleep_between)

    # última tentativa: deixa estourar como timeout "limpo"
    if last_exc:
        raise last_exc
    raise TimeoutException(f"Falha ao clicar (retry): {locator}")


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


def _normalize_locator(locator_or_xpath):
    # aceita WebElement, ("//div...") ou (By.XPATH, "//div...")
    if isinstance(locator_or_xpath, WebElement):
        return locator_or_xpath

    if isinstance(locator_or_xpath, tuple):
        return locator_or_xpath

    if isinstance(locator_or_xpath, str):
        return (By.XPATH, locator_or_xpath)

    raise TypeError(f"Locator inválido: {type(locator_or_xpath)} -> {locator_or_xpath}")


def scroll_to(driver, locator_or_xpath, timeout=8):
    target = _normalize_locator(locator_or_xpath)

    # se for WebElement, scroll direto
    if hasattr(target, "rect"):  # WebElement
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
        return target

    # caso locator/xpath:
    el = visible(driver, target, timeout=timeout)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    return el


def fill_input(driver, wait, locator, value: str, timeout=10):
    el = visible(driver, locator, timeout=timeout)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)
    el.send_keys(value)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def mobile_click(driver, wait, locator, timeout=20, retries=3, use_js_fallback=True):
    last = None
    w = WebDriverWait(driver, timeout, poll_frequency=0.2,
                      ignored_exceptions=(StaleElementReferenceException,))

    for _ in range(retries):
        try:
            # 1) aguarda visível (melhor que presence)
            el = w.until(EC.visibility_of_element_located(locator))

            # 2) traz pro viewport
            driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", el)
            time.sleep(0.15)

            # 3) aguarda realmente clicável
            el = w.until(EC.element_to_be_clickable(locator))

            # 4) re-find pra evitar stale e clicar
            el = driver.find_element(*locator)
            try:
                el.click()
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                if not use_js_fallback:
                    raise
                # 5) fallback JS click
                el = driver.find_element(*locator)
                driver.execute_script("arguments[0].click();", el)

            return True

        except (StaleElementReferenceException, ElementClickInterceptedException, TimeoutException) as e:
            last = e
            if use_js_fallback:
                try:
                    # fallback mais agressivo: re-find + JS click
                    el = driver.find_element(*locator)
                    driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", el)
                    time.sleep(0.1)
                    driver.execute_script("arguments[0].click();", el)
                    return True
                except Exception as e2:
                    last = e2

            time.sleep(0.4)

        except Exception as e:
            last = e
            time.sleep(0.4)

    raise last