from selenium.webdriver.common.by import By

# Carrossel / produto / botão adicionar (home)
CAROUSEL_1 = (By.XPATH, "(//div[contains(@class, 'slider-products')])[1]")
QTY_INPUT_FIRST = (By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]")
ADD_BTN_FIRST_CAROUSEL = (By.XPATH, "(//*[@class='slick-slide slick-current slick-active']//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]")

# Icone favorito
HOME_CAROUSEL_1 = (By.XPATH, "(//div[contains(@class,'slider-products')])[1]")
FIRST_PRODUCT_CARD = (By.XPATH, ".//li[contains(@class,'product-item')][1]")
WISHLIST_BTN_INSIDE = (By.XPATH, ".//button[contains(@id,'button_wishlist')]")

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

# =====================================================
# HOME - COOKIES
# =====================================================

BTN_COOKIES = (
    By.XPATH,
    "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']"
)

# =====================================================
# HOME - REGIÃO
# =====================================================

BTN_OUTRAS_REGIOES = (
    By.ID,
    "other-regions"
)

# =====================================================
# HOME - MODAL CLIENTE
# =====================================================

BTN_QUERO_SER_CLIENTE = (
    By.XPATH,
    "//button[@id='modal-customer-open']/span[normalize-space(text())='Quero ser cliente']"
)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
# Icone favorito
MOBILE_HOME_CAROUSEL_1 = (By.XPATH, "(//div[contains(@class,'slider-products')])[1]") # HOME - CAROUSEL 1
MOBILE_HOME_CAROUSEL_ACTIVE_PRODUCT_CARD = (By.XPATH, ".//li[contains(@class,'product-item')]") # CARD dentro do slide ativo
MOBILE_HOME_CAROUSEL_WISHLIST_BTN = (By.XPATH, ".//button[contains(@id,'button_wishlist')]") # Botão wishlist dentro do card
# SLIDE ATIVO (ignora clonados)
MOBILE_HOME_CAROUSEL_ACTIVE_SLIDE = (
    By.XPATH,
    ".//div[contains(@class,'slick-slide') "
    "and contains(@class,'slick-active') "
    "and not(contains(@class,'slick-cloned'))]"
)