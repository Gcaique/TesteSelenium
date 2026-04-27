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

def send_code_by_email_sul(driver, wait):
    wait.until(EC.element_to_be_clickable(SEND_BY_EMAIL)).click()
    wait.until(EC.element_to_be_clickable(EMAIL_OPTION)).click()
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


def close_success_modal(driver, wait):
    wait.until(EC.visibility_of_element_located(BTN_CLOSE_MODAL_LOGIN))
    driver.find_element(*BTN_CLOSE_MODAL_LOGIN).click()


# --- API (Magento) - helpers para resetar atributo de "primeiro acesso" via REST ---
_CUSTOMER_ID_BY_VIEW = {
    "default": 499,
    "sul": 481,
}


def _resolve_timeout_s(wait=None, timeout_s: int | float | None = None) -> int | float:
    """Resolve o timeout efetivo: usa `timeout_s`, senão `wait._timeout`, senão fallback 20s."""
    if timeout_s is not None:
        return timeout_s
    # WebDriverWait guarda o timeout selecionado via CLI (--timeout), usado pelo run_gui.py.
    t = getattr(wait, "_timeout", None)
    if isinstance(t, (int, float)) and t > 0:
        return t
    return 20


def _get_admin_token(base: str, *, wait=None, timeout_s: int | float | None = None) -> str:
    """Obtém um token Bearer de admin via endpoint do Magento (`/integration/admin/token`)."""
    user = (os.getenv("USER_ADMIN") or "").strip()
    password = (os.getenv("PASSWORD_ADMIN") or "").strip()
    if not user or not password:
        raise RuntimeError("Defina USER_ADMIN e PASSWORD_ADMIN no .env.")

    timeout_eff = _resolve_timeout_s(wait, timeout_s)
    url = f"{base}/integration/admin/token"

    r = requests.post(url, json={"username": user, "password": password}, timeout=timeout_eff)
    if r.status_code >= 400:
        raise AssertionError(f"Falha ao obter token admin. {r.status_code} -> {r.text}")

    # Magento geralmente retorna um JSON string (ex: "abc..."). requests.json() vira str.
    token = r.json()
    if not isinstance(token, str) or not token.strip():
        raise AssertionError(f"Token admin invalido: {token!r}")

    return token.strip()


def _get_custom_attr_value(custom_attrs, code: str) -> str | None:
    """Busca o valor de um `custom_attribute` pelo `attribute_code` e retorna como string (ou None)."""
    if not custom_attrs:
        return None
    for attr in custom_attrs:
        if (attr or {}).get("attribute_code") == code:
            raw = (attr or {}).get("value")
            if raw is None:
                return None
            try:
                return str(raw).strip()
            except Exception:
                return None
    return None


def reset_first_acess(*, view: str = "default", wait=None, timeout_s: int | float | None = None) -> bool:
    """
    Garante que o atributo `primeiro_acesso` esteja "0" via Magento 2 API.

    - Customer ID hardcoded por visao (default/sul).
    - Faz GET e pula PUT se ja estiver em 0 (evita chamadas desnecessárias).
    - PUT envia apenas os 3 custom_attributes obrigatórios:
      primeiro_acesso=0, tipologia=16423, status_financeiro=1.

    Config:
    - FIRST_ACCESS_API_BASE_URL deve incluir /rest/default/V1 (o path e ajustado para sul quando view="sul").
    - FIRST_ACCESS_API_TOKEN: token Bearer (Admin).

    Timeout:
    - Se `timeout_s` nao for informado, usa `wait._timeout` (mesmo timeout selecionado no run_gui.py via --timeout).
    """
    base = (os.getenv("FIRST_ACCESS_API_BASE_URL") or "").rstrip("/")

    if not base:
        raise RuntimeError("Defina FIRST_ACCESS_API_BASE_URL no .env.")

    if view not in _CUSTOMER_ID_BY_VIEW:
        raise ValueError(f"view invalida: {view}. Use: {list(_CUSTOMER_ID_BY_VIEW.keys())}")

    if view == "sul":
        base = base.replace("/rest/default/V1", "/rest/sul/V1")

    timeout_eff = _resolve_timeout_s(wait, timeout_s)
    customer_id = _CUSTOMER_ID_BY_VIEW[view]

    # Token dinamico por chamada (nao persistir em .env)
    token = _get_admin_token(base, wait=wait, timeout_s=timeout_s)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 1) GET customer para checar valor atual de primeiro_acesso
    get_url = f"{base}/customers/{customer_id}"
    r = requests.get(get_url, headers=headers, timeout=timeout_eff)
    if r.status_code >= 400:
        raise AssertionError(f"Falha no GET customer {customer_id} ({view}). {r.status_code} -> {r.text}")

    data = r.json() or {}
    customer = data.get("customer") if isinstance(data, dict) else None
    if not isinstance(customer, dict):
        customer = data if isinstance(data, dict) else {}

    custom_attrs = customer.get("custom_attributes") or []
    current_first_access = _get_custom_attr_value(custom_attrs, "primeiro_acesso")
    if current_first_access == "0":
        return True

    # 2) PUT apenas com atributos obrigatorios
    put_url = f"{base}/customers/{customer_id}"
    payload = {
        "customer": {
            "custom_attributes": [
                {"attribute_code": "primeiro_acesso", "value": "0"},
                {"attribute_code": "tipologia", "value": "16423"},
                {"attribute_code": "status_financeiro", "value": "1"},
            ]
        }
    }
    r2 = requests.put(put_url, json=payload, headers=headers, timeout=timeout_eff)
    if r2.status_code >= 400:
        raise AssertionError(f"Falha no PUT customer {customer_id} ({view}). {r2.status_code} -> {r2.text}")

    return True


# Alias para grafias usadas anteriormente.
reset_firts_acess = reset_first_acess
