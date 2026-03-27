from selenium.webdriver.common.by import By

# Dropdown do usuário (links)
DD_MINHA_CONTA = (By.XPATH, "//*[@id='login-dropdown']//*[normalize-space(text())='Minha conta']")
DD_COMPARAR = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Comparar produtos']")
DD_MEUS_PEDIDOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pedidos']")
DD_FAVORITOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Lista de favoritos']")
DD_MEUS_PONTOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pontos']")
DD_MEUS_CUPONS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus cupons']")
DD_MINHAS_MISSOES = (By.XPATH, "//*[@id='login-dropdown']//a[contains(normalize-space(text()), 'Minhas miss')]")

# Login (modal no header)
LOGIN_NAME_CONTAINER = (By.ID, "login-name")  # área do usuário (logado)
USERNAME_INPUT = (By.ID, "username")  # input e-mail/cnpj/cpf
PASSWORD_INPUT = (By.XPATH, "//*[@name='login[password]']")  # input senha
BTN_AVANCAR = (By.ID, "send2")  # botão "Avançar"
LINK_ESQUECI_SENHA = (By.XPATH, "//a[@class='action remind hj-fgt-pwd-modal_opener-action']")
BTN_MOSTRAR_SENHA = (By.XPATH, "//*[contains(@data-bind,'showPassword')]/label")

#ALERTAS
ERROR_EMAIL_NOT_FOUND = (By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(),'Verifique o dado informado')]")
ERROR_WRONG_PASSWORD = (By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(),'A senha digitada')]")

# Logout
BTN_LOGOUT = (By.ID, "action-logout")

# Busca (muito usada em vários lugares)
SEARCH_INPUT = (By.ID, "minisearch-input-top-search")
SEE_ALL_LINK = (By.XPATH, "//a[@class='see-all-link']")
SEARCH_SUGGEST_ADD_2 = (By.XPATH, "(//div[@class='product-add-to-cart ']//button)[2]")
SEARCH_BUTTON = (By.XPATH, "//button[@title='Buscar']//span[normalize-space()='Buscar']")

# Header deslogado
BTN_TERMS = (By.ID, "login-terms")
BTN_CLOSE_MODAL = (By.XPATH, "//button[@class='close-modal']")
BTN_QUERO_SER_CLIENTE = (By.XPATH, "//button[@id='modal-customer-open']//span[normalize-space()='Quero ser cliente']")
BTN_CLOSE_QUERO_SER_CLIENTE = (By.XPATH, "(//*[@class='modal-inner-wrap']//button[contains(@class,'action-close')])[2]")
LOGIN_MENU = (By.XPATH, "//div[@id='login-name']/span") # "Faça seu login"
ERROR_LOGIN_MESSAGE = (By.XPATH, "//*[@class='message-error error message']")

# LOGO
LOGO = (By.XPATH, "//a[contains(@class,'hj-header-logo')]")


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

# LOGIN DROPDOWN
MOBILE_LOGIN_NAME = (By.XPATH, "//div[@id='login-name']//span[contains(@class,'login-name')]")
MOBILE_LOGIN_ACESSO = (By.ID, "login-form-opener") # “Acesso”
MOBILE_QUERO_SER_CLIENTE = (By.ID, "first-acess-register-modal-opener") # “Quero ser cliente”
MOBILE_LOGIN_DROPDOWN_OPENED = (By.XPATH, "//*[@class='customer-dropdown login-name active']") # Dropdown do Faça seu login aberto

# Busca
MOBILE_SEARCH_BUTTON = (By.XPATH, "//button[@title='Buscar']")
MOBILE_SEARCH_SUGGEST_ADD_1 = (By.XPATH, "(//div[@class='product-add-to-cart ']//button)[1]")

# Dropdown do usuário (links)
MOBILE_DD_MINHA_CONTA = (By.CSS_SELECTOR, "#login-dropdown a[href*='customer/account']")
MOBILE_DD_COMPARAR = (By.CSS_SELECTOR, "#login-dropdown a[href*='product_compare']")
MOBILE_DD_MEUS_PEDIDOS = (By.CSS_SELECTOR, "#login-dropdown a[href*='sales/order/history']")
MOBILE_DD_FAVORITOS = (By.XPATH, "//div[@id='login-dropdown']//a[normalize-space(.)='Lista de favoritos' and not(contains(@style,'display:none'))]")
MOBILE_DD_MEUS_PONTOS = (By.CSS_SELECTOR, "#login-dropdown a[href*='reward']")
MOBILE_DD_MEUS_CUPONS = (By.XPATH, "//div[@id='login-dropdown']//a[normalize-space(.)='Meus cupons']")
MOBILE_DD_MINHAS_MISSOES = (By.CSS_SELECTOR, "#login-dropdown a[href*='mission']")
MOBILE_DD_SAIR = (By.CSS_SELECTOR, "#login-dropdown a[href*='logout']")