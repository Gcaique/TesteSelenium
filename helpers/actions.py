import time
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.keys import Keys

from helpers.waiters import clickable, visible, DEFAULT_TIMEOUT

def _resolve_wait(driver, wait, timeout=None, poll=0.1):
    """
    Retorna um WebDriverWait, priorizando o fornecido (fixture). Usa timeout explícito
    ou, como fallback, DEFAULT_TIMEOUT.
    """
    if wait is not None:
        return wait
    effective = timeout if timeout is not None else DEFAULT_TIMEOUT
    return WebDriverWait(driver, effective, poll_frequency=poll)


def click(driver, locator, timeout=None, wait=None):
    """Clique robusto com fallback JS"""
    w = _resolve_wait(driver, wait, timeout)
    el = clickable(driver, locator, timeout=timeout, wait=w)
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


def fill(driver, locator, value: str, timeout=None, wait=None):
    """Preenche input com fallback JS para clear"""
    w = _resolve_wait(driver, wait, timeout)
    el = visible(driver, locator, timeout=timeout, wait=w)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)

    el.send_keys(value)


def scroll_into_view(driver, locator, timeout=None, wait=None):
    """Scroll até elemento e retorna ele"""
    w = _resolve_wait(driver, wait, timeout)
    el = visible(driver, locator, timeout=timeout, wait=w)
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


def try_click(driver, locator, timeout=None, wait=None) -> bool:
    """Tenta clicar sem quebrar o teste"""
    try:
        click(driver, locator, timeout=timeout, wait=wait)
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


def safe_click_loc(driver, wait, locator, timeout=None):
    """
    Pega o WebElement (clicável) e clica usando seu safe_click.
    """
    w = _resolve_wait(driver, wait, timeout)
    el = w.until(EC.element_to_be_clickable(locator))
    safe_click(driver, w, el)
    return el


def safe_click_loc_retry(driver, locator, timeout=None, retries=4, sleep_between=0.25, wait=None):
    """
    Clica em um locator com retry REAL contra Stale/Intercept.
    Diferença do safe_click_loc: ele re-encontra o elemento a cada tentativa.
    """
    last_exc = None
    for _ in range(retries):
        try:
            w = _resolve_wait(driver, wait, timeout)
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
    el = scroll_into_view(driver, locator, timeout=timeout, wait=wait)

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


def scroll_to(driver, locator_or_xpath, timeout=None, wait=None):
    target = _normalize_locator(locator_or_xpath)

    # se for WebElement, scroll direto
    if hasattr(target, "rect"):  # WebElement
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
        return target

    # caso locator/xpath:
    w = _resolve_wait(driver, wait, timeout)
    el = visible(driver, target, timeout=timeout, wait=w)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    return el


def fill_input(driver, wait, locator, value: str, timeout=None):
    w = _resolve_wait(driver, wait, timeout)
    el = visible(driver, locator, timeout=timeout, wait=w)
    try:
        el.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", el)
    el.send_keys(value)

def clear_and_type(driver, locator, texto):
    """Limpa o campo e digita o texto."""
    campo = driver.find_element(*locator)
    campo.clear()
    time.sleep(1)
    campo.send_keys(texto)
    time.sleep(1)

def scroll_to_middle(driver, wait, locator, timeout=None):
    """Faz scroll ate o elemento ficar centralizado na viewport."""
    w = _resolve_wait(driver, wait, timeout)
    el = w.until(EC.presence_of_element_located(locator))
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
        el,
    )
    return el


def scroll_to_top(driver, wait, locator, timeout=None):
    """Faz scroll ate o elemento ficar no topo da viewport."""
    w = _resolve_wait(driver, wait, timeout)
    el = w.until(EC.presence_of_element_located(locator))
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});",
        el,
    )
    return el


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def _first_displayed(driver, locator):
    els = driver.find_elements(*locator)
    for e in els:
        try:
            if e.is_displayed():
                return e
        except StaleElementReferenceException:
            continue
    return None


def tap_element(driver, element):
    finger = PointerInput(interaction.POINTER_TOUCH, "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to(element)   # <- em vez de move_to_location(x,y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(0.06)
    actions.pointer_action.pointer_up()
    actions.perform()


def mobile_click_strict(driver, locator, timeout=None, retries=4, sleep_between=0.25, wait=None):
    last = None
    w = _resolve_wait(driver, wait, timeout, poll=0.2)

    for _ in range(retries):
        try:
            el = w.until(lambda d: _first_displayed(d, locator))

            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                time.sleep(0.2)
            except Exception:
                pass

            el = w.until(lambda d: _first_displayed(d, locator))

            # 1) CLICK normal primeiro (como era antes)
            try:
                el.click()
                return True
            except Exception as e:
                last = e

            # 2) CLICK via JS
            try:
                driver.execute_script("arguments[0].click();", el)
                return True
            except Exception as e:
                last = e

            # 3) TAP real por elemento (mais forte no iOS)
            try:
                tap_element(driver, el)
                return True
            except Exception as e:
                last = e

        except Exception as e:
            last = e

        time.sleep(sleep_between)

    raise last

def scroll_into_view_loc_mobile(driver, locator, timeout=None):
    effective = timeout if timeout is not None else 20
    end = time.time() + effective
    last_err = None

    while time.time() < end:
        try:
            el = driver.find_element(*locator)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            return el
        except StaleElementReferenceException as e:
            last_err = e
            time.sleep(0.3)

    raise TimeoutError(f"Não consegui dar scroll no elemento: {locator}. Erro: {last_err}")