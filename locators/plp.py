from selenium.webdriver.common.by import By


#---------------------------------------------------------------
# Paginação
#---------------------------------------------------------------
def PAGE_NUMBER(n: str):
    return (By.XPATH, f"//div[contains(@class,'pages')]//span[normalize-space()='{n}']")

PAGINA_2 = (By.XPATH, "//div[@class='pages']//ul//span[normalize-space(text())='2']")
PAGES_UL = (By.XPATH, "//div[contains(@class,'pages')]//ul")

# Botão de paginação por número (genérico)
PAGINATION_BY_PAGE = lambda page_num: (By.XPATH, f"//div[@class='pages']//ul//span[normalize-space(text())='{page_num}']", )

# Botão "Próxima" (fallback caso você queira varrer sem depender de número fixo)
PAGINATION_NEXT = (By.CSS_SELECTOR, "a.action.next, .pages a.action.next")

#---------------------------------------------------------------
# Filtros
#---------------------------------------------------------------
FILTER_CONSERVACAO_OPEN = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[1]/span")
FILTER_CONSERVACAO_RESFRIADO = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]")
FILTER_CONSERVACAO_CONGELADO = (By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label")
FILTER_MARCA_OPEN = (By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[1]")
FILTER_MARCA_OPT1 = (By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[2]/div/ol/li[1]/a/label/span[1]")
FILTER_NACIONALIDADE = (By.XPATH, "//*[@id='narrow-by-list']/div[3]/div[1]/span")
FILTER_NACIONALIDADE_OPTION_1 = (By.XPATH, "//*[@id='narrow-by-list']/div[3]/div[2]/div/ol/li[1]/a/label/span[1]")
FILTER_CLEAR_ALL = (By.XPATH, "//div[@class='block-actions filter-actions']//*[normalize-space(text())='Limpar Tudo']")

#---------------------------------------------------------------
# Ordenação
#---------------------------------------------------------------
SORTER_SELECT = (By.ID, "sorter")
def SORT_OPTION(v: str):
    return (By.XPATH, f"//*[@id='sorter']/option[@value='{v}']")

SORT_LOW_TO_HIGH = (By.XPATH, "//*[@id='sorter']/option[@value='low_to_high']")
SORT_HIGH_TO_LOW = (By.XPATH, "//*[@id='sorter']/option[@value='high_to_low']")

#---------------------------------------------------------------
# Categorias
#---------------------------------------------------------------

# Categorias por função, passando somente o nome da categoria no arquivo de teste
# ======= (O nome da categoria deve estar do mesmo jeito que estiver no site) =======
def CATEGORY_MENU(name: str):
    return (By.XPATH, f"//*[@id='nav-menu-desktop']//span[normalize-space()='{name}']")


CATEGORY_PROMOCOES = (By.XPATH, "//*[@id='nav-menu-desktop']//span[contains(normalize-space(text()), 'Promo')]")
CATEGORY_PESCADOS = (By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Pescados']")
CATEGORY_CORDEIROS = (By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Cordeiros']")
CATEGORY_BOVINOS_PREMIUM = (By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space()='Bovinos Premium']")
CATEGORY_BOVINOS = (By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Bovinos']")

# Avise-me (PLP/PDP)
AVISE_DISABLED_ANY = (By.CSS_SELECTOR, "a[id^='button_disabled_']")
AVISE_ENABLED_ANY = (By.CSS_SELECTOR, "a[id^='button_enabled_']")

# Botões que exigem login
BTN_ENTRAR_LISTA = (By.XPATH, "//a[contains(@class,'loggin-btn') and .//span[normalize-space()='Entrar']]")

# Botões de ações (card)
BTN_INCREMENT_QTY = (By.XPATH, "(//div[@class='product actions product-item-actions']//button[contains(@class,'increment-qty')])[1]")
BTN_ADD_TO_CART = (By.XPATH, "(//button[contains(@class,'action tocart') and contains(@class,'primary')])[1]")

TOOLBAR_AMOUNT = (By.ID, "toolbar-amount")

PLP_LIMITER = (By.ID, "limiter")

# Image do produto
PLP_PRODUCT_IMAGE_WRAPPER_BY_INDEX = lambda idx: (By.XPATH, f"(//*[contains(@id,'product-item-info')]//span[@class='product-image-wrapper'])[{idx}]",)

# Botão do favorito
PLP_WISHLIST_BTN_BY_INDEX = lambda idx: (By.XPATH, f"(//button[contains(@id,'button_wishlist')])[{idx}]",)
