from selenium.webdriver.common.by import By

# Carrossel / produto / botão adicionar (home)
CAROUSEL_1 = (By.XPATH, "(//div[contains(@class, 'slider-products')])[1]")
QTY_INPUT_FIRST = (By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]")
ADD_BTN_FIRST_CAROUSEL = (By.XPATH, "(//*[@class='slick-slide slick-current slick-active']//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]")
# Icone favorito
HOME_WISHLIST_BTN_1 = (By.XPATH, "(//button[contains(@id,'button_wishlist')])[1]")

# Carrossel / Mapa de cortes / Footer - Interação com o scroll da home
BRANDS_CAROUSEL = (By.XPATH, "//div[@class='brands-carousel']")
CUTTING_MAP = (By.XPATH, "//*[@class='cutting-map __home-section']")
FOOTER = (By.XPATH, "//div[@class='footer-content']")

# Refazer pedido / comprados recentemente
LAST_ORDERS = (By.ID, "last-orders-action")
LAST_ITEMS = (By.ID, "last-items-action")

# Seções home (scroll)
HOME_SECTIONS = [
    "(//div[contains(@class, 'slider-products')])[1]",
    "//div[@class='brands-carousel']",
    "(//div[contains(@class, 'slider-products')])[2]",
    "//*[@class='cutting-map __home-section']",
    "//div[@class='footer-content']"
]