import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import requests

from locators.firstAcess import *



def ensure_visible_in_modal(driver, element):
    # scroll dentro do modal / viewport
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)


def open_first_access_modal(driver, wait):
    wait.until(EC.visibility_of_element_located(FIRST_ACCESS_CREATE_PASSWORD))
    driver.find_element(*FIRST_ACCESS_CREATE_PASSWORD).click()


def send_code_by_email(driver, wait):
    wait.until(EC.element_to_be_clickable(SEND_BY_EMAIL)).click()
    wait.until(EC.element_to_be_clickable(EMAIL_OPTION_2)).click()
    wait.until(EC.element_to_be_clickable(BTN_SEND_CODE_2)).click()


def validate_token(driver, wait, token):
    wait.until(EC.visibility_of_element_located(TOKEN_INPUT))
    el = driver.find_element(*TOKEN_INPUT)
    el.clear()
    el.send_keys(token)

    wait.until(EC.element_to_be_clickable(BTN_VERIFY_TOKEN)).click()


def create_password(driver, wait, email, password, confirm):
    wait.until(EC.visibility_of_element_located(EMAIL_FIRST_ACCESS))

    el_email = driver.find_element(*EMAIL_FIRST_ACCESS)
    ensure_visible_in_modal(driver, el_email)
    el_email.clear()
    el_email.send_keys(email)

    el_pass = driver.find_element(*PASSWORD_FIRST_ACCESS)
    ensure_visible_in_modal(driver, el_pass)
    el_pass.clear()
    el_pass.send_keys(password)

    el_confirm = driver.find_element(*CONFIRM_PASSWORD)
    ensure_visible_in_modal(driver, el_confirm)
    el_confirm.clear()
    el_confirm.send_keys(confirm)

    wait.until(EC.element_to_be_clickable(BTN_SAVE_ACCOUNT)).click()


def create_password_invalid(driver, wait, email, password, confirm):
    wait.until(EC.visibility_of_element_located(EMAIL_FIRST_ACCESS))

    el_email = driver.find_element(*EMAIL_FIRST_ACCESS)
    ensure_visible_in_modal(driver, el_email)
    el_email.clear()
    el_email.send_keys(email)

    el_pass = driver.find_element(*PASSWORD_FIRST_ACCESS)
    ensure_visible_in_modal(driver, el_pass)
    el_pass.clear()
    el_pass.send_keys(password)

    el_confirm = driver.find_element(*CONFIRM_PASSWORD)
    ensure_visible_in_modal(driver, el_confirm)
    el_confirm.clear()
    el_confirm.send_keys(confirm)

    # NÃO use element_to_be_clickable em botão disabled
    btn = wait.until(EC.presence_of_element_located(BTN_SAVE_ACCOUNT))
    ensure_visible_in_modal(driver, btn)

    # Valida atributo disabled
    wait.until(lambda d: btn.get_attribute("disabled") is not None)
    return True


def close_success_modal(driver, wait):
    wait.until(EC.visibility_of_element_located(BTN_CLOSE_MODAL_LOGIN))
    driver.find_element(*BTN_CLOSE_MODAL_LOGIN).click()


def reset_first_access(email: str):
    """
    Reseta o 'primeiro acesso' do usuário via API (equivalente ao que você faz no Apidog).
    Você precisa ajustar URL e payload conforme sua chamada real.
    """
    base = os.getenv("FIRST_ACCESS_API_BASE_URL", "").rstrip("/")
    token = os.getenv("FIRST_ACCESS_API_TOKEN", "")

    if not base or not token:
        raise RuntimeError(
            "Defina FIRST_ACCESS_API_BASE_URL e FIRST_ACCESS_API_TOKEN no .env"
        )

    url = f"{base}/first-access/reset"  # <-- ajuste conforme endpoint real
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"email": email}

    r = requests.post(url, json=payload, headers=headers, timeout=20)
    if r.status_code >= 400:
        raise AssertionError(f"Falha ao resetar primeiro acesso. {r.status_code} -> {r.text}")

    return True
