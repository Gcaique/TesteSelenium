from selenium.webdriver.common.by import By

# ── Login ──────────────────────────────────────────────────────────
FACA_SEU_LOGIN = (By.XPATH, "//div[@id='login-name']/span")
INPUT_EMAIL = (By.XPATH, "//input[@id='username']")
BTN_AVANCAR = (By.XPATH, "//button[@id='send2']")
INPUT_SENHA = (By.XPATH, "//*[@name='login[password]']")

# ── Roleta de cupons ──────────────────────────────────────────────
SPIN_CLOSE_BTN = (
    By.XPATH,
    "//button[@class='action-close hj-spintowin-close_button']",
)

# ── Mapa de corte (home section) ─────────────────────────────────
MAPA_CORTE_SECTION = (By.XPATH, "//*[@class='cutting-map __home-section']")
MAPA_CORTE_LOADED = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-2 hj-cutting-map_cut-area-2-bovine']",
)

# ── Bovine images ─────────────────────────────────────────────────
BOVINE_IMG_2 = (By.XPATH, "//*[@id='smoking-cut-area-2-bovine']")
BOVINE_IMG_9 = (By.XPATH, "//*[@id='smoking-cut-area-9-bovine']")
BOVINE_IMG_11 = (By.XPATH, "//*[@id='smoking-cut-area-11-bovine']")
BOVINE_IMG_20 = (By.XPATH, "//*[@id='smoking-cut-area-20-bovine']")
BOVINE_IMG_21 = (By.XPATH, "//*[@id='smoking-cut-area-21-bovine']")
BOVINE_IMG_4 = (By.XPATH, "//*[@id='smoking-cut-area-4-bovine']")
BOVINE_IMG_14 = (By.XPATH, "//*[@id='smoking-cut-area-14-bovine']")

# ── Bovine wait-after-close confirmations ─────────────────────────
BOVINE_AREA_2 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-2 hj-cutting-map_cut-area-2-bovine']",
)
BOVINE_AREA_9 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-9 hj-cutting-map_cut-area-9-bovine']",
)
BOVINE_AREA_11 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-11 hj-cutting-map_cut-area-11-bovine']",
)
BOVINE_AREA_20 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-20 hj-cutting-map_cut-area-20-bovine']",
)
BOVINE_AREA_4 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-4 hj-cutting-map_cut-area-4-bovine']",
)
BOVINE_AREA_14 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-14 hj-cutting-map_cut-area-14-bovine']",
)
BOVINE_AREA_5 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-5 hj-cutting-map_cut-area-5-bovine']",
)
BOVINE_AREA_3 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-3 hj-cutting-map_cut-area-3-bovine']",
)
BOVINE_AREA_13 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-13 hj-cutting-map_cut-area-13-bovine']",
)

# ── Bovine list items ─────────────────────────────────────────────
BOVINE_ITEM_03 = (
    By.XPATH,
    "//li[@id='smoking-item-bovine-id-03']/span[@class='cutting-map __name']",
)
BOVINE_ITEM_05 = (
    By.XPATH,
    "//li[@id='smoking-item-bovine-id-05']/span[@class='cutting-map __name']",
)
BOVINE_ITEM_13 = (
    By.XPATH,
    "//li[@id='smoking-item-bovine-id-13']/span[@class='cutting-map __name']",
)
BOVINE_ITEM_20 = (
    By.XPATH,
    "//li[@id='smoking-item-bovine-id-20']/span[@class='cutting-map __name']",
)

# ── Modal ─────────────────────────────────────────────────────────
MODAL_CLOSE = (By.XPATH, "//button[@id='smoke-cutting-map_modal-close']")
MODAL_NEXT = (
    By.XPATH,
    "//*[@class='cutting-map __modal __next hj-cutting-map_pagination-next']",
)
MODAL_PREV = (
    By.XPATH,
    "//*[@class='cutting-map __modal __prev hj-cutting-map_pagination-prev']",
)
MODAL_VER_PRODUTOS = (By.XPATH, "//a[@id='smoke-cutting-map_modal-lnk']")

