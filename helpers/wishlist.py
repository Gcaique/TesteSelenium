import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers.actions import *
from helpers.waiters import visible
from helpers.popups import try_close_popups
from helpers.minicart import *

from locators.wishlist import *
from locators.header import LOGIN_NAME_CONTAINER, DD_FAVORITOS



def wait_favorite_status(driver, timeout=12):
    """
    Algumas telas mudam por title='Favorito', outras por class add-to-wishlist.
    Então aceitamos qualquer uma como confirmação.
    """
    end = time.time() + timeout
    while time.time() < end:
        if driver.find_elements(*WISHLIST_STATUS_FAVORITO):
            return True
        if driver.find_elements(*WISHLIST_STATUS_ADDED_CLASS):
            return True
        time.sleep(0.2)
    return False


# Abrir lista de favoritos
def open_favorites_page(driver, wait):
    safe_click_loc(driver, wait, LOGIN_NAME_CONTAINER, timeout=12)
    time.sleep(0.3)
    safe_click_loc(driver, wait, DD_FAVORITOS, timeout=12)
    time.sleep(2)


# Interações nos cards da Lista de favoritos
def wishlist_increment_by_index(driver, wait, idx: int):
    safe_click_loc(driver, wait, WISHLIST_INCREMENT_BY_INDEX(idx), timeout=12)


def wishlist_decrement_by_index(driver, wait, idx: int):
    safe_click_loc(driver, wait, WISHLIST_DECREMENT_BY_INDEX(idx), timeout=12)


def wishlist_set_qty_input_by_index(driver, idx: int, value: str, timeout=15):
    """
    Ajusta qty em input numerico.
    """
    inputs = WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located(WISHLIST_QTY_INPUTS)
    )

    target = inputs[idx - 1]  # idx humano (1..N)
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
    driver.execute_script("arguments[0].focus();", target)
    time.sleep(0.2)

    try:
        target.clear()
    except Exception:
        driver.execute_script("arguments[0].value='';", target)

    target.send_keys(value)


def wishlist_add_item_to_cart_by_index(driver, wait, idx: int):
    safe_click_loc(driver, wait, WISHLIST_TOCART_BTN_BY_INDEX(idx), timeout=15)
    wait_minicart_loading(driver)
    time.sleep(1.5)


# Interação com o botão Adicionar todos ao carrinho
def wishlist_add_all_to_cart(driver, wait):
    safe_click_loc(driver, wait, WISHLIST_ADD_ALL_TO_CART, timeout=12)
    wait_minicart_loading(driver)
    time.sleep(1.5)



# Avise-me (Wishlist)
def wishlist_avise_me_flow(driver, wait):
    """
      - clica Avise-me (disabled)
      - espera o botão virar enabled
      - dá refresh
      - valida que continua enabled
      - clica Avise-me (enabled)
    """

    # clica no Avise-me (estado "disabled")
    scroll_and_safe_click_loc(driver, wait, BTN_AVISE_DISABLED, timeout=20)

    # espera trocar para enabled
    time.sleep(5)

    # refresh na página
    driver.refresh()

    # após refresh, valida que o botão segue enabled
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(BTN_AVISE_ENABLED)
    )

    # clica no Avise-me enabled
    scroll_and_safe_click_loc(driver, wait, BTN_AVISE_ENABLED, timeout=20)

    # aguarda alguma mudança/feedback pós clique
    time.sleep(4)


# Remoção + Confirmação
def remove_card_item_with_confirm(driver, wait, idx: int):
    '''Remove produto da lista de favoritos localizado no card'''
    safe_click_loc(driver, wait, REMOVE_CARD_BTN_BY_INDEX(idx), timeout=15)
    visible(driver, CONFIRM_MODAL_ACCEPT, timeout=15)
    safe_click_loc(driver, wait, CONFIRM_MODAL_ACCEPT, timeout=15)
    time.sleep(1.0)
