from selenium.webdriver.common.by import By

# ========================================
# COOKIE BANNER
# ========================================
BTN_ACEITAR_COOKIES = (By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")

# ========================================
# MODAL DE REGIAO
# ========================================
BTN_OUTRAS_REGIOES = (By.XPATH, "//button[@id='other-regions']")

# ========================================
# HEADER
# ========================================
BTN_LOGIN_HEADER = (By.XPATH, "//div[@id='login-name']/span")
BTN_LOGOUT_HEADER = (By.XPATH, "//a[contains(@href,'logout')]")

# ========================================
# LOGIN PAGE
# ========================================
INPUT_USERNAME = (By.XPATH, "//input[@id='username']")
INPUT_PASSWORD = (By.XPATH, "//*[@name='login[password]']")
BTN_AVANCAR_LOGIN = (By.XPATH, "//button[@id='send2']")
LINK_ESQUECI_SENHA = (By.XPATH, "//a[@class='action remind hj-fgt-pwd-modal_opener-action']")
MSG_ERRO_SENHA = (
    By.XPATH,
    "//*[@class='message-error error message']//*[contains(normalize-space(text()),'A senha digitada')]",
)
BTN_MOSTRAR_SENHA = (By.XPATH, "//*[contains(@data-bind,'showPassword')]/label")

# ========================================
# MODAL ESQUECI MINHA SENHA
# ========================================
BTN_SMS_MODAL = (
    By.XPATH,
    "//button[@class='option-button option-sms hj-fgt-pwd-modal_reset-sms-option']",
)
BTN_EMAIL_MODAL = (
    By.XPATH,
    "//button[@class='option-button option-email hj-fgt-pwd-modal_reset-email-option']",
)
BTN_AVANCAR_MODAL = (
    By.XPATH,
    "//button[@class='action primary next hj-fgt-pwd-modal_validation-next-action']",
)
BTN_VOLTAR_MODAL = (
    By.XPATH,
    "//button[@class='action secondary back hj-fgt-pwd-modal_validation-back-action']",
)
MSG_ALERTA_MODAL = (By.XPATH, "//*[@class='warning-message warning message']")
INPUT_EMAIL_OPTION_0 = (By.XPATH, "//input[@id='email-option-0']")

# ========================================
# MODAL VERIFIQUE
# ========================================
BTN_RECEBI_LINK = (
    By.XPATH,
    "//button[@class='action primary hj-fgt-pwd-modal_verify-received-link']",
)

# ========================================
# ADMIN - LOGIN
# ========================================
ADMIN_INPUT_USERNAME = (By.XPATH, "//*[@id='username']")
ADMIN_INPUT_PASSWORD = (By.XPATH, "//*[@id='login']")
ADMIN_BTN_ENTRAR = (By.XPATH, "//button[@class='action-login action-primary']/span")
ADMIN_BTN_FECHAR_MODAL = (
    By.XPATH,
    "(//header[@class='modal-header']//button[@class='action-close'])[1]",
)

# ========================================
# ADMIN - NAVEGACAO
# ========================================
ADMIN_MENU_STORES = (By.XPATH, "//*[@id='menu-magento-backend-stores']")
ADMIN_SUBMENU_EMAIL_LOGS = (
    By.XPATH,
    "//*[@id='menu-magento-backend-stores']/div/ul/li[3]/ul/li[1]/div/ul/li[1]/a",
)

# ========================================
# ADMIN - EMAIL LOGS
# ========================================
ADMIN_BTN_FILTERS = (By.XPATH, "(//div[@class='data-grid-filters-actions-wrap']//button)[1]")
ADMIN_INPUT_RECIPIENT = (
    By.XPATH,
    "//*[@class='admin__form-field-control']/input[@name='recipient']",
)
ADMIN_BTN_APPLY_FILTERS = (
    By.XPATH,
    "//*[@class='admin__footer-main-actions']//button[@class='action-secondary']",
)
ADMIN_BTN_SELECT_FIRST = (
    By.XPATH,
    "(//*[@class='admin__data-grid-wrap']//button[@class='action-select'])[1]",
)
ADMIN_BTN_VIEW = (
    By.XPATH,
    "//*[@class='action-select-wrap _active']//a[normalize-space(text())='View']",
)

# ========================================
# ADMIN - TEMPLATE EMAIL (IFRAME)
# ========================================
ADMIN_IFRAME_EMAIL = (By.XPATH, "//*[@id='modal-content-11']/div/iframe")
ADMIN_LINK_EMAIL_BODY = (By.XPATH, "//*[@class='main-content']//a")

# ========================================
# PAGINA CRIAR NOVA SENHA
# ========================================
INPUT_NOVA_SENHA = (
    By.XPATH,
    "//*[@class='field password required']//input[@id='password']",
)
INPUT_CONFIRMAR_SENHA = (
    By.XPATH,
    "//*[@class='field confirmation required']//input[@id='password-confirmation']",
)
BTN_MOSTRAR_NOVA_SENHA = (
    By.XPATH,
    "//*[@class='field password required']//span[@class='show_password']",
)
BTN_MOSTRAR_CONFIRMAR_SENHA = (
    By.XPATH,
    "//*[@class='field confirmation required']//span[@class='show_password']",
)
BTN_REDEFINIR_SENHA = (By.XPATH, "//*[@class='actions-toolbar']//button[@id='reset-pwd']")

# ========================================
# MODAL SUCESSO REDEFINICAO
# ========================================
BTN_ENTRAR_APOS_REDEFINIR = (By.XPATH, "//a[@class='modal-reset-pswd-success __action']")
