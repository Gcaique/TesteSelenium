from selenium.webdriver.common.by import By

# PDP (entrada na PDP + ações)
FIRST_PRODUCT_PLP = (By.XPATH, "(//*[contains(@id,'product-item-info')][.//button[@title='Adicionar']]//span[@class='product-image-wrapper'])[1]") # Serve para acessar o primeiro produto de outras categorias com estoque disponivel
PDP_INCREMENT = (By.XPATH, "(//button[@class='increment-qty hj-product_card-increment_qty'])[1]")
PDP_ADD_TO_CART = (By.ID, "product-addtocart-button")
PRODUCT_TITLES = (By.XPATH, "//*[contains(@id,'product-item-info')]//strong")

# Previsão de entrega (PDP)
ADDRESSES_SELECT = (By.ID, "addresses")
ADDRESSES_OPT2 = (By.XPATH, "//*[@id='addresses']/option[2]")
BTN_VERIFY_FORECAST = (By.ID, "verify-delivery-forecast")
FORECAST_RESULT = (By.XPATH, "//*[@class='shipping-rate-result']")

#Botões que exigem login
BTN_ENTRAR_PDP = (By.XPATH, "//button[contains(@class,'loggin-btn') and contains(@class,'tget-btn-buy')]")