from selenium.webdriver.common.by import By

# shipping step (Endereço)
BTN_CONTINUAR_SHIPPING = (By.XPATH, "//*[@id='shipping-method-buttons-container']//button")

# payment (Pagamento)
PIX = (By.XPATH, "//label[@for='dux_pay_pix']")
TERMS_PIX = (By.ID, "terms_conditions_dux_pay_pix_agreement")

BTN_FINALIZAR_COMPRA = (By.XPATH, "(//button[contains(@class,'action primary checkout')]//span[normalize-space()='Finalizar compra'])[1]")
