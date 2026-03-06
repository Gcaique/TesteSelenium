from selenium.webdriver.common.by import By


# ── Home Page ────────────────────────────────────────────────────────────────
LAST_ORDERS_BTN = (By.XPATH, "//a[@id='last-orders-action']")
LAST_ITEMS_BTN = (By.XPATH, "//a[@id='last-items-action']")


# ── Login Modal ──────────────────────────────────────────────────────────────
LOGIN_SEND_BTN = (
    By.XPATH,
    "//*[@class='secondary login-name']//button[@id='send2']",
)
USERNAME_INPUT = (By.XPATH, "//input[@id='username']")
PASSWORD_INPUT = (By.XPATH, "//*[@name='login[password]']")


# ── Spin To Win (Roleta de Cupons) ──────────────────────────────────────────
SPIN_CLOSE_BTN = (
    By.XPATH,
    "//button[@class='action-close hj-spintowin-close_button']",
)


# ── Filtro (Ultimos Pedidos / Comprados Recentemente) ───────────────────────
PERIOD_SELECT = (By.XPATH, "//select[@id='period']")
PERIOD_LAST_7_DAYS = (
    By.XPATH,
    "//select[@id='period']//option[@value='last_seven_days']",
)
FILTER_BTN = (
    By.XPATH,
    "//button[@class='hj-filter__action-change-filter']",
)
FILTER_BTN_DISABLED = (
    By.XPATH,
    "//button[@class='hj-filter__action-change-filter button-disabled']",
)
CLEAR_FILTER_LINK = (
    By.XPATH,
    "//a[normalize-space(text())='Limpar filtro']",
)


# ── Ultimos Pedidos - Grid ──────────────────────────────────────────────────
LAST_ORDERS_ADD_CART_BTN = (
    By.XPATH,
    "(//button[@class='hj-last-orders__order-additional-info-action-button "
    "hj-action-switch-btn'])[1]",
)


# ── Ultimos Pedidos - Ver Similar ───────────────────────────────
# Botao Ver Similar habilitado dentro de um pedido com "Adicionar pedido" habilitado
VER_SIMILAR_REFAZER_BTN = (
    By.XPATH,
    "(//div[contains(@class,'hj-last-orders__order-items') and @data-order-id]"
    "[ancestor::div[contains(@class,'hj-last-orders__order')][1]"
    "//button[contains(@class,'hj-last-orders__order-additional-info-action-button')"
    "and contains(@class,'hj-action-switch-btn')"
    "and not(@disabled)and not(@aria-disabled='true')]]"
    "//button[contains(@class,'hj-last-orders__order-item-card-action-switch-btn')"
    "and contains(@class,'js-switch-btn')"
    "and not(@disabled)and not(@aria-disabled='true')])[1]",
)

# Botao "Adicionar pedido ao carrinho" do pedido que contem o Ver Similar trocado
ADD_ORDER_WITH_SIMILAR_BTN = (
    By.XPATH,
    "(//div[contains(@class,'hj-last-orders__order-items') and @data-order-id]"
    "[.//button[contains(@class,'hj-last-orders__order-item-card-action-switch-btn') "
    "and contains(@class,'js-switch-btn')]]"
    "/ancestor::div[contains(@class,'hj-last-orders__order')][1]"
    "//button[contains(@class,'hj-last-orders__order-additional-info-action-button')"
    "and contains(@class,'hj-action-switch-btn')"
    "and not(@disabled)and not(@aria-disabled='true')])[1]",
)


# ── Comprados Recentemente ──────────────────────────────────────────────────
ADD_ALL_TO_CART_BTN = (
    By.XPATH,
    "//button[@class='customer-orders __action primary "
    "hj-last-items__action-add-all-to-cart']",
)
PAGE_SIZE = (By.XPATH, "//*[@class='page-size']")

FAVORITE_BTN_FIRST = (
    By.XPATH,
    "(//*[@class='product details product-item-details']"
    "//button[@title='Favorito'])[1]",
)
FAVORITE_ON_WISHLIST_FIRST = (
    By.XPATH,
    "(//*[@class='product details product-item-details']"
    "//button[@class='action add-to-wishlist onwishlist "
    "hj-product_card-add_to_wishlist'])[1]",
)
FAVORITE_ADD_TO_FIRST = (
    By.XPATH,
    "(//*[@class='product details product-item-details']"
    "//button[@title='Adicionar aos favoritos'])[1]",
)


# ── Comprados Recentemente - Avise-me ─────────────────────────
AVISE_ME_SPAN = (
    By.XPATH,
    "//a[contains(@class, 'action alert primary')]//span",
)
AVISE_ME_CLICKED_SPAN = (
    By.XPATH,
    "//a[contains(@class, 'alert-active clicked')]//span",
)


# ── Comprados Recentemente - Ver Similar ──────────────────────
VER_SIMILAR_COMPRADOS_BTN = (
    By.XPATH,
    "(//button[@class='hj-action-switch-btn js-switch-btn'])[1]",
)
SWITCH_BACK_BTN = (
    By.XPATH,
    "//button[@class='js-switch-back hj-last-orders__order-item-action-switch-back']",
)

