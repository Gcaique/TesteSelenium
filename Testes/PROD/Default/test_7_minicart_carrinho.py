import pytest
from locators.checkout import *
from helpers.plp import *
from helpers.auth import *
from helpers.popups import *
from helpers.minicart import *


VALID_USER = "caique.oliveira4@infobase.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.logado
def test_7_minicart_carrinho(driver, setup_site, wait):
    """
    Fluxo completo de MiniCart + Carrinho.
    """

    # 1) Login
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    wait.until(EC.visibility_of_element_located(MINICART_ICON))
    try_close_popups(driver)

    # 2) Categoria Bovinos
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # 3) Favoritar no MiniCart
    wishlist_toggle_add_towishlist(driver, wait, index=1)

    # 4) Incrementar 2x
    MINICART_INCREMENT_BTN = (
        By.CSS_SELECTOR,
        "#mini-cart li.product-item button.action.increase"
    )

    # 5) Decrementar
    MINICART_DECREMENT_BTN = (
        By.CSS_SELECTOR,
        "#mini-cart li.product-item button.action.decrease"
    )

    # 6) Remover (cancelar)
    click_when_clickable(wait, MC_DELETE_BTN)
    click_when_clickable(wait, MC_MODAL_DISMISS)

    # 7) Remover (confirmar)
    if driver.find_elements(*MINICART_ITEMS):
        items = driver.find_elements(*MINICART_ITEMS)

        if len(items) > 0:
            try:
                minicart_empty(driver, wait)
            except Exception:
                pass

    wait.until(lambda d: len(d.find_elements(*MINICART_ITEMS)) == 0)

    wait.until(EC.visibility_of_element_located(MINICART_EMPTY))

    # 8) Ver produtos
    click_when_clickable(wait, MINICART_EMPTY_VIEW_PRODUCTS)

    # 9) Categoria Azeite
    click_when_clickable(wait, CATEGORY_MENU("Azeite"))
    wait_category_loaded(wait, driver)

    scroll_into_view(driver, TOOLBAR_AMOUNT)
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # 10) Categoria Bovinos Premium
    click_when_clickable(wait, CATEGORY_MENU("Bovinos Premium"))
    wait_category_loaded(wait, driver)
    scroll_into_view(driver, TOOLBAR_AMOUNT)

    # Produto 1 (2x incremento)
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(1))
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(1))
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(1))
    wait_minicart_ready(driver)

    # Produto 2
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(2))
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(2))
    wait_minicart_ready(driver)

    # Produto 3 (3x incremento)
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(3))
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(3))
    click_when_clickable(wait, PLP_INCREMENT_BY_INDEX(3))
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(3))
    wait_minicart_ready(driver)

    # Produto 4
    safe_click_loc(driver, wait, PLP_ADD_TO_CART_BY_INDEX(4))
    wait_minicart_ready(driver)

    # 11) Lista de Favoritos

    # fecha o minicart se estiver aberto
    if driver.find_elements(*MINICART_ACTIVE):
        click_when_clickable(wait, MINICART_CLOSE)

    wait.until(EC.invisibility_of_element_located(MINICART_ACTIVE))

    driver.execute_script("window.scrollTo(0,0);")

    from selenium.webdriver import ActionChains

    # hover no nome do usuário
    user_menu = wait.until(EC.visibility_of_element_located(LOGIN_NAME_CONTAINER))
    ActionChains(driver).move_to_element(user_menu).perform()

    # clique JS no item favoritos
    fav = wait.until(EC.presence_of_element_located(DD_FAVORITOS))
    driver.execute_script("arguments[0].click();", fav)

    # espera URL mudar
    wait.until(lambda d: "/wishlist" in d.current_url)

    try:
        # adiciona o primeiro item dos favoritos ao carrinho
        click_when_clickable(wait, WISHLIST_TOCART_BTN_BY_INDEX(1))

        # espera o minicart atualizar
        wait_minicart_ready(driver)

    except:
        pass

    # 12) Finalizar Compra via MiniCart

    wait_minicart_ready(driver)

    click_when_clickable(wait, BTN_CHECKOUT_TOP)
    wait.until(EC.visibility_of_element_located(BTN_CONTINUAR_SHIPPING))

    # 13) Voltar Home
    click_when_clickable(wait, LOGO)

    # 14) Ir para Carrinho
    click(driver, MINICART_ICON)
    wait_minicart_ready(driver)

    click_when_clickable(wait, VIEWCART)
    wait.until(EC.url_contains("/checkout/cart"))

    # 15) Alterar qty segundo item para 0
    cart_qty_inputs = wait.until(
        EC.visibility_of_all_elements_located(CART_PRODUCT_QTY_INPUT)
    )
    cart_qty_inputs[1].clear()
    cart_qty_inputs[1].send_keys("0")

    CART_PRODUCT_ROW = (By.CSS_SELECTOR, "tbody.cart.item")

    # 16) Remover segundo item manualmente
    cart_remove_buttons = wait.until(
        EC.presence_of_all_elements_located(CART_REMOVE_PRODUCT_BTN)
    )
    btn = driver.find_elements(*CART_REMOVE_PRODUCT_BTN)[1]
    driver.execute_script("arguments[0].click();", btn)

    # 17) Finalizar compra pelo carrinho

    wait.until(lambda d: len(d.find_elements(*CART_PROCEED_CHECKOUT)) > 0)

    btn_checkout = driver.find_element(*CART_PROCEED_CHECKOUT)

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_checkout)
    driver.execute_script("arguments[0].click();", btn_checkout)

    wait.until(EC.url_contains("/checkout"))

    # 18) Voltar direto para o carrinho
    driver.get("https://meuminerva.com/checkout/cart/")
    wait.until(EC.url_contains("/checkout/cart"))

    # 19) Limpar carrinho
    click_when_clickable(wait, EMPTY_CART_BTN)
    click_when_clickable(wait, MC_MODAL_ACCEPT)

    wait.until(EC.visibility_of_element_located(CART_EMPTY_MESSAGE))


