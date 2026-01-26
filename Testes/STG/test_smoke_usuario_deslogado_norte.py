import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config


def test_smoke_usuario_deslogado_norte():
    # Configuração do WebDriver usando config
    driver = config.criar_driver("Abre o navegador e acessa a página do Meu Minerva")
    wait = WebDriverWait(driver, 10)

    try:
        # =========================
        # Acessar site
        # =========================
        driver.get("https://mcstaging.meuminerva.com.br/")

        # =========================
        # Aceitar cookies
        # =========================
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")
        ))
        driver.save_screenshot("screenshot.png")
        driver.find_element(By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']").click()
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")
        ))
        driver.save_screenshot("screenshot.png")

        # =========================
        # Modal seleção de região
        # =========================
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='other-regions']")))
        driver.find_element(By.XPATH, "//button[@id='other-regions']").click()
        time.sleep(5)
        driver.save_screenshot("screenshot.png")

        # =========================
        # Login / Termo de uso
        # =========================
        driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
        driver.save_screenshot("screenshot.png")

        driver.find_element(By.XPATH, "//a[@id='login-terms']").click()
        time.sleep(3)
        driver.save_screenshot("screenshot.png")

        driver.find_element(By.XPATH, "//button[@class='close-modal']").click()

        # =========================
        # Quero ser cliente
        # =========================
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@id='modal-customer-open']/span[normalize-space()='Quero ser cliente']")
        ))
        driver.find_element(
            By.XPATH,
            "//button[@id='modal-customer-open']/span[normalize-space()='Quero ser cliente']"
        ).click()

        time.sleep(2)
        driver.save_screenshot("screenshot.png")

        driver.find_element(
            By.XPATH, "(//*[@class='modal-inner-wrap']//button[@class='action-close'])[2]"
        ).click()
        time.sleep(1)

        # =========================
        # Scroll home / seções
        # =========================
        sections_xpaths = [
            "(//div[contains(@class, 'slider-products')])[1]",
            "//div[@class='brands-carousel']",
            "(//div[contains(@class, 'slider-products')])[2]",
            "//*[@class='cutting-map __home-section']",
            "//div[@class='footer-content']"
        ]

        for xpath in sections_xpaths:
            element = driver.find_element(By.XPATH, xpath)
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element
            )
            driver.save_screenshot("screenshot.png")

        # =========================
        # Busca de produto
        # =========================
        search_input = driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']")
        search_input.click()
        search_input.send_keys("angus")
        time.sleep(2)
        driver.save_screenshot("screenshot.png")

        driver.find_element(
            By.XPATH, "//button[@title='Buscar']/span[normalize-space()='Buscar']"
        ).click()
        time.sleep(2)
        driver.save_screenshot("screenshot.png")

        # =========================
        # Paginação
        # =========================
        for page in ["2", "3"]:
            element = driver.find_element(By.XPATH, "//div[@class='pages']//ul")
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element
            )
            driver.save_screenshot("screenshot.png")

            driver.find_element(
                By.XPATH, f"//div[@class='pages']//ul//span[normalize-space()='{page}']"
            ).click()
            time.sleep(2)
            driver.save_screenshot("screenshot.png")

        # =========================
        # Filtros
        # =========================
        filtros = [
            ("//*[@id='narrow-by-list']/div[1]/div[1]/span", None),
            ("//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]", None),
            ("//div[@class='block-actions filter-actions']//*[normalize-space()='Limpar Tudo']", None),
            ("//div[@class='toolbar-sorter sorter']//*[@id='sorter']", "name_asc"),
            ("//*[@id='sorter']/option[@value='name_asc']", None),
            ("//*[@id='sorter']/option[@value='name_desc']", None)
        ]

        for xpath, option_value in filtros:
            driver.find_element(By.XPATH, xpath).click()
            if option_value:
                driver.find_element(
                    By.XPATH, f"//*[@id='sorter']/option[@value='{option_value}']"
                ).click()
            time.sleep(2)
            driver.save_screenshot("screenshot.png")

        # =========================
        # Categorias
        # =========================
        categorias = ["Bovinos Premium", "Promo", "Pescados", "Bovinos"]
        for categoria in categorias:
            driver.find_element(
                By.XPATH,
                f"//*[@id='nav-menu-desktop']//span[contains(normalize-space(), '{categoria}')]"
            ).click()
            time.sleep(2)
            driver.save_screenshot("screenshot.png")

        # =========================
        # Login nos produtos
        # =========================
        produtos_indices = [1, 10]
        for idx in produtos_indices:
            driver.find_element(
                By.XPATH,
                f"(//a[@class='action tocart primary loggin-btn tget-btn-buy']/span[normalize-space()='Entrar'])[{idx}]"
            ).click()

            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='username']"))
            )
            driver.save_screenshot("screenshot.png")

        # =========================
        # PDP
        # =========================
        driver.find_element(
            By.XPATH, "(//*[contains(@id,'product-item-info')]//strong)[10]"
        ).click()

        time.sleep(5)
        driver.save_screenshot("screenshot.png")

        driver.find_element(
            By.XPATH, "//button[@class='loggin-btn primary tget-btn-buy']"
        ).click()

        time.sleep(2)
        driver.save_screenshot("screenshot.png")

        # =========================
        # CLIQUE NO LOGO (AJUSTADO)
        # =========================
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        logo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class,'hj-header-logo')]")
            )
        )

        try:
            logo.click()
        except:
            driver.execute_script("arguments[0].click();", logo)

        driver.save_screenshot("screenshot.png")
        time.sleep(5)

        # =========================
        # Últimos pedidos / produtos
        # =========================
        ultimos = ["last-orders-action", "last-items-action"]
        for action in ultimos:
            driver.find_element(By.XPATH, f"//a[@id='{action}']").click()

            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@class='secondary login-name']//button[@id='send2']")
                )
            )
            driver.save_screenshot("screenshot.png")

            driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
            driver.save_screenshot("screenshot.png")

        # =========================
        # Troca de região
        # =========================
        regioes = ["southern-region", "other-regions"]
        for regiao in regioes:
            driver.find_element(
                By.XPATH,
                "//a[@class='change-region-action hj-header_change-region-action-desktop']"
            ).click()

            wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//button[@id='{regiao}']"))
            )
            driver.save_screenshot("screenshot.png")

            driver.find_element(By.XPATH, f"//button[@id='{regiao}']").click()
            time.sleep(8)
            driver.save_screenshot("screenshot.png")

        print("AUTOMACAO FINALIZADA COM SUCESSO")

    finally:
        driver.quit()