# Incrementar qty no card do produto similar (dentro do card que tem o botao Voltar)
SIMILAR_INCREMENT_QTY = (
    By.XPATH,
    "//li[contains(@class,'product-item')]"
    "[.//button[contains(@class, 'js-switch-back') "
    "and contains(@class, 'hj-last-orders__order-item-action-switch-back')]]"
    "//button[contains(@class, 'increment-qty') "
    "and contains(@class, 'hj-product_card-increment_qty')]",
)

# Decrementar qty no card do produto similar
SIMILAR_DECREMENT_QTY = (
    By.XPATH,
    "//li[contains(@class,'product-item')]"
    "[.//button[contains(@class,'js-switch-back') "
    "and contains(@class,'hj-last-orders__order-item-action-switch-back')]]"
    "//button[contains(@class,'decrement-qty')"
    "and contains(@class,'hj-product_card-decrement_qty')]",
)

# Botao Adicionar do card do produto similar
SIMILAR_ADD_TO_CART_BTN = (
    By.XPATH,
    "//div[contains(@class,'product-item-info')]"
    "[.//button[contains(@class,'js-switch-back') "
    "and contains(@class,'hj-last-orders__order-item-action-switch-back')]]"
    "//button[contains(@class,'action')"
    "and contains(@class,'tocart') "
    "and contains(@class,'hj-product_card-btn_buy')]",
)


# ── Comprados Recentemente - Qty + Add individual ─────────────
INCREMENT_QTY_SECOND = (
    By.XPATH,
    "(//div[@class='product-item-qty-container']"
    "//button[@class='increment-qty hj-product_card-increment_qty'])[2]",
)
DECREMENT_QTY_SECOND = (
    By.XPATH,
    "(//div[@class='product-item-qty-container']"
    "//button[@class='decrement-qty hj-product_card-decrement_qty'])[2]",
)
ADD_TO_CART_SECOND = (
    By.XPATH,
    "(//button[contains(@class, 'action tocart primary tocart')])[2]",
)


# ── Mini Cart ───────────────────────────────────────────────────────────────
MINICART_LOADING = (
    By.XPATH,
    "//*[@class='minicart-wrapper is-loading active']",
)
MINICART_ACTIVE_LOADING = (
    By.XPATH,
    "//*[@class='minicart-wrapper active is-loading']",
)
CHECKOUT_BTN = (By.XPATH, "//button[@id='top-cart-btn-checkout']")


# ── Checkout - Shipping ─────────────────────────────────────────────────────
SHIPPING_NEXT_BTN = (
    By.XPATH,
    "//*[@id='shipping-method-buttons-container']//button",
)
CUPONS_EXPANDED = (
    By.XPATH,
    "//form[@id='discount-form']//label[@aria-expanded='true']",
)
CUPONS_COLLAPSED = (
    By.XPATH,
    "//form[@id='discount-form']//label[@aria-expanded='false']",
)


# ── Checkout - Payment ──────────────────────────────────────────────────────
BODY_AJAX_LOADING = (
    By.XPATH,
    "//body[@class='checkout-index-index page-layout-checkout ajax-loading']",
)
BOLETO_LABEL = (By.XPATH, "//label[@for='checkmo']")
BOLETO_CONDITIONS_SELECT = (By.XPATH, "//*[@id='payment-conditions-checkmo']")
BOLETO_COND_21 = (
    By.XPATH,
    "//*[@id='payment-conditions-checkmo']/option[@value='21']",
)
BOLETO_COND_28 = (
    By.XPATH,
    "//*[@id='payment-conditions-checkmo']/option[@value='28']",
)
TERMS_CHECKBOX = (
    By.XPATH,
    "//*[@id='terms_conditions_checkmo_agreement']",
)
FINALIZAR_COMPRA_BTN = (
    By.XPATH,
    "(//button[@class='action primary checkout hj-checkout-action_primary']"
    "/span[normalize-space(text())='Finalizar compra'])[1]",
)


# ── Checkout - Success ──────────────────────────────────────────────────────
SUCCESS_PAGE_BODY = (
    By.XPATH,
    "//body[@class='checkout-onepage-success page-layout-1column mm-wrapper']",
)
IR_PARA_HOME_BTN = (
    By.XPATH,
    "//a[@class='action primary continue']",
)


# ── Menu Usuario / Meus Pedidos ─────────────────────────────────────────────
LOGIN_NAME_MENU = (By.XPATH, "//div[@class='login-name']")
MEUS_PEDIDOS_LINK = (
    By.XPATH,
    "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pedidos']",
)
ORDERS_PAGINATION_SELECT = (
    By.XPATH,
    "//*[@class='order-pagination __items-per-page']//select",
)
FORMA_PAGAMENTO_COL = (By.XPATH, "(//th[@class='col status sort'])[3]")
ORDER_DETAIL_FIRST = (
    By.XPATH,
    "(//table[@id='my-orders-table']//a[@class='action view'])[1]",
)
ORDERS_TABLE = (By.XPATH, "//table[@id='my-orders-table']")
REORDER_BTN = (By.XPATH, "//a[@class='reorder']")
