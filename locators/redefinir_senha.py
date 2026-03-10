from selenium.webdriver.common.by import By


# Modal esqueci minha senha
BTN_SMS_MODAL = (By.XPATH,"//button[@class='option-button option-sms hj-fgt-pwd-modal_reset-sms-option']",)
BTN_EMAIL_MODAL = (By.XPATH, "//button[@class='option-button option-email hj-fgt-pwd-modal_reset-email-option']")
BTN_AVANCAR_MODAL = (By.XPATH, "//button[@class='action primary next hj-fgt-pwd-modal_validation-next-action']")
BTN_VOLTAR_MODAL = (By.XPATH, "//button[@class='action secondary back hj-fgt-pwd-modal_validation-back-action']")
MSG_ALERTA_MODAL = (By.XPATH, "//*[@class='warning-message warning message']")
INPUT_EMAIL_OPTION_0 = (By.XPATH, "//input[@id='email-option-0']")

# Modal verifique
BTN_RECEBI_LINK = (By.XPATH, "//button[@class='action primary hj-fgt-pwd-modal_verify-received-link']")

# Admin - login
ADMIN_INPUT_USERNAME = (By.XPATH, "//*[@id='username']")
ADMIN_INPUT_PASSWORD = (By.XPATH, "//*[@id='login']")
ADMIN_BTN_ENTRAR = (By.XPATH, "//button[@class='action-login action-primary']/span")
ADMIN_BTN_FECHAR_MODAL = (By.XPATH, "(//header[@class='modal-header']//button[@class='action-close'])[1]")

# Admin - navegação
ADMIN_MENU_STORES = (By.XPATH, "//*[@id='menu-magento-backend-stores']/a")
ADMIN_SUBMENU_EMAIL_LOGS = (By.XPATH, "//*[@id='menu-magento-backend-stores']/div/ul/li[3]/ul/li[1]/div/ul/li[1]/a")

# Admin - email logs
ADMIN_BTN_FILTERS = (By.XPATH, "(//div[@class='data-grid-filters-actions-wrap']//button)[1]")
ADMIN_INPUT_RECIPIENT = (By.XPATH, "//*[@class='admin__form-field-control']/input[@name='recipient']")
ADMIN_BTN_APPLY_FILTERS = (By.XPATH, "//*[@class='admin__footer-main-actions']//button[@class='action-secondary']")
ADMIN_BTN_SELECT_FIRST = (By.XPATH, "(//*[@class='admin__data-grid-wrap']//button[@class='action-select'])[1]")
ADMIN_BTN_VIEW = (By.XPATH, "//*[@class='action-select-wrap _active']//a[normalize-space(text())='View']")

# Admin - template email (iframe)
ADMIN_IFRAME_EMAIL = (By.XPATH, "//*[@id='modal-content-11']/div/iframe")
ADMIN_LINK_EMAIL_BODY = (By.XPATH, "//*[@class='main-content']//a")

# Pagina criar nova senha
INPUT_NOVA_SENHA = (By.XPATH, "//*[@class='field password required']//input[@id='password']")
INPUT_CONFIRMAR_SENHA = (By.XPATH, "//*[@class='field confirmation required']//input[@id='password-confirmation']")
BTN_MOSTRAR_NOVA_SENHA = (By.XPATH, "//*[@class='field password required']//span[@class='show_password']")
BTN_MOSTRAR_CONFIRMAR_SENHA = (By.XPATH, "//*[@class='field confirmation required']//span[@class='show_password']")
BTN_REDEFINIR_SENHA = (By.XPATH, "//*[@class='actions-toolbar']//button[@id='reset-pwd']")

# Modal sucesso redefinicao
BTN_ENTRAR_APOS_REDEFINIR = (By.XPATH, "//a[@class='modal-reset-pswd-success __action']")
