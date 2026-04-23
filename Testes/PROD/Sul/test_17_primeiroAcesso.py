import time
import os

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.header import LOGIN_MENU, USERNAME_INPUT, BTN_AVANCAR

from helpers.firstAcess import *
from helpers.waiters import minicart_visible
from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("CAIQUE_OLIVEIRA5")


@pytest.mark.smoke
@pytest.mark.pipeline
@pytest.mark.sul
@pytest.mark.primeiroAcesso
def test_17_primeiro_acesso_sul(driver, setup_site, wait):
    # Garante pre-condicao via API: primeiro_acesso precisa estar "0" para este customer (visão Sul).
    reset_first_acess(view="sul", wait=wait)

    # 1) Abre login
    wait.until(EC.element_to_be_clickable(LOGIN_MENU)).click()

    wait.until(EC.visibility_of_element_located(USERNAME_INPUT))
    el_user = driver.find_element(*USERNAME_INPUT)
    el_user.clear()
    el_user.send_keys(VALID_USER)

    wait.until(EC.element_to_be_clickable(BTN_AVANCAR)).click()

    # 2) Modal de Primeiro acesso
    open_first_access_modal(driver, wait)

    # 3) Modal de seleção de e-mail
    send_code_by_email_sul(driver, wait)

    # 4) Token válido
    token_valid = (os.getenv("TOKEN") or "").strip()
    if not token_valid:
        pytest.fail('Defina TOKEN no .env/secrets para validar o token do primeiro acesso.')
    validate_token(driver, wait, token_valid)

    # 5) Criar credenciais válidas
    create_password(driver, wait, VALID_USER, VALID_PASS, VALID_PASS)

    # 6) Apresentação da modal de conclusão
    close_success_modal(driver, wait)

    # 7) Apresentação da Home Page Logada
    WebDriverWait(driver, 20).until(lambda d: minicart_visible(d), message="Era para estar logado após primeiro acesso.")
