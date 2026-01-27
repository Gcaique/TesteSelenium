from selenium.webdriver.common.by import By

# Dropdown do usuário (links)
DD_MINHA_CONTA = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Minha conta']")
DD_COMPARAR = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Comparar produtos']")
DD_MEUS_PEDIDOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pedidos']")
DD_FAVORITOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Lista de favoritos']")
DD_MEUS_PONTOS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pontos']")
DD_MEUS_CUPONS = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus cupons']")
DD_MINHAS_MISSOES = (By.XPATH, "//*[@id='login-dropdown']//a[contains(normalize-space(text()), 'Minhas miss')]")

# Login (modal no header)
LOGIN_MENU = (By.XPATH, "//div[@id='login-name']/span")
LOGIN_NAME_CONTAINER = (By.ID, "login-name")  # área do usuário (logado)
USERNAME_INPUT = (By.ID, "username")
PASSWORD_INPUT = (By.XPATH, "//*[@name='login[password]']")
BTN_AVANCAR = (By.ID, "send2")

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
LOGIN_NAME_SPAN = (By.XPATH, "//div[@id='login-name']/span")

# LOGO
LOGO = (By.XPATH, "//a[contains(@class,'hj-header-logo')]")




