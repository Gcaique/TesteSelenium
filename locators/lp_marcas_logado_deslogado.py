from selenium.webdriver.common.by import By

# =========================
# HEADER
# =========================

SEARCH_INPUT = (By.ID, "minisearch-input-top-search")
SEARCH_BUTTON = (By.XPATH, "//button[@title='Buscar']")
LOGIN_MENU = (By.ID, "login-name")
LOGO = (By.XPATH, "//a[contains(@class,'hj-header-logo')]")
MINICART_ICON = (By.XPATH, "//a[contains(@class,'showcart')]")

# =========================
# QUERO SER CLIENTE
# =========================

BTN_QUERO_SER_CLIENTE = (
    By.XPATH,
    "//button[@id='modal-customer-open']//span[normalize-space()='Quero ser cliente']"
)

BTN_CLOSE_QUERO_SER_CLIENTE = (
    By.XPATH,
    "(//*[@class='modal-inner-wrap']//button[contains(@class,'action-close')])[2]"
)

BTN_CLOSE_MODAL_LOGIN = (
    By.XPATH,
    "//aside[contains(@class,'modal-popup')]//button[contains(@class,'action-close')]"
)

# =========================
# HOME - CARROSSEL MARCAS
# =========================

BRANDS_CAROUSEL_ITEM = lambda index: (
    By.XPATH,
    f"(//li[contains(@class,'brands-carousel-item')])[{index}]"
)

# =========================
# ANCORAS
# =========================

ANCHOR_LINK = lambda text: (
    By.XPATH,
    f"//nav[contains(@class,'anchors')]//span[normalize-space()='{text}']"
)

# =========================
# BOTÕES LP
# =========================

BTN_COMPRE_AGORA = (
    By.XPATH,
    "//a[contains(@class,'pagebuilder-button-primary')]"
)

BOTAO_ENTRAR = (
    By.XPATH,
    "//a[normalize-space()='Entrar']"
)

# =========================
# LOGIN MODAL
# =========================

USERNAME_INPUT = (By.ID, "username")
PASSWORD_INPUT = (By.NAME, "login[password]")
BTN_AVANCAR = (By.ID, "send2")

# =========================
# OUTRAS MARCAS
# =========================

CARD_ESTANCIA_92 = (
    By.XPATH,
    "//div[contains(@class,'_estancia-92')]//a"
)

# =========================
# CARROSSEIS ESTÂNCIA
# =========================

CARROSSEL_ANGUS = (By.ID, "angus")
CARROSSEL_NOVILHO = (By.ID, "novilho")
CARROSSEL_CORDEIRO = (By.ID, "cordeiro")

SLICK_NEXT_INSIDE = (
    By.XPATH,
    ".//button[contains(@class,'slick-next')]"
)

BTN_ENTRAR_DENTRO_CARROSSEL = (
    By.XPATH,
    ".//a[normalize-space()='Entrar']"
)
# Busca (muito usada em vários lugares)
SEARCH_INPUT = (By.ID, "minisearch-input-top-search")
SEE_ALL_LINK = (By.XPATH, "//a[@class='see-all-link']")
SEARCH_SUGGEST_ADD_2 = (By.XPATH, "(//div[@class='product-add-to-cart ']//button)[2]")
SEARCH_BUTTON = (By.XPATH, "//button[@title='Buscar']//span[normalize-space()='Buscar']")