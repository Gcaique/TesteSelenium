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
    nome_teste="login logout sul-prod",
    navegador="chrome",
    sistema_operacional="Windows 11",
    device_name=""
)
wait = WebDriverWait(driver, 10)

try:
    # Abre o navegador e acessa a pagina do Meu Minerva
    driver.get("https://mcstaging.meuminerva.com/")
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
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("teste.12345@teste.com")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando disparo de alerta e-mail nao encontrado
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(text()),'Verifique o dado informado ou tente acessar com um CPF/CNPJ.')]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    element = driver.find_element(By.XPATH, "//input[@id='username']")
    element.clear()
    element.send_keys("42.765.782/0001-08")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando disparo de alerta de e-mail nao encontrado
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(text()),'Verifique o dado informado ou tente acessar com um e-mail.')]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    element = driver.find_element(By.XPATH, "//input[@id='username']")
    element.clear()
    element.send_keys("teste.teste")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando disparo de alerta de e-mail invalido
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(normalize-space(text()), 'Insira um e-mail ou CNPJ/CPF')]")
        )
    )
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    element = driver.find_element(By.XPATH, "//input[@id='username']")
    element.clear()
    element.send_keys("11.222.333/4444-55")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando disparo de alerta de CNPJ/CPF invalido
    WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(text()),'Insira um e-mail ou CNPJ/CPF')]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    element = driver.find_element(By.XPATH, "//input[@id='username']")
    element.clear()
    element.send_keys("caique.oliveira@infobase.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@name='login[password]']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Alterando dado no campo E-mail/CNPJ
    element = driver.find_element(By.XPATH, "//input[@id='username']")
    element.clear()
    element.send_keys("caique.oliveira@teste.com")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Alterando dado no campo E-mail/CNPJ
    element = driver.find_element(By.XPATH, "//input[@id='username']")
    element.clear()
    element.send_keys("caique.oliveira@infobase.com.br")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Inserindo dado no campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").send_keys("min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando disparo de alerta de senha invalida
    WebDriverWait(driver, 35).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(text()),'A senha digitada')]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Alterando dado no campo de senha
    element = driver.find_element(By.XPATH, "//*[@name='login[password]']")
    element.clear()
    element.send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando roleta de cupons ser apresentada
    time.sleep(8)
    import time
    from selenium.webdriver.common.by import By
    time.sleep(5)  # garante que a roleta já apareceu
    try:
        driver.find_element(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button").click()
    except:
        pass
    # Interagindo com o botao fechar da roleta de cupons
    try:
        driver.find_element(By.XPATH, "//button[@class='action-close hj-spintowin-close_button']").click()
    except:
        pass  # se o botão não existir, apenas continua
    # Aguarda elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
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
    # Interagindo com a categoria Bovinos
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Bovinos']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
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
    # Interagindo com a categoria Promocoes
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[contains(normalize-space(text()), 'Promo')]").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
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
    # Interagindo com o campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").click()
    # Digitando termo no campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").send_keys("pul")
    # Aguardando elemento carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de Busca
    driver.find_element(By.XPATH, "//button[@title='Buscar']/span[normalize-space(text())='Buscar']").click()
    # Aguardando pagina carregar
    time.sleep(3)
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
    # Interagindo com a logo do site
    driver.find_element(By.XPATH, "//a[@class='logo hj-header-logo']").click()
    # Aguardando botao Ultimos Pedidos ficar interagivel
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@id='last-orders-action']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ultimos Pedidos
    driver.find_element(By.XPATH, "//a[@id='last-orders-action']").click()
    # Aguardando grid de Ultimos Pedidos carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ver produtos
    driver.find_element(By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a").click()
    # Aguardando botao Ultimos Produtos Comprados ficar interagivel
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@id='last-items-action']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ultimos Produtos Comprados
    driver.find_element(By.XPATH, "//a[@id='last-items-action']").click()
    # Aguardando grid de Ultimos Pedidos carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ver produtos
    driver.find_element(By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a").click()
    # Aguardando Home logada carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu do usuario
    driver.find_element(By.XPATH, "//*[@id='login-name']").click()
    # Aguardando menu carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='action-logout']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Sair
    driver.find_element(By.XPATH, "//*[@id='action-logout']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
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
    # Interagindo com a categoria Bovinos Premium
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[normalize-space(text())='Bovinos']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
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
    # Interagindo com a categoria Promocoes
    driver.find_element(By.XPATH, "//*[@id='nav-menu-desktop']//span[contains(normalize-space(text()), 'Promo')]").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
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
    # Interagindo com o campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").click()
    # Digitando termo no campo de Busca
    driver.find_element(By.XPATH, "//input[@id='minisearch-input-top-search']").send_keys("pul")
    # Aguardando elemento carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao de Busca
    driver.find_element(By.XPATH, "//button[@title='Buscar']/span[normalize-space(text())='Buscar']").click()
    # Aguardando pagina carregar
    time.sleep(3)
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
    # Interagindo com a Logo do site
    driver.find_element(By.XPATH, "//a[@class='logo hj-header-logo']").click()
    # Aguardando botao Ultimos Pedidos ficar interagivel
    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@id='last-orders-action']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ultimos Pedidos
    driver.find_element(By.XPATH, "//a[@id='last-orders-action']").click()
    # Aguardando modal de Acesso a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='secondary login-name']//button[@id='send2']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("caique.oliveira@infobase.com.br")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@name='login[password]']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Inserindo dado no campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando grid de Ultimos Pedidos carregar
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a")))
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando roleta de cupons ser apresentada
    time.sleep(8)
    import time
    from selenium.webdriver.common.by import By

    time.sleep(5)  # garante que a roleta já apareceu
    try:
        driver.find_element(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button").click()
    except:
        pass
    # Interagindo com o botao fechar da roleta de cupons
    try:
        driver.find_element(By.XPATH, "//button[@class='action-close hj-spintowin-close_button']").click()
    except:
        pass  # se o botão não existir, apenas continua
    # Aguarda elemento carregar
    time.sleep(2)
    # Interagindo com o botao fechar da roleta de cupons
    try:
        driver.find_element(By.XPATH, "//button[@class='action-close hj-spintowin-close_button']").click()
    except:
        pass  # se não existir, segue em frente
    # Aguarda elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu do usuario
    driver.find_element(By.XPATH, "//*[@id='login-name']").click()
    # Aguardando menu carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='action-logout']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Sair
    driver.find_element(By.XPATH, "//*[@id='action-logout']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ultimos Produtos Comprados
    driver.find_element(By.XPATH, "//a[@id='last-items-action']").click()
    # Aguardando modal de Acesso a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='secondary login-name']//button[@id='send2']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("caique.oliveira@infobase.com.br")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@name='login[password]']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Inserindo dado no campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando grid de Ultimos Produtos Comprados carregar
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='customer-orders __empty-grid hj-empty-grid__message']//a")))
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando roleta de cupons ser apresentada
    try:
        driver.find_element(By.XPATH, "//button[@class='action-close hj-spintowin-close_button']").click()
    except:
        pass  # se não existir, segue em frente
    # Interagindo com o botao fechar da roleta de cupons
    try:
        driver.find_element(By.XPATH, "//button[@class='action-close hj-spintowin-close_button']").click()
    except:
        pass  # se o botão não existir, continua o teste
    # Aguarda elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu do usuario
    driver.find_element(By.XPATH, "//*[@id='login-name']").click()
    # Aguardando menu carregar
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='action-logout']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Sair
    driver.find_element(By.XPATH, "//*[@id='action-logout']").click()
    # Aguardando Home Page carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Ação não reconhecida: printMessage
    # Ação em lowerCase: printmessage
    # Elemento: , Valor: AUTOMACAO FINALIZADA COM SUCESSO

finally:
    driver.quit()