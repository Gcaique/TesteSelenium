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
    nome_teste="logado norte_stg",
    navegador="chrome",
    sistema_operacional="Windows 11",
    device_name=""
)
wait = WebDriverWait(driver, 10)

try:
    # Abre o navegador e acessa a pagina do Meu Minerva
    driver.get("https://mcstaging.meuminerva.com/")
    # Aguarda elemento do cookie carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aceitar cookies
    driver.find_element(By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']").click()
    # Aguardando elemento do cookie a ser fechado
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@id='privacytools-banner-consent']//*[@title='Aceitar']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando modal de selecao de regiao a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='other-regions']")))
    # Interagindo com o primeiro botao da modal de regiao
    driver.find_element(By.XPATH, "//button[@id='other-regions']").click()
    # Aguardando Home Page carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("hub.teste2-bruno-popup@minervafoods.com")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@name='login[password]']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Alterando dado no campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando Home logada carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando roleta de cupons ser apresentada
    if driver.find_elements(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button"):
        driver.find_element(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Minha conta
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Minha conta']").click()
    # Aguardando pagina Minha conta carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Comparar produtos
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Comparar produtos']").click()
    # Aguardando pagina do Comparar produtos carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Meus pedidos
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pedidos']").click()
    # Aguardando pagina Meus pedidos carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a Lista de favoritos
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Lista de favoritos']").click()
    # Aguardando pagina Lista de favoritos carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Meus pontos
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus pontos']").click()
    # Aguardando pagina Meus pontos carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Meus cupons
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Meus cupons']").click()
    # Aguardando pagina Meus cupons carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com Minhas missoes
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[contains(normalize-space(text()), 'Minhas miss')]").click()
    # Aguardando pagina Minhas missoes carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com Selecionar regiao
    driver.find_element(By.XPATH, "//a[@class='change-region-action hj-header_change-region-action-desktop']").click()
    # Aguardando modal de selecao de regiao ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='southern-region']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o segundo botao da modal
    driver.find_element(By.XPATH, "//button[@id='southern-region']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Selecionar regiao
    driver.find_element(By.XPATH, "//a[@class='change-region-action hj-header_change-region-action-desktop']").click()
    # Aguardando modal de selecao de regiao a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='other-regions']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o primeiro botao da modal de regiao
    driver.find_element(By.XPATH, "//button[@id='other-regions']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo o icone do Mini-cart
    driver.find_element(By.XPATH, "//*[@class='action showcart']").click()
    # Aguardando Mini-cart ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='action showcart active']")))
    # Aguardando Mini-cart ser apresentado
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de fechar do Mini-cart
    driver.find_element(By.XPATH, "//button[@id='btn-minicart-close']").click()
    # Aguardando fechar o Mini-cart
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='action showcart']")))
    # Aguardando fechar o Mini-cart
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o primeiro carrossel
    element = driver.find_element(By.XPATH, "(//div[contains(@class, 'slider-products')])[1]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com o input do card de produto
    driver.find_element(By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]").click()
    # Inserindo dado no input
    element = driver.find_element(By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]")
    element.clear()
    element.send_keys("0'")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Rolando a pagina para o botao Adicionar
    element = driver.find_element(By.XPATH, "(//*[@class='slick-slide slick-current slick-active']//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Interagindo com o botao Adicionar
    driver.find_element(By.XPATH, "(//*[@class='slick-slide slick-current slick-active']//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando mini-cart ser apresentado
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper is-loading active']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando carregar atualizacao de itens no mini-cart
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper is-loading active']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando elementos da pagina a ficar interagivel
    time.sleep(2)
    # Interagindo com o campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").click()
    # Digitando termo no campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").send_keys("suino")
    # Aguardando dropdown da busca a ser apresentado
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='product-add-to-cart ']//button)[2]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Adicionar ao carrinho
    driver.find_element(By.XPATH, "(//div[@class='product-add-to-cart ']//button)[2]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando loading do mini-cart a ser apresentado
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando carregar atualizacao de itens no mini-cart
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando elementos da pagina a ficar interagivel
    time.sleep(2)
    # Interagindo com o campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").click()
    # Digitando termo no campo de Busca
    element = driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']")
    element.clear()
    element.send_keys("pack")
    # Aguardando dropdown da busca a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class='see-all-link']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").click()
    # Digitando termo no campo de Busca
    element = driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']")
    element.clear()
    element.send_keys("carne")
    # Aguardando dropdown da busca a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class='see-all-link']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de Ver todos
    driver.find_element(By.XPATH, "//a[@class='see-all-link']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de paginacao para a Segunda pagina
    driver.find_element(By.XPATH, "//div[@class='pages']//ul//span[normalize-space(text())='2']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de filtros Por Conservacao
    driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[1]/span").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de filtro Resfriado
    driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[1]/div[2]/div/ol/li[2]/a/label/span[1]").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Expandindo o elemento de filtros Por Marca
    if driver.find_elements(By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[1]"):
        driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o primeiro select do filtro Marca
    if driver.find_elements(By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[2]/div/ol/li[1]/a/label/span[1]"):
        driver.find_element(By.XPATH, "//*[@id='narrow-by-list']/div[2]/div[2]/div/ol/li[1]/a/label/span[1]").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Limpando os filtros
    driver.find_element(By.XPATH, "//div[@class='block-actions filter-actions']//*[normalize-space(text())='Limpar Tudo']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de ordenacao de Menor preco
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='low_to_high']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o elemento de ordenacao de Maior preco
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='high_to_low']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Expandindo o elemento de ordenacao
    driver.find_element(By.XPATH, "//div[@class='toolbar-sorter sorter']//*[@id='sorter']").click()
    # Interagindo com o elemento de ordenacao de Recomendado
    driver.find_element(By.XPATH, "//*[@id='sorter']/option[@value='relevance']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Interagindo com o botao incrementar
    driver.find_element(By.XPATH, "(//div[@class='product-item-qty-container']//button[@class='increment-qty hj-product_card-increment_qty'])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Adicionar
    driver.find_element(By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando loading do mini-cart a ser apresentado
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando carregar atualizacao de itens no mini-cart
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando elementos da pagina a ficar interagivel
    time.sleep(6)
    # Interagindo com a categoria Promocoes
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[contains(normalize-space(text()), 'Promo')]").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='toolbar-amount']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Interagindo com o input do card de produto
    driver.find_element(By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]").click()
    # Inserindo dado no input
    element = driver.find_element(By.XPATH, "(//*[contains(@id,'product-item-qty')])[1]")
    element.clear()
    element.send_keys("2'")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Adicionar
    driver.find_element(By.XPATH, "(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando loading do mini-cart a ser apresentado
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando carregar atualizacao de itens no mini-cart
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando elementos da pagina a ficar interagivel
    time.sleep(2)
    # Interagindo com a categoria Pescados
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Pescados']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o primeiro produto da categoria
    driver.find_element(By.XPATH, "(//*[contains(@id,'product-item-info')]//span[@class='product-image-wrapper'])[1]").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao incrementar
    driver.find_element(By.XPATH, "(//button[@class='increment-qty hj-product_card-increment_qty'])[1]").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Adicionar ao carrinho
    driver.find_element(By.XPATH, "//button[@id='product-addtocart-button']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando loading do mini-cart a ser apresentado
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando carregar atualizacao de itens no mini-cart
    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='minicart-wrapper active is-loading']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando elementos da pagina a ficar interagivel
    time.sleep(2)
    # Interagindo com o select de endereco Previsao de entrega
    driver.find_element(By.XPATH, "//*[@id='addresses']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o dropdown de endereco
    driver.find_element(By.XPATH, "//*[@id='addresses']/option[2]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Consultar
    driver.find_element(By.XPATH, "//input[@id='verify-delivery-forecast']").click()
    # Aguardando elemento de Previsao de entrega carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='shipping-rate-result']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a categoria Cordeiros
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Cordeiros']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@class='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "//*[@id='limiter']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de paginacao para a segunda pagina
    driver.find_element(By.XPATH, "//div[@class='pages']//ul//span[normalize-space(text())='2']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll na pagina
    element = driver.find_element(By.XPATH, "(//*[@class='product-item-info'])[5]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao do Avise-me
    driver.find_element(By.XPATH, "(//button[contains(@id,'button_disabled')]//span[contains(normalize-space(text()),'Avise-me')])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando botao mudar de status
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Atualizando a pagina
    # Ação não reconhecida: refresh
    # Ação em lowerCase: refresh
    # Elemento: , Valor:
    # Aguardando pagina carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao do Avise-me ativado
    driver.find_element(By.XPATH, "(//button[contains(@id,'button_enabled')]//span[contains(normalize-space(text()),'Ok, avisaremos')])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando botao mudar de status
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o produto da categoria
    elementos = driver.find_elements(By.XPATH,
                                     "(//*[contains(@id,'product-item-info')]//span[@class='product-image-wrapper'])")
    if len(elementos) >= 4:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", elementos[3])
        driver.execute_script("arguments[0].click();", elementos[3])
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao do Avise-me
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@id,'button_disabled')]//span[contains(normalize-space(),'Avise-me')]"
            ))
        ).click()
    except:
        pass
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando botao mudar de status
    time.sleep(4)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Atualizando a pagina
    # Ação não reconhecida: refresh
    # Ação em lowerCase: refresh
    # Elemento: , Valor:
    # Aguardando pagina carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao do Avise-me ativado
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@id,'button_enabled')]//span[contains(normalize-space(),'Ok, avisaremos')]"
            ))
        ).click()
    except:
        pass
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando botao mudar de status
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ver Carrinho
    driver.find_element(By.XPATH, "//a[@class='action viewcart']").click()
    # Aguardando pagina carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[@id='empty_cart_button']/span")))
    # Interagindo com o botao Limpar carrinho
    driver.find_element(By.XPATH, "//button[@id='empty_cart_button']/span").click()
    # Aguardando elemento carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='action-primary action-accept']")))
    # Interagindo com o botao Confirmar
    driver.find_element(By.XPATH, "//button[@class='action-primary action-accept']").click()
    # Aguardando elemento carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='action primary']")))
    # Interagindo com o botao Ver catalogo
    driver.find_element(By.XPATH, "//a[@class='action primary']").click()
    # Aguardando pagina carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Ação não reconhecida: printMessage
    # Ação em lowerCase: printmessage
    # Elemento: , Valor: AUTOMACAO FINALIZADA COM SUCESSO

finally:
    driver.quit()