# ── Carrossel de marcas (modal) ───────────────────────────────────
CAROUSEL_BTN_2 = (By.XPATH, "(//ul[@id='carousel-brands']//button)[2]")
CAROUSEL_BTN_3 = (By.XPATH, "(//ul[@id='carousel-brands']//button)[3]")
CAROUSEL_BTN_4 = (By.XPATH, "(//ul[@id='carousel-brands']//button)[4]")
CAROUSEL_MARCA_PUL = (
    By.XPATH,
    "(//*[@class='slick-slide slick-active']//a[@id='smoke-cutting-map-modal-brands-lnk'])[2]",
)
CAROUSEL_FIRST_BRAND = (
    By.XPATH,
    "//a[@id='smoke-cutting-map-modal-brands-lnk']",
)
CAROUSEL_FIRST_BRAND_ACTIVE = (
    By.XPATH,
    "//*[@class='slick-slide slick-current slick-active']//a[@id='smoke-cutting-map-modal-brands-lnk']",
)

# ── Logo header ───────────────────────────────────────────────────
LOGO_HEADER = (By.XPATH, "//a[@class='logo hj-header-logo']")

# ── Aba Cordeiro ──────────────────────────────────────────────────
ABA_CORDEIRO = (By.XPATH, "//*[@id='lamb-map']")
ABA_CORDEIRO_ACTIVE = (
    By.XPATH,
    "//*[@class='cutting-map __tab-item hj-cutting-map_tab-item-lamb __active hj-cutting-map_tab-item-lamb-active']",
)

# ── Lamb images ───────────────────────────────────────────────────
LAMB_IMG_1 = (By.XPATH, "//*[@id='smoking-cut-area-1-lamb']")
LAMB_IMG_2 = (By.XPATH, "//*[@id='smoking-cut-area-2-lamb']")
LAMB_IMG_4 = (By.XPATH, "//*[@id='smoking-cut-area-4-lamb']")
LAMB_IMG_8 = (By.XPATH, "//*[@id='smoking-cut-area-8-lamb']")
LAMB_IMG_9 = (By.XPATH, "//*[@id='smoking-cut-area-9-lamb']")

# ── Lamb wait-after-close confirmations ───────────────────────────
LAMB_AREA_2 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-2 hj-cutting-map_cut-area-2-lamb']",
)
LAMB_AREA_3 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-3 hj-cutting-map_cut-area-3-lamb']",
)
LAMB_AREA_4 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-4 hj-cutting-map_cut-area-4-lamb']",
)
LAMB_AREA_8 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-8 hj-cutting-map_cut-area-8-lamb']",
)
LAMB_AREA_9 = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-9 hj-cutting-map_cut-area-9-lamb']",
)
# CSV 186: __area-8 (parece um typo no CSV, mas respeitando o original)
LAMB_AREA_6_CSV = (
    By.XPATH,
    "//*[@class='cutting-map __cut-area __area-8 hj-cutting-map_cut-area-6-lamb']",
)

# ── Lamb list items ───────────────────────────────────────────────
LAMB_ITEM_02 = (
    By.XPATH,
    "//li[@id='smoking-item-lamb-id-02']/span[@class='cutting-map __name']",
)
LAMB_ITEM_03 = (
    By.XPATH,
    "//li[@id='smoking-item-lamb-id-03']/span[@class='cutting-map __name']",
)
LAMB_ITEM_06 = (
    By.XPATH,
    "//li[@id='smoking-item-lamb-id-06']/span[@class='cutting-map __name']",
)
LAMB_ITEM_08 = (
    By.XPATH,
    "//li[@id='smoking-item-lamb-id-08']/span[@class='cutting-map __name']",
)
LAMB_ITEM_09 = (
    By.XPATH,
    "//li[@id='smoking-item-lamb-id-09']/span[@class='cutting-map __name']",
)

# ── Logout ────────────────────────────────────────────────────────
MENU_USUARIO = (By.XPATH, "//*[@id='login-name']")
BTN_SAIR = (By.XPATH, "//*[@id='action-logout']")

# ── Footer ────────────────────────────────────────────────────────
FOOTER_CONTENT = (By.XPATH, "//*[@class='footer-content']")
FOOTER_MAPA_CORTE = (
    By.XPATH,
    "//a[normalize-space(text())='Mapa de Corte']",
)

# ── Pagina de categoria (scroll) ─────────────────────────────────
PRODUCT_ITEM_5 = (By.XPATH, "(//li[@class='item product product-item '])[5]")
PRODUCT_ITEM_9 = (By.XPATH, "(//li[@class='item product product-item '])[9]")
