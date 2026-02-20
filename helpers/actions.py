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
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotVisibleException,
)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput


def _first_displayed(driver, locator):
    els = driver.find_elements(*locator)
    for e in els:
        try:
            if e.is_displayed():
                return e
        except StaleElementReferenceException:
            continue
    return None


def _tap_center(driver, el):
    rect = el.rect
    x = rect["x"] + rect["width"] / 2
    y = rect["y"] + rect["height"] / 2

    finger = PointerInput(PointerInput.TOUCH, "finger")
    actions = ActionChains(driver)
    actions.w3c_actions.devices = [finger]

    finger.create_pointer_move(duration=0, x=int(x), y=int(y), origin="viewport")
    finger.create_pointer_down()
    finger.create_pointer_up()
    actions.perform()


def mobile_click_strict(driver, locator, timeout=12, retries=4, sleep_between=0.25):
    last = None
    wait = WebDriverWait(driver, timeout, poll_frequency=0.2)

    for _ in range(retries):
        try:
            # 1) pega o primeiro elemento VISÍVEL (não apenas presente)
            el = wait.until(lambda d: _first_displayed(d, locator))

            # 2) scroll pro elemento
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.15)
            except Exception:
                pass

            # 3) re-pega o visível (evita stale/DOM reflow)
            el = wait.until(lambda d: _first_displayed(d, locator))

            # 4) click normal
            try:
                el.click()
                return True
            except (ElementClickInterceptedException, StaleElementReferenceException, ElementNotVisibleException) as e:
                last = e

            # 5) click via JS (às vezes ajuda em webviews)
            try:
                driver.execute_script("arguments[0].click();", el)
                return True
            except Exception as e:
                last = e

            # 6) tap real por coordenadas (mais forte no iOS)
            try:
                _tap_center(driver, el)
                return True
            except Exception as e:
                last = e

        except Exception as e:
            last = e

        time.sleep(sleep_between)

    raise last if last else TimeoutException(f"Falha ao clicar em {locator}")