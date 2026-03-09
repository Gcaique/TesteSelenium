from selenium.webdriver.common.by import By


# Modal de cadastro
INPUT_CNPJ = (By.ID, "modal-taxvat")
BTN_INICIAR_CADASTRO = (By.XPATH, "//button[normalize-space()='Iniciar cadastro']")

# Step Dados Gerais
INPUT_PASSWORD = (By.ID, "password")
INPUT_PASSWORD_CONFIRM = (By.ID, "password-confirmation")
INPUT_BUSINESS_NAME = (By.ID, "business_name")
INPUT_NOME_CONTATO = (By.ID, "nome_contato")
INPUT_EMAIL = (By.ID, "email_address")
INPUT_CELULAR = (By.ID, "celular")
INPUT_TELEFONE = (By.ID, "telefone")
SWITCH_CELULAR_PRINCIPAL = (By.XPATH, "//input[@id='celular_principal']/parent::label")
SWITCH_CELULAR_WHATSAPP = (By.XPATH, "//input[@id='celular_is_wpp']/parent::label")
SELECT_TIPOLOGIA = (By.ID, "tipologia")

# Step Validação (TOKEN)
INPUT_TOKEN_SMS = (By.ID, "sms_validation")
MSG_TOKEN_INVALIDO = (By.XPATH, "//span[contains(normalize-space(),'Token')]")

# Step Revisão
CHECKBOX_TERMOS = (By.ID, "terms_accepted")
BTN_CRIAR_CONTA = (By.XPATH, "//button[normalize-space()='Criar Conta']")

# Botão Continuar. "Serve para todos os steps"
BTN_CONTINUAR = (By.ID, "reset-pwd")

# Modal de Sucesso
MODAL_SUCESSO = (By.ID, "modal-register-success")
BTN_COPIAR_EMAIL = By.XPATH, ("(//p[@class='_contact_email _contact']/span)[1]")
BTN_IR_HOME = (By.XPATH, "//div[@id='modal-register-success']//button")