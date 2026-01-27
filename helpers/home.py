from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Redireciona a pagina para os elementos da HOME PAGE (Carrossel / mapa de corte / footer)
def scroll_and_confirm(wait, driver, xpath: str):
    locator = (By.XPATH, xpath)
    try:
        element = wait.until(EC.visibility_of_element_located(locator))
    except TimeoutException:
        assert False, f"Elemento NÃO encontrado (ou não visível) para o XPath: {xpath}"

    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    assert element.is_displayed(), f"Elemento encontrado, mas NÃO visível após scroll. XPath: {xpath}"