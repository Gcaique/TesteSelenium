from selenium.webdriver.common.by import By

#-----------------------------------------------------------------------
# MINI-CART
#-----------------------------------------------------------------------
VIEWCART = (By.XPATH, "//a[@class='action viewcart']")
MINICART_ICON = (By.XPATH, "//*[@class='action showcart']")
MINICART_ACTIVE = (By.XPATH, "//*[@class='action showcart active']")
MINICART_CLOSE = (By.ID, "btn-minicart-close")
MINICART_EMPTY = (By.XPATH, "//*[@class='empty-content']")
MINICART_EMPTY_VIEW_PRODUCTS = (By.XPATH, "//*[@class='empty-content']//a")
REMOVE_SIMPLE_DELETE_BY_INDEX = lambda idx: (By.XPATH, f"(//*[@class='product-photo-wishilist-remove-wrapper']//a[@class='action delete'])[{idx}]",)

# Botões do ações
MINICART_PRODUCT_NAME = (By.CSS_SELECTOR, "#mini-cart li.product-item strong.product-item-name a")
MINICART_PRODUCT_PRICE = (By.CSS_SELECTOR, "#mini-cart li.product-item span.price")
MINICART_PRODUCT_QTY = (By.CSS_SELECTOR, "#mini-cart li.product-item input.qty")
MINICART_LIST = (By.CSS_SELECTOR, "ol#mini-cart.minicart-items")
MINICART_ITEMS = (By.CSS_SELECTOR, "ol#mini-cart li.product-item")
MINICART_ITEMS_BY_INDEX = lambda idx: (By.XPATH, f"(//a[@class='hj-minicart_product-item'])[{idx}]")
MINICART_WISHLIST_BTN_IN_ITEM = (By.CSS_SELECTOR, "button[id^='button_wishlist_']")
MINICART_INCREMENT_BTN = (By.XPATH, "(//ol[@id='mini-cart']//button[@class='increment-qty'])[1]") # Botão de incrementar quantidade (+) no minicart
MINICART_DECREMENT_BTN = (By.XPATH, "(//ol[@id='mini-cart']//button[@class='decrement-qty'])[1]") # Botão de decrementar quantidade (-) no minicart
MC_DELETE_BTN = (By.CSS_SELECTOR, "#mini-cart a.action.delete") # Botão de remover item no minicart
MC_MODAL_ACCEPT = (By.CSS_SELECTOR, "button.action-primary.action-accept") # Modal confirmar remoção


# Loading minicart
MINICART_LOADING_1 = (By.XPATH, "//*[@class='minicart-wrapper is-loading active']") # Quando o mini-cart não está sendo apresentado na página
MINICART_LOADING_2 = (By.XPATH, "//*[@class='minicart-wrapper active is-loading']") # Quando o mini-cart está sendo apresentado na página
MINICART_LOADING_3 = (By.XPATH, "//*[@class='minicart-wrapper is-loading']")

# alertas
MINICART_REMOVE_ALERT = (By.XPATH, "//*[@class='minicart-wrapper active']//*[contains(normalize-space(text()), 'Você rem')]")

BTN_CHECKOUT_TOP = (By.ID, "top-cart-btn-checkout")


#-----------------------------------------------------------------------
# CARRINHO "/checkout/cart"
#-----------------------------------------------------------------------
EMPTY_CART_BTN = (By.XPATH, "//button[@id='empty_cart_button']")
EMPTY_CART_CONFIRM = (By.XPATH, "//button[@class='action-primary action-accept']")
VER_CATALOGO = (By.XPATH, "//a[@class='action primary']")

# Botões do ações
CART_PRODUCT_IMG = (By.XPATH, "//a[@class='product-item-photo hj-cart-product_item_photo']")
CART_PRODUCT_QTY_INPUT = (By.CSS_SELECTOR, "input.qty")
CART_REMOVE_PRODUCT_BTN = (By.CSS_SELECTOR, "a.action-delete")
CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, "div.cart-empty")
CART_INCREMENT_BTN = lambda idx: (By.XPATH, f"(//*[@class='product']//button[@class='increment-qty hj-product_card-increment_qty'])[{idx}]")
CART_DECREMENT_BTN = lambda idx: (By.XPATH, f"(//*[@class='product']//button[@class='decrement-qty hj-product_card-decrement_qty'])[{idx}]")

# Botão "Finalizar Compra" dentro da página /checkout/cart
CART_PROCEED_CHECKOUT = (By.XPATH, "//ul[@class='checkout methods items checkout-methods-items']//button")


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

# MINI-CART
MOBILE_REMOVE_SIMPLE_DELETE_BY_INDEX = lambda idx: (By.XPATH, f"(//a[@class='action delete hj-minicart_product-item-delete'])[{idx}]",)

# ÍCONE do mini-cart (para ABRIR)
MOBILE_MINICART_ICON = (
    By.XPATH,
    "//div[contains(@class,'minicart-wrapper')]"
    "//a[@id='open-minicart' and contains(@class,'showcart') and contains(@class,'hj-header-minicart')]"
)

# Estado ABERTO
MOBILE_MINICART_OPENED = (
    By.XPATH,
    "//div[contains(@class,'minicart-wrapper') and contains(@class,'active')]"
    "//a[@id='open-minicart' and contains(@class,'showcart') and contains(@class,'active')]"
)

# BOTÃO FECHAR (X)
MOBILE_MINICART_CLOSE = (
    By.XPATH,
    "//div[contains(@class,'minicart-wrapper') and contains(@class,'active')]"
    "//*[self::button or self::a]"
    "["
    "(@id='btn-minicart-close')"
    " or (contains(@class,'action') and contains(@class,'close'))"
    " or contains(@class,'minicart-close')"
    " or translate(@aria-label,'FECHARCLOSE','fecharclose')='fechar'"
    " or translate(@aria-label,'FECHARCLOSE','fecharclose')='close'"
    " or translate(@title,'FECHARCLOSE','fecharclose')='fechar'"
    " or translate(@title,'FECHARCLOSE','fecharclose')='close'"
    "]"
)

# Estado FECHADO (wrapper sem active) - útil pra validar que fechou
MOBILE_MINICART_CLOSED = (
    By.XPATH,
    "//div[contains(@class,'minicart-wrapper') and not(contains(@class,'active'))]"
    "//a[@id='open-minicart' and contains(@class,'showcart') and contains(@class,'hj-header-minicart')]"
)


# CARRINHO
# Resumo do pedido
SUMARY_EXPAND = (By.XPATH, "//*[@class='summary-floating __expand']")
SUMARY_EXPAND_ARROW = (By.XPATH, "//*[@class='summary-floating __expand']/img")