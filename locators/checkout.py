from selenium.webdriver.common.by import By

# Step SHIPPING
BTN_CONTINUAR_SHIPPING = (By.XPATH, "//*[@id='shipping-method-buttons-container']//button")
STEP_ENDERECO = (By.XPATH, "//ul[@class='opc-progress-bar']//li[@class='opc-progress-bar-item _complete']")
BTN_MAIN_ADRESS_SHIPPING = (By.XPATH, "//*[@class='shipping-address-item selected-item']//button[@class='btn-main-address']")

# CUPOM
INPUT_CUPOM = (By.ID, "discount-code")
BTN_APLICAR_CUPOM = (By.ID, "button-apply-coupon")
MENSAGEM_SUCESSO_CUPOM = (By.XPATH, "//*[@class='message message-success success']")
BTN_REMOVER_CUPOM = (By.ID, "remove-coupon")
RADIO_BTN_CUPOM = (By.ID, "coupon-automacao10")

# PIX
PIX = (By.XPATH, "//label[@for='dux_pay_pix']")
TERMS_PIX = (By.ID, "terms_conditions_dux_pay_pix_agreement")
BTN_FINALIZAR_COMPRA_PIX = (By.XPATH, "(//button[contains(@class,'action primary checkout')])[1]")
PARTIAL_BILLING_TRIGGER_PIX = (By.XPATH, "//*[@id='partial_billing_dux_pay_pix_div']//strong[@class='partial-billing-trigger']")
PIX_SUCESSO = (By.XPATH, "//span[@class='dux-pix-customer-area __counter-label']")
PIX_COPIAR = (By.XPATH, "//*[@class='dux-pay-pix __btn-pix']/button")

# RECEBIMENTO PARCIAL
PARTIAL_BILLING_ACCEPT = (By.XPATH, "//aside[contains(@class,'_show')]//input[contains(@class,'accept')]")
PARTIAL_BILLING_REJECT = (By.XPATH, "//aside[contains(@class,'_show')]//input[contains(@class,'reject')]")

# BOLETO
BOLETO = (By.XPATH, "//label[@for='checkmo']")
PARTIAL_BILLING_TRIGGER_BOLETO = (By.XPATH, "//*[@id='partial_billing_checkmo_div']//strong")
BOLETO_SELECT = (By.ID, "payment-conditions-checkmo")
BOLETO_OPTION_21 = (By.XPATH, "//*[@id='payment-conditions-checkmo']/option[@value='21']")
TERMS_BOLETO = (By.ID, "terms_conditions_checkmo_agreement")
BTN_FINALIZAR_COMPRA_BOLETO = (By.XPATH, "(//button[contains(@class,'action primary checkout')])[2]")

PAGINA_SUCESSO = (By.XPATH, "//body[contains(@class,'checkout-onepage-success')]")
BTN_IR_PARA_HOME = (By.XPATH, "//a[@class='action primary continue']")

# CARTÃO
CARTAO = (By.XPATH, "//label[@for='braspag_pagador_creditcard']")
TERMS_CARTAO = (By.ID, "terms_conditions_braspag_pagador_creditcard_agreement")
BTN_FINALIZAR_COMPRA_CARTAO = (By.XPATH, "(//button[contains(@class,'action primary checkout')])[3]")
ERRO_CARTAO = (By.XPATH, "//*[@data-ui-id='checkout-cart-validationmessages-message-error']")
INPUT_NOME_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_cc_owner']")
INPUT_NUMERO_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_cc_number']")
SELECT_MES_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_expiration']")
OPTION_MES_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_expiration']/option[@value='1']")
SELECT_ANO_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_expiration_yr']")
OPTION_ANO_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_expiration_yr']/option[@value='2027']")
INPUT_CVV_CARTAO = (By.XPATH, "//*[@id='braspag_pagador_creditcard_cc_cid']")



# ENDEREÇO
BTN_ALTERAR_ENDERECO = (By.XPATH, "//*[@class='choose-address']/a")
BTN_MAIN_ADDRESS = lambda idx: (By.XPATH, f"(//*[@id='main-address'])[{idx}]")
BTN_ACCEPT_MODAL = (By.XPATH, "//button[@class='action action-primary action-accept']")
BTN_VOLTAR = (By.XPATH, "//*[@class='go-back-address']//a")
BTN_SELECIONAR_ENDERECO = lambda idx: (By.XPATH, f"(//*[@class='shipping-address-item not-selected-item']//*[@class='btn-select-address'])[{idx}]")


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

# shipping step (Endereço)
MOBILE_BTN_CONTINUAR_SHIPPING = (By.CSS_SELECTOR, "#shipping-method-buttons-container button[data-role='opc-continue']")

# payment (Pagamento)
MOBILE_PIX_INPUT = (By.ID, "dux_pay_pix")
MOBILE_PIX_LABEL = (By.CSS_SELECTOR, "label[for='dux_pay_pix']") # clique robusto: clicar no label do PIX
MOBILE_PIX_TEXT = (By.XPATH, "//*[self::label or self::span][normalize-space()='Pix']/ancestor::label[1]") # fallback: clicar no texto Pix (caso mude o for/id)
MOBILE_TERMS_PIX = (By.ID, "terms_conditions_dux_pay_pix_agreement") # Termos

MOBILE_BTN_FINALIZAR_COMPRA_PIX = (By.XPATH, "(//button[contains(@class,'action primary checkout')])[1]")

# cupom
MOBILE_APLICAR_CUPOM = (By.XPATH, "//*[@class='action showcart']")
MOBILE_MODAL_APLICAR_CUPOM = (By.XPATH, "//*[@class='modal-custom opc-sidebar opc-summary-wrapper custom-slide _show']")
MOBILE_BTN_CLOSE_MODAL_CUPOM = (By.XPATH, "//*[@class='modal-custom opc-sidebar opc-summary-wrapper custom-slide _show']//*[@class='action-close']")

# resumo do pedido
MOBILE_OPEN_SUMARY = (By.XPATH, "//*[@class='summary-floating __expand __not-expanded']//img")
MOBILE_CLOSE_SUMARY = (By.XPATH, "//*[@class='summary-floating __expand']//img")