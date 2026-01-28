from selenium.webdriver.common.by import By

URL_HOME = "https://meuminerva.com/"

# Cookies
COOKIE_ACCEPT = (By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")

# Região
REGION_OPEN = (By.XPATH, "//a[contains(@class,'change-region-action') and contains(@class,'hj-header_change-region-action-desktop')]")
BTN_DEFAULT_REGION = (By.ID, "other-regions")
BTN_SUL_REGION = (By.ID, "southern-region")
REGION_MODAL = (By.CSS_SELECTOR, "div.modal-select-region")


# Indicador de LOGADO (fonte da verdade)
MINICART_WRAPPER = (By.XPATH, "//*[@data-block='minicart' and contains(@class,'minicart-wrapper')]")

# Roleta / Hotjar
SPIN_CLOSE = (By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button")
HOTJAR_CLOSE = (By.XPATH, "//dialog//button") # fallback (se aparecer)