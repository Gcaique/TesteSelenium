from selenium.webdriver.common.by import By

# header + dropdown
#LOGIN_NAME_CONTAINER = (By.ID, "login-name")
#LINK_MINHA_CONTA = (By.XPATH, "//*[@id='login-dropdown']//a[normalize-space()='Minha conta']")
#BTN_LOGOUT = (By.ID, "action-logout")

# side menu
NAV_MINHA_CONTA = (By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space()='Minha conta']")
NAV_MEUS_PEDIDOS = (By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space()='Meus pedidos']")
NAV_LISTA_FAVORITOS = (By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space()='Lista de favoritos']")
NAV_ENDERECOS = (By.XPATH, "//*[@id='block-collapsible-nav']//a[contains(normalize-space(),'Endere')]")
NAV_MEUS_PONTOS = (By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space()='Meus pontos']")
NAV_CADASTRO_REDES = (By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space()='Cadastro de redes']")
NAV_MEUS_CUPONS = (By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space()='Meus cupons']")
NAV_MINHAS_MISSOES = (By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space()= 'Minhas missões']")
NAV_INFO_CONTA = (By.XPATH, "//*[@id='block-collapsible-nav']//a[contains(normalize-space(),'Informa')]")

# MINHA CONTA endereços
BTN_MAIN_ADDRESS_DASHBOARD = (By.XPATH, "//*[@class='box-content']//button[contains(@class,'hj-account_dashboard_address-main_button')]")
BTN_ACCEPT_MODAL = (By.XPATH, "//*[@class='modal-inner-wrap']//button[contains(@class,'action-accept')]")
LINK_VER_TODOS_ENDERECOS = (By.XPATH, "//*[@class='block block-dashboard-addresses']//span[normalize-space()='Ver todos']")

# MINHA CONTA pedidos recentes
LINK_PEDIDOS_RECENTES = (By.XPATH, "//a[contains(@class,'hj-account-order_history')]/span")

# MEUS PEDIDOS (Pedidos)
GRID_ORDERS_READY = (By.XPATH, "//*[@class='order-pagination __items-per-page']//select")
FIRST_ORDER_DETAILS = (By.XPATH, "(//table[@id='my-orders-table']//a[@class='action view'])[1]")

# MEUS PEDIDOS (Pix copy)
BTN_COPY_PIX = (By.XPATH, "//*[@class='dux-pix-customer-area __action']//button")
BTN_COPY_PIX_COPIED = (By.XPATH, "//*[@class='dux-pix-customer-area __action']//button[contains(@class,'__copied')]")

# MEUS PEDIDOS (filtros pedidos)
SEL_PERIOD = (By.ID, "period")
OPT_PERIOD_7D = (By.XPATH, "//*[@id='period']/option[@value='last_seven_days']")
BTN_FILTER = (By.XPATH, "//*[@class='order-filter __item __actions']//button")
SEL_ORDER_STATUS = (By.ID, "order-status")
OPT_ORDER_STATUS_FATURADO = (By.XPATH, "//*[@id='order-status']/option[@value='Faturado']")
SEL_PAYMENT_STATUS = (By.ID, "payment-status")
OPT_PAYMENT_STATUS_AGUARDANDO = (By.XPATH, "//*[@id='payment-status']/option[@value='Aguardando Pagamento']")
BTN_FILTER_ACTIVE = (By.XPATH, "//*[@class='order-filter __item __actions filter-active-enabled']/button")
BTN_CLEAR_FILTER = (By.XPATH, "//*[@class='order-filter __item __actions filter-active-enabled']//a")

# ENDEREÇOS (definir como principal - tela endereços)
BTN_MAIN_ADDRESS_DEFAULT = (By.XPATH, "//*[@class='box-content']//button[contains(@class,'hj-account_default_address-main_button')]")
BTN_MAIN_ADDRESS_DEFAULT_2 = (By.XPATH, "(//*[@class='box-content']//button[contains(@class,'hj-account_default_address-main_button')])[2]")
SECOND_ADDRESS_BOX = (By.XPATH, "(//*[@class='addresses-container']//*[@class='box-content'])[2]")

