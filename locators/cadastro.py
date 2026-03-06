from selenium.webdriver.common.by import By

# =====================================================
# STEP CNPJ
# =====================================================

INPUT_CNPJ = (By.ID, "modal-taxvat")
BTN_INICIAR_CADASTRO = (By.XPATH, "//button[normalize-space()='Iniciar cadastro']")

# =====================================================
# STEP DADOS GERAIS
# =====================================================

INPUT_PASSWORD = (By.ID, "password")
INPUT_PASSWORD_CONFIRM = (By.ID, "password-confirmation")

BTN_CONTINUAR = (By.ID, "reset-pwd")

INPUT_BUSINESS_NAME = (By.ID, "business_name")
INPUT_NOME_CONTATO = (By.ID, "nome_contato")
INPUT_EMAIL = (By.ID, "email_address")
INPUT_CELULAR = (By.ID, "celular")
INPUT_TELEFONE = (By.ID, "telefone")

SWITCH_CELULAR_PRINCIPAL = (By.XPATH, "//input[@id='celular_principal']/parent::label")

SWITCH_CELULAR_WHATSAPP = (By.XPATH, "//input[@id='celular_is_wpp']/parent::label")

SELECT_TIPOLOGIA = (By.ID, "tipologia")

# =====================================================
# STEP VALIDAÇÃO (TOKEN)
# =====================================================

INPUT_TOKEN_SMS = (By.ID, "sms_validation")

MSG_TOKEN_INVALIDO = (By.XPATH, "//span[contains(normalize-space(),'Token')]")

# =====================================================
# STEP REVISÃO
# =====================================================

CHECKBOX_TERMOS = (By.ID, "terms_accepted")

BTN_CRIAR_CONTA = (By.XPATH, "//button[normalize-space()='Criar Conta']")

# =====================================================
# SUCESSO
# =====================================================

MODAL_SUCESSO = (By.ID, "modal-register-success")

BTN_IR_HOME = (By.XPATH, "//div[@id='modal-register-success']//button")