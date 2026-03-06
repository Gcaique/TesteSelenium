from selenium.webdriver.common.by import By

# ===== HEADER =====
BTN_LOGIN_HEADER = (By.XPATH, "//a[contains(@href,'login')]")
BTN_LOGOUT_HEADER = (By.XPATH, "//a[contains(@href,'logout')]")

# ===== LOGIN PAGE =====
LINK_ESQUECI_SENHA = (By.XPATH, "//a[contains(@href,'recover')]")

# ===== RECUPERAÇÃO =====
INPUT_EMAIL = (By.ID, "email")
BTN_ENVIAR = (By.XPATH, "//button[@type='submit']")

# ===== MENSAGEM =====
MSG_SUCESSO = (By.XPATH, "//*[contains(text(),'email enviado')]")