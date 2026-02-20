from selenium.webdriver.common.by import By

#-----------------------------------------------------------------------
# Mini-cart
#-----------------------------------------------------------------------
VIEWCART = (By.XPATH, "//a[@class='action viewcart']")
MINICART_ICON = (By.XPATH, "//*[@class='action showcart']")
MINICART_ACTIVE = (By.XPATH, "//*[@class='action showcart active']")
MINICART_CLOSE = (By.ID, "btn-minicart-close")
MINICART_EMPTY = (By.XPATH, "//*[@class='empty-content']")
MINICART_EMPTY_VIEW_PRODUCTS = (By.XPATH, "//*[@class='empty-content']//a")
REMOVE_SIMPLE_DELETE_BY_INDEX = lambda idx: (By.XPATH, f"(//*[@class='product-photo-wishilist-remove-wrapper']//a[@class='action delete'])[{idx}]",)


MINICART_LIST = (By.CSS_SELECTOR, "ol#mini-cart.minicart-items")
MINICART_ITEMS = (By.CSS_SELECTOR, "ol#mini-cart li.product-item")
MINICART_WISHLIST_BTN_IN_ITEM = (By.CSS_SELECTOR, "button[id^='button_wishlist_']")

# Loading minicart
MINICART_LOADING_1 = (By.XPATH, "//*[@class='minicart-wrapper is-loading active']") # Quando o mini-cart não está sendo apresentado na página
MINICART_LOADING_2 = (By.XPATH, "//*[@class='minicart-wrapper active is-loading']") # Quando o mini-cart está sendo apresentado na página
MINICART_LOADING_3 = (By.XPATH, "//*[@class='minicart-wrapper is-loading']")

# alertas
MINICART_REMOVE_ALERT = (By.XPATH, "//*[@class='minicart-wrapper active']//*[contains(normalize-space(text()), 'Você rem')]")

BTN_CHECKOUT_TOP = (By.ID, "top-cart-btn-checkout")

#-----------------------------------------------------------------------
# Carrinho "/checkout/cart"
#-----------------------------------------------------------------------
EMPTY_CART_BTN = (By.XPATH, "//button[@id='empty_cart_button']/span")
EMPTY_CART_CONFIRM = (By.XPATH, "//button[@class='action-primary action-accept']")
VER_CATALOGO = (By.XPATH, "//a[@class='action primary']")
SUMARY_EXPAND = (By.XPATH, "//*[@class='summary-floating __expand']")
SUMARY_EXPAND_ARROW = (By.XPATH, "//*[@class='summary-floating __expand']/img")