# MEUS PONTOS
REWARD_ALL = (By.ID, "reward-all")
REWARD_EARNINGS = (By.ID, "reward-earnings")
REWARD_USED = (By.ID, "reward-used")
REWARD_EXPIRED = (By.ID, "reward-expired")
REWARD_CANCELED = (By.ID, "reward-canceled")

# RELATÓRIOS PONTOS
BTN_POINTS_REPORT = (By.XPATH, "//a[@class='report-action']")
POINTS_REPORT_FILTER = (By.XPATH, "//select[@class='rewardquests__filter__dropdown']")
POINTS_REPORT_FILTER_OPT2 = (By.XPATH, "(//select[@class='rewardquests__filter__dropdown']/option)[2]")
LINK_BACK_TO_MISSIONS = (By.XPATH, "//a[@class='rewardquests__go-to-missions__link']")
MISSIONS_READY = (By.XPATH, "//*[@class='rewardquests __see-rules hj-fidelity_see-rules']//span")

# CADASTRO DE REDES
GRID_ASSIGNED_READY = (By.XPATH, "//*[@id='assigned-grid']//button[normalize-space()='Agrupar outro CNPJ']")
TAB_AGRUPAR = (By.XPATH, "(//*[@class='steps']//li)[2]")
TAB_INFO = (By.XPATH, "(//*[@class='steps']//li)[3]")
TAB_REGRAS = (By.XPATH, "(//*[@class='steps']//li)[4]")

# MEUS CUPONS
COUPON_FIRST = (By.XPATH, "(//*[@class='coupon-info']//span[@class='coupon-name'])[1]")
COUPON_VER_MAIS_1 = (By.XPATH, "(//*[@class='coupon-info']//a[contains(@class,'hj-my_coupons-action')])[1]")
COUPON_COPY_1 = (By.XPATH, "(//*[@class='coupon-content']//span[@class='code-copy'])[1]")
TAB_UNAVAILABLE = (By.XPATH, "//li[contains(@class,'unavailable')]/a")

# INFORMAÇÕES DA CONTA (editar email/senha)
BTN_EDIT_EMAIL = (By.XPATH, "//label[@for='change-email']//span[normalize-space()='Editar']")
BTN_EDIT_PASSWORD = (By.XPATH, "//label[@for='change-password']//span[normalize-space()='Editar']")
CURRENT_EMAIL = (By.ID, "current-email")
CONFIRM_EMAIL = (By.ID, "email")
CURRENT_PASSWORD = (By.ID, "current-password")
NEW_PASSWORD = (By.ID, "password")
CONFIRM_NEW_PASSWORD = (By.ID, "password-confirmation")
BTN_SAVE_ACCOUNT_INFO = (By.XPATH, "//button[contains(@class,'action') and contains(@class,'save') and contains(@class,'hj-customer-action_save')]")
BTN_CANCEL_ACCOUNT = (By.XPATH, "//a[contains(@class,'action back') and contains(@class,'cancel')]")

ALERT_SUCCESS = (By.XPATH, "//*[@class='message-alert']/*[@class='message-success success message']")

#INFORMAÇÕES DA CONTA (Telefone principal / WhatsApp)
BTN_DEFINIR_COMO_PRINCIPAL = (By.XPATH, "(//button[normalize-space()='Definir como principal'])[1]")
BTN_MODAL_DEFINIR = (By.XPATH, "//button[contains(@class,'action-primary') and contains(@class,'action-accept')]")
ALERT_SUCCESS_PHONE = (By.XPATH, "//*[@class='message-success success message']")
WHATSAPP_SWITCH = (By.XPATH, "//*[@class='content sequence-1-1']//span[contains(@class,'slider')]")
BODY_AJAX_LOADING = (By.XPATH, "//body[contains(@class,'ajax-loading')]")