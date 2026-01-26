from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import config

# Configuração do WebDriver usando config
driver = config.criar_driver(
    ambiente="desktop",
    nome_teste="usuario_deslogado_sul",
    navegador="chrome",
    sistema_operacional="Windows 11",
    device_name=""
)
wait = WebDriverWait(driver, 10)

try:
    # Abre o navegador e acessa a pagina do Meu Minerva
    driver.get("https://meuminerva.com/")
    # Aguardando modal de selecao de regiao a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='southern-region']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o segundo botao da modal de regiao
    driver.find_element(By.XPATH, "//button[@id='southern-region']").click()
    # Aguardando Home Page carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguarda elemento do cookie carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")))
    # Aceitar cookies
    driver.find_element(By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']").click()
    # Aguardando elemento do cookie a ser fechado
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o link Termo de uso
    driver.find_element(By.XPATH, "//a[@id='login-terms']").click()
    # Aguardando elemento carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Fechando modal Termo de uso
    driver.find_element(By.XPATH, "//button[@class='close-modal']").click()
    # Aguardando elemento carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[@id='modal-customer-open']/span[normalize-space(text())='Quero ser cliente']")))
    # Interagindo com o botao Quero ser cliente
    driver.find_element(By.XPATH, "//button[@id='modal-customer-open']/span[normalize-space(text())='Quero ser cliente']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # fechar a modal Quero ser cliente
    driver.find_element(By.XPATH, "(//*[@class='modal-inner-wrap']//button[@class='action-close'])[2]").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Rolando a pagina para o primeiro carrossel
    element = driver.find_element(By.XPATH, "(//div[contains(@class, 'slider-products')])[1]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o carrossel de marcas
    element = driver.find_element(By.XPATH, "//div[@class='brands-carousel']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o segundo carrossel
    element = driver.find_element(By.XPATH, "(//div[contains(@class, 'slider-products')])[2]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o Mapa de corte
    element = driver.find_element(By.XPATH, "//*[@class='cutting-map __home-section']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o Footer
    element = driver.find_element(By.XPATH, "//div[@class='footer-content']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").click()
    # Digitando termo no campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").send_keys("pul")
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de Busca
    driver.find_element(By.XPATH, "//button[@title='Buscar']/span[normalize-space(text())='Buscar']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll
    # Ação não reconhecida: scrollToTop
    # Ação em lowerCase: scrolltotop
    # Elemento: xpath=(//*[contains(@id,'product-item-info')]//strong)[1], Valor:
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de filtros Por Conservacao
    driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[1]/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de filtro Resfriado
    driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Limpando os filtros
    driver.find_element(By.XPATH, "//div[@class='block-actions filter-actions']//*[normalize-space(text())='Limpar Tudo']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de ordenacao de A-Z
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='name_asc']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de ordenacao de Z-A
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='name_desc']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a categoria Bovinos
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Bovinos']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o elemento de paginacao
    element = driver.find_element(By.XPATH, "//div[@class='pages']//ul")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de paginacao para a Segunda pagina
    driver.find_element(By.XPATH, "//div[@class='pages']//ul//span[normalize-space(text())='2']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll
    # Ação não reconhecida: scrollToTop
    # Ação em lowerCase: scrolltotop
    # Elemento: xpath=(//*[contains(@id,'product-item-info')]//strong)[1], Valor:
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a ultima categoria
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[contains(normalize-space(text()), 'Promo')]").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de filtros Por Marca
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="narrow-by-list"]/div/div[1]')
        )
    ).click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de filtro Pul
    driver.find_element(
        By.XPATH,
        '//*[@id="narrow-by-list"]/div/div[2]/div/ol/li[1]/a/label/span[1]'
    ).click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de filtros Por Conservacao
    driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[1]/span").click()
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o elemento de filtro Congelado
    driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("-")
    # Limpando os filtros
    driver.find_element(By.XPATH, "//div[@class='block-actions filter-actions']//*[normalize-space(text())='Limpar Tudo']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a categoria Marcas
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Marcas']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de ordenacao de Z-A
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='name_desc']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de ordenacao de A-Z
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='name_asc']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Entrar do primeiro item
    driver.find_element(By.XPATH, "(//a[@class='action tocart primary loggin-btn tget-btn-buy']/span[normalize-space(text())='Entrar'])[1]").click()
    # Aguardando elemento carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='username']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o elemento de paginacao
    element = driver.find_element(By.XPATH, "//div[@class='pages']//ul")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Entrar do decimo item
    driver.find_element(By.XPATH, "(//a[@class='action tocart primary loggin-btn tget-btn-buy']/span[normalize-space(text())='Entrar'])[10]").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a PDP de um item da lista
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as EC

    produto = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//*[contains(@id,'product-item-info')]//strong)[10]")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", produto)
    produto.click()
    # Aguardando elemento carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Entrar da PDP
    driver.find_element(By.XPATH, "//button[@class='loggin-btn primary tget-btn-buy']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a Logo do site
    driver.find_element(By.XPATH, "//a[@class='logo hj-header-logo']").click()
    # Aguardando elemento carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ultimos Pedidos
    driver.find_element(By.XPATH, "//a[@id='last-orders-action']").click()
    # Aguardando modal de Acesso a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='secondary login-name']//button[@id='send2']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ultimos Produtos Comprados
    driver.find_element(By.XPATH, "//a[@id='last-items-action']").click()
    # Aguardando modal de Acesso a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='secondary login-name']//button[@id='send2']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Selecionar regiao
    driver.find_element(By.XPATH, "//a[@class='change-region-action hj-header_change-region-action-desktop']").click()
    # Aguardando modal de selecao de regiao ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='other-regions']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o primeiro botao da modal
    driver.find_element(By.XPATH, "//button[@id='other-regions']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Selecionar regiao
    driver.find_element(By.XPATH, "//a[@class='change-region-action hj-header_change-region-action-desktop']").click()
    # Aguardando modal de selecao de regiao a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='southern-region']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o segundo botao da modal de regiao
    driver.find_element(By.XPATH, "//button[@id='southern-region']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Ação não reconhecida: printMessage
    # Ação em lowerCase: printmessage
    # Elemento: , Valor: AUTOMACAO FINALIZADA COM SUCESSO

finally:
    driver.quit()