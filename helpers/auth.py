import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

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


#TESTE_1
def expect_login_popup(driver, wait, label="login_popup"):
    """
       Confirma que o pop-up de login abriu.
       Como você usa ID 'username', esperamos ele aparecer.
       Se falhar, salva screenshot pra você enxergar o estado real da tela.
       """
    try:
        wait.until(EC.visibility_of_element_located(USERNAME_INPUT))
    except TimeoutException:
        driver.save_screenshot(f"debug_{label}_timeout.png")
        raise
