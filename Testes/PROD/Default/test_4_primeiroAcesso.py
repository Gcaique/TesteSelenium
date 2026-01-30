import time

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.header import LOGIN_MENU, USERNAME_INPUT, BTN_AVANCAR

from helpers.firstAcess import *
from helpers.waiters import minicart_visible

# =========================
# Credenciais
# =========================
VALID_USER = "caique.oliveira2@infobase.com.br"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.primeiroAcesso
def test_4_primeiro_acesso(driver, setup_site, wait):


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
    send_code_by_email(driver, wait)

    # 4) Modal de inserção do token / token iválido
    validate_token(driver, wait, "456789")

    # 5) Token válido
    validate_token(driver, wait, "456798")

    # 6) Criar email inválido
    create_password(driver, wait, "automatizacao@teste", "Min@1234", "Min@1234")

    # 7) Criar senha inválida
    create_password_invalid(driver, wait, "caique.oliveira2@infobase.com.br", "min@123", "Min@1234")

    # 8) Criar confirmar senha inválida
    create_password_invalid(driver, wait, "caique.oliveira2@infobase.com.br", "Min@1234", "min@1234")

    # 9) Criar credenciais finais válidas
    create_password(driver, wait, "caique.oliveira2@infobase.com.br", "Min@1234", "Min@1234")

    # 10) Apresentação da modal de conclusão
    close_success_modal(driver, wait)

    # 11) Apresentação da Home Page Logada
    WebDriverWait(driver, 20).until(lambda d: minicart_visible(d), message="Era para estar logado após primeiro acesso.")