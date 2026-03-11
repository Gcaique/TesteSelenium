from selenium.webdriver.common.by import By

# Ancoras
ANCHOR_LINK = lambda text: (By.XPATH, f"//nav[contains(@class,'anchors')]//span[normalize-space()='{text}']")

# Botões LPs
BTN_COMPRE_AGORA = (By.XPATH, "//a[contains(@class,'pagebuilder-button-primary')]")
BTN_ENTRAR = (By.XPATH, "//*[@id='produto']//a[normalize-space()='Entrar']")
BTN_ADICIONAR_ALMA_LUSA = (By.XPATH, '//*[@id="produto"]//form/button')

# Outras marcas
CARD_ESTANCIA_92 = (By.XPATH, "//div[contains(@class,'_estancia-92')]//a")

# Carrosseis Estância
CARROSSEL_ANGUS = (By.ID, "angus")
CARROSSEL_NOVILHO = (By.ID, "novilho")
CARROSSEL_CORDEIRO = (By.ID, "cordeiro")

SLICK_NEXT_INSIDE = (By.XPATH,".//button[contains(@class,'slick-next')]")

BTN_ENTRAR_DENTRO_CARROSSEL = (By.XPATH, ".//a[normalize-space()='Entrar']")


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

# Lp Alma Lusa
MOBILE_BTN_CONHECA_MAIS = (By.XPATH, "//*[@id='intro']//a")
MOBILE_DOTS_CARROSSEL = lambda idx: (By.XPATH, f"(//ul[@class='slick-dots']//button)[{idx}]")
MOBILE_BTN_COMPRE_AGORA_2 = (By.XPATH, "//*[@id='diferenciais']//a[@class='pagebuilder-button-primary not-logged']")
MOBILE_SECAO_SOBRE = (By.XPATH, "//*[@id='sobre']")
MOBILE_SECAO_DIFERENCIAIS = (By.XPATH, "//*[@id='diferenciais']")
MOBILE_SECAO_PRODUTO = (By.XPATH, "//*[@id='produto']")

# Lp Estância 92
MOBILE_SECAO_NOSSA_HISTORIA = (By.XPATH, "//*[@id='nossa-historia']")

MOBILE_SECAO_OUTRAS_MARCAS = (By.XPATH, "//*[@id='marcas']")