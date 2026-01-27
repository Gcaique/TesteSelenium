from selenium.webdriver.common.by import By

# Mini-cart
VIEWCART = (By.XPATH, "//a[@class='action viewcart']")
MINICART_ICON = (By.XPATH, "//*[@class='action showcart']")
MINICART_ACTIVE = (By.XPATH, "//*[@class='action showcart active']")
MINICART_CLOSE = (By.ID, "btn-minicart-close")
# Loading minicart
MINICART_LOADING_1 = (By.XPATH, "//*[@class='minicart-wrapper is-loading active']") # Quando o mini-cart não está sendo apresentado na página
MINICART_LOADING_2 = (By.XPATH, "//*[@class='minicart-wrapper active is-loading']") # Quando o mini-cart está sendo apresentado na página


# Carrinho "/checkout/cart"
EMPTY_CART_BTN = (By.XPATH, "//button[@id='empty_cart_button']/span")
EMPTY_CART_CONFIRM = (By.XPATH, "//button[@class='action-primary action-accept']")
VER_CATALOGO = (By.XPATH, "//a[@class='action primary']")