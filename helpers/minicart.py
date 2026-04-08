import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from helpers.waiters import wait, visible, _effective_timeout, DEFAULT_TIMEOUT
from helpers.actions import click, safe_click_loc_retry, mobile_click_strict

from locators.common import (MINICART_WRAPPER)
from locators.cart import *
from locators.wishlist import *
from helpers.actions import click_when_clickable

def minicart_visible(driver) -> bool:
    """Fonte da verdade para usuário logado"""
    try:
        el = wait(driver, 1.5).until(
            EC.visibility_of_element_located(MINICART_WRAPPER)
        )
        return el.is_displayed()
    except Exception:
        return False


def wait_minicart_loading(driver):
    """Espera loading do minicart (três variações de classe)"""
    try:
        wait(driver, 10).until(EC.visibility_of_element_located(MINICART_LOADING_1))
    except Exception:
        pass

    try:
        wait(driver, 10).until(EC.invisibility_of_element_located(MINICART_LOADING_1))
    except Exception:
        pass

    try:
        wait(driver, 10).until(EC.visibility_of_element_located(MINICART_LOADING_2))
    except Exception:
        pass

    try:
        wait(driver, 10).until(EC.invisibility_of_element_located(MINICART_LOADING_2))
    except Exception:
        pass

    try:
        wait(driver, 10).until(EC.visibility_of_element_located(MINICART_LOADING_3))
    except Exception:
        pass

    try:
        wait(driver, 10).until(EC.invisibility_of_element_located(MINICART_LOADING_3))
    except Exception:
        pass

def wait_minicart_ready(driver, timeout=None, wait=None):
    """
    Garante:
    - loading sumiu
    - minicart está aberto
    - botão 'Ver carrinho' está visível
    """
    t = _effective_timeout(wait, timeout)
    t_open = _effective_timeout(wait, None)
    wait_minicart_loading(driver)

    if not driver.find_elements(*MINICART_ACTIVE):
        click(driver, MINICART_ICON, timeout=t_open, wait=wait)
        visible(driver, MINICART_ACTIVE, timeout=t_open, wait=wait)

    visible(driver, VIEWCART, timeout=t, wait=wait)

def minicart_click_wishlist(driver, index=1, timeout=None):
    """Clica no ícone de wishlist (coração) do item N dentro do minicart."""
    eff = _effective_timeout(None, timeout, default=DEFAULT_TIMEOUT)
    w = WebDriverWait(driver, eff)
    end = time.time() + eff
    last_err = None

    # garante que o minicart já está renderizado
    w.until(lambda d: d.find_elements(*MINICART_LIST))

    while time.time() < end:
        try:
            items = driver.find_elements(*MINICART_ITEMS)
            if len(items) < index:
                time.sleep(0.3)
                continue

            item = items[index - 1]

            # garante item “em foco” (mesmo sendo fixo, KO troca o DOM)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", item)
            time.sleep(0.15)

            btns = item.find_elements(*MINICART_WISHLIST_BTN_IN_ITEM)
            if not btns:
                time.sleep(0.3)
                continue

            btn = btns[0]

            # Espera ficar clicável do ponto de vista prático.
            w.until(lambda d: btn.is_displayed() and btn.is_enabled())

            # clique normal com fallback JS
            try:
                btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", btn)

            # pequena folga pro ajax/knockout processar
            time.sleep(0.6)
            return True

        except (StaleElementReferenceException, TimeoutException) as e:
            last_err = e
            time.sleep(0.3)

    raise TimeoutException(f"Não consegui clicar no coração do minicart (item {index}). Último erro: {last_err}")


def wishlist_toggle_remove_onwishlist(driver, wait, index=1):
    """Remoção item nos favoritos pelo minicart (coração do item index)."""
    minicart_click_wishlist(driver, index=index, timeout=None)
    time.sleep(1.2) # só uma folguinha pro ajax/KO


def wishlist_toggle_add_towishlist(driver, wait, index=1):
    """Adicionar item nos favoritos pelo minicart (coração do item index)."""
    minicart_click_wishlist(driver, index=index, timeout=None)
    time.sleep(1.2)  # só uma folguinha pro ajax/KO



def remove_simple_delete(driver, wait, idx: int = 1):
    """Remove produto do minicart e confirma modal."""
    t = _effective_timeout(wait, 15, default=15)
    safe_click_loc_retry(driver, REMOVE_SIMPLE_DELETE_BY_INDEX(idx), timeout=t, retries=6)
    visible(driver, CONFIRM_MODAL_ACCEPT, timeout=t, wait=wait)
    safe_click_loc_retry(driver, CONFIRM_MODAL_ACCEPT, timeout=t, retries=6)


def wait_remove_alert_cycle(driver, timeout=None):
    """
    Regras:
      - se o alerta aparecer, NÃO faça mais nada até ele sumir
      - quando ele sumir, a remoção terminou
    """
    # Se já está vazio, não precisa esperar alerta
    if driver.find_elements(*MINICART_EMPTY_VIEW_PRODUCTS):
        return

    # 1) espera alerta aparecer
    try:
        WebDriverWait(driver, 4, poll_frequency=0.1).until(
            EC.visibility_of_element_located(MINICART_REMOVE_ALERT)
        )
    except TimeoutException:
        # pode acontecer do alerta não aparecer em alguns casos
        return

    # 2) espera o alerta SUMIR (remoção terminou)
    eff = _effective_timeout(None, timeout, default=DEFAULT_TIMEOUT)
    WebDriverWait(driver, eff, poll_frequency=0.1).until(
        EC.invisibility_of_element_located(MINICART_REMOVE_ALERT)
    )


def minicart_empty(driver, wait, max_removals: int = 30):
    """
    Remove item por item:
      - remove sempre o index 1
      - depois aguarda o ciclo completo do alerta (aparecer -> sumir)
      - só então remove o próximo
    """
    # já vazio
    if driver.find_elements(*MINICART_EMPTY_VIEW_PRODUCTS):
        return True

    for _ in range(max_removals):
        # se ficou vazio entre ciclos
        if driver.find_elements(*MINICART_EMPTY_VIEW_PRODUCTS):
            return True

        # se o alerta está VISIVEL, espera ficar INVISIVEL antes de tentar qualquer clique
        try:
            if driver.find_elements(*MINICART_REMOVE_ALERT):
                WebDriverWait(driver, 25, poll_frequency=0.1).until(
                    EC.invisibility_of_element_located(MINICART_REMOVE_ALERT)
                )
        except Exception:
            pass

        # tenta remover o primeiro item (se não existe mais botão, acabou)
        if not driver.find_elements(*REMOVE_SIMPLE_DELETE_BY_INDEX(1)):
            # sem botão remover => considera vazio / ok
            return True

        remove_simple_delete(driver, wait, idx=1)
        wait_remove_alert_cycle(driver, timeout=None)

    # se estourou limite
    raise AssertionError("Minicart não ficou vazio após tentativas de remoção.")

def minicart_increment_qty(driver, wait):
    "Incrementa quantidade do produto no minicart"
    click_when_clickable(wait, MINICART_INCREMENT_BTN)
    wait_minicart_loading(driver)

def minicart_decrement_qty(driver, wait):
    "Decrementa quantidade do produto no minicart"
    click_when_clickable(wait, MINICART_DECREMENT_BTN)
    wait_minicart_loading(driver)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def remove_simple_delete_mobile(driver, wait, idx: int = 1):
    """Remove produto do minicart e confirma modal."""
    t = _effective_timeout(wait, 15, default=15)
    mobile_click_strict(driver, MOBILE_REMOVE_SIMPLE_DELETE_BY_INDEX(idx), timeout=t, retries=6, sleep_between=0.25)
    visible(driver, CONFIRM_MODAL_ACCEPT, timeout=t, wait=wait)
    mobile_click_strict(driver, CONFIRM_MODAL_ACCEPT, timeout=t, retries=6, sleep_between=0.25)


def wait_remove_alert_cycle_mobile(driver, timeout=None):
    """
    Regras:
      - se o alerta aparecer, NÃO faça mais nada até ele sumir
      - quando ele sumir, a remoção terminou
    """
    # Se já está vazio, não precisa esperar alerta
    if driver.find_elements(*MINICART_EMPTY_VIEW_PRODUCTS):
        return

    # 1) espera alerta aparecer
    try:
        WebDriverWait(driver, 4, poll_frequency=0.1).until(
            EC.visibility_of_element_located(MINICART_REMOVE_ALERT)
        )
    except TimeoutException:
        # pode acontecer do alerta não aparecer em alguns casos
        return

    # 2) espera o alerta SUMIR (remoção terminou)
    eff = _effective_timeout(None, timeout, default=DEFAULT_TIMEOUT)
    WebDriverWait(driver, eff, poll_frequency=0.1).until(
        EC.invisibility_of_element_located(MINICART_REMOVE_ALERT)
    )


def minicart_empty_mobile(driver, wait, max_removals: int = 30):
    """
    Remove item por item:
      - remove sempre o index 1
      - depois aguarda o ciclo completo do alerta (aparecer -> sumir)
      - só então remove o próximo
    """
    # já vazio
    if driver.find_elements(*MINICART_EMPTY_VIEW_PRODUCTS):
        return True

    for _ in range(max_removals):
        # se ficou vazio entre ciclos
        if driver.find_elements(*MINICART_EMPTY_VIEW_PRODUCTS):
            return True

        # se o alerta está VISIVEL, espera ficar INVISIVEL antes de tentar qualquer clique
        try:
            if driver.find_elements(*MINICART_REMOVE_ALERT):
                WebDriverWait(driver, 25, poll_frequency=0.1).until(
                    EC.invisibility_of_element_located(MINICART_REMOVE_ALERT)
                )
        except Exception:
            pass

        # tenta remover o primeiro item (se não existe mais botão, acabou)
        if not driver.find_elements(*MOBILE_REMOVE_SIMPLE_DELETE_BY_INDEX(1)):
            # sem botão remover => considera vazio / ok
            return True

        remove_simple_delete_mobile(driver, wait, idx=1)
        wait_remove_alert_cycle_mobile(driver, timeout=None)

    # se estourou limite
    raise AssertionError("Minicart não ficou vazio após tentativas de remoção.")
