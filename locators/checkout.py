from selenium.webdriver.common.by import By

# ================= SHIPPING =================

BTN_CONTINUAR_SHIPPING = (
    By.XPATH,
    "//*[@id='shipping-method-buttons-container']//button"
)

CHECKOUT_LOADING = (
    By.XPATH,
    "//body[contains(@class,'ajax-loading')]"
)

# ================= CUPOM =================

CUPOM_INPUT = (By.ID, "discount-code")
CUPOM_APLICAR = (By.ID, "button-apply-coupon")
CUPOM_SUCESSO = (By.XPATH, "//*[@class='message message-success success']")
CUPOM_REMOVER = (By.ID, "remove-coupon")

# ================= PIX =================

PIX = (By.XPATH, "//label[@for='dux_pay_pix']")
TERMS_PIX = (By.ID, "terms_conditions_dux_pay_pix_agreement")

BTN_FINALIZAR_COMPRA_PIX = (
    By.XPATH,
    "(//button[contains(@class,'action primary checkout')])[1]"
)

PIX_SUCESSO = (
    By.XPATH,
    "//span[@class='dux-pix-customer-area __counter-label']"
)

PIX_COPIAR = (
    By.XPATH,
    "//*[@class='dux-pay-pix __btn-pix']/button"
)

# ================= BOLETO =================

BOLETO_LABEL = (By.XPATH, "//label[@for='checkmo']")

PARTIAL_BILLING_TRIGGER = (
    By.XPATH,
    "//*[@id='partial_billing_checkmo_div']//strong"
)

PARTIAL_BILLING_ACCEPT = (
    By.XPATH,
    "//aside[contains(@class,'_show')]//input[contains(@class,'accept')]"
)

BOLETO_SELECT = (By.ID, "payment-conditions-checkmo")

BOLETO_OPTION_21 = (
    By.XPATH,
    "//*[@id='payment-conditions-checkmo']/option[@value='21']"
)

TERMS_BOLETO = (By.ID, "terms_conditions_checkmo_agreement")

BTN_FINALIZAR_COMPRA_BOLETO = (
    By.XPATH,
    "(//button[contains(@class,'action primary checkout')])[2]"
)

PAGINA_SUCESSO = (
    By.XPATH,
    "//body[contains(@class,'checkout-onepage-success')]"
)

# ================= CARTÃO =================

CARTAO = (
    By.XPATH,
    "//label[@for='braspag_pagador_creditcard']"
)

TERMS_CARTAO = (
    By.ID,
    "terms_conditions_braspag_pagador_creditcard_agreement"
)

BTN_FINALIZAR_COMPRA_CARTAO = (
    By.XPATH,
    "(//button[contains(@class,'action primary checkout')])[3]"
)

ERRO_CARTAO = (
    By.XPATH,
    "//*[@data-ui-id='checkout-cart-validationmessages-message-error']"
)
# ================= ENDEREÇO =================

ALTERAR_ENDERECO = (
    By.XPATH,
    "//button[contains(@class,'action-edit-address')]"
)

SALVAR_ENDERECO = (
    By.XPATH,
    "//button[contains(@class,'action-save-address')]"
)


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
