from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def select_pix_payment(driver, timeout=20):
    """
    O que faz:
    - Garante que o método de pagamento PIX fique selecionado.
    - Clica preferencialmente no LABEL (área maior e mais estável no iOS Safari).
    - Faz scroll para o elemento antes de clicar.
    - Confirma que o radio ficou checked.
    """
    wait = WebDriverWait(driver, timeout)

    # 1) Espera a seção de pagamento existir
    wait.until(EC.presence_of_element_located((By.ID, "checkout-payment-method-load")))

    # 2) Primeiro tenta pelo LABEL (mais clicável)
    label = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='dux_pay_pix']")))

    # scroll pro centro
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)

    # tenta clique normal
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='dux_pay_pix']"))).click()
    except Exception:
        # fallback: clique via JS
        driver.execute_script("arguments[0].click();", label)

    # 3) Confirma que o input ficou checked
    wait.until(lambda d: d.find_element(By.ID, "dux_pay_pix").is_selected())