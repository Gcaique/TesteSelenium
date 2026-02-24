from selenium.webdriver.common.by import By

# shipping step (Endereço)
BTN_CONTINUAR_SHIPPING = (By.XPATH, "//*[@id='shipping-method-buttons-container']//button")

# payment (Pagamento)
PIX = (By.XPATH, "//label[@for='dux_pay_pix']")
TERMS_PIX = (By.ID, "terms_conditions_dux_pay_pix_agreement")

BTN_FINALIZAR_COMPRA = (By.XPATH, "(//button[contains(@class,'action primary checkout')]//span[normalize-space()='Finalizar compra'])[1]")


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

# shipping step (Endereço)
MOBILE_BTN_CONTINUAR_SHIPPING = (By.CSS_SELECTOR, "#shipping-method-buttons-container button[data-role='opc-continue']")

# payment (Pagamento)
MOBILE_PIX = (By.ID, "dux_pay_pix")
MOBILE_TERMS_PIX = (By.ID, "terms_conditions_dux_pay_pix_agreement")

MOBILE_BTN_FINALIZAR_COMPRA = (By.XPATH, "(//button[contains(@class,'action primary checkout')])[1]")
