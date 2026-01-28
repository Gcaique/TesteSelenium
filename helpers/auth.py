import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


from helpers.waiters import visible
from helpers.actions import click, fill
from helpers.popups import try_close_popups
from helpers.minicart import minicart_visible

from locators.header import (
    LOGIN_MENU,
    USERNAME_INPUT,
    PASSWORD_INPUT,
    BTN_AVANCAR,

)


def ensure_logged_in(driver, user: str, passwd: str):
    """Garante login (idempotente)"""

    if minicart_visible(driver):
        try_close_popups(driver)
        return

    # abre login
    click(driver, LOGIN_MENU, timeout=10)
    visible(driver, USERNAME_INPUT, timeout=10)

    # username
    fill(driver, USERNAME_INPUT, user)
    click(driver, BTN_AVANCAR, timeout=10)

    # senha
    visible(driver, PASSWORD_INPUT, timeout=10)
    fill(driver, PASSWORD_INPUT, passwd)
    click(driver, BTN_AVANCAR, timeout=10)

    # confirmação via minicart
    end = time.time() + 20
    while time.time() < end:
        if minicart_visible(driver):
            try_close_popups(driver)
            return
        time.sleep(0.2)

    driver.save_screenshot("debug_login_failed.png")
    raise TimeoutException(
        "Login não confirmou: mini-cart não ficou visível."
    )


def expect_login_popup(driver, wait, label="login_popup", timeout=12, retries=2, sleep_between=0.6):
    """
    Confirma que o pop-up de login do header abriu.
    Critério: aparecer USERNAME_INPUT ou BTN_AVANCAR (depende do estado do modal).
    Faz pequenas tentativas antes de falhar.
    """
    last_exc = None

    for attempt in range(retries + 1):
        try:
            end = time.time() + timeout
            while time.time() < end:
                # qualquer um dos dois já prova que o popup abriu
                if driver.find_elements(*USERNAME_INPUT) or driver.find_elements(*BTN_AVANCAR):
                    # garante visibilidade real
                    if driver.find_elements(*USERNAME_INPUT):
                        wait.until(EC.visibility_of_element_located(USERNAME_INPUT))
                    else:
                        wait.until(EC.visibility_of_element_located(BTN_AVANCAR))
                    return True

                time.sleep(0.2)

            raise TimeoutException("Popup não apareceu dentro do timeout.")
        except (TimeoutException, StaleElementReferenceException) as e:
            last_exc = e
            time.sleep(sleep_between)

    raise last_exc
