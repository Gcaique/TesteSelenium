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
    nome_teste="primeiro acesso norte_prod",
    navegador="chrome",
    sistema_operacional="Windows 11",
    device_name=""
)
wait = WebDriverWait(driver, 10)

try:
    # Abre o navegador e acessa a pagina do Admin do Meu Minerva
    driver.get("https://meuminerva.com/adm_Min138/admin/")
    # Aguarda elemento carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='username']")))
    # Interagindo com o campo de login
    driver.find_element(By.XPATH, "//*[@id='username']").click()
    # Inserindo dado no campo de login
    driver.find_element(By.XPATH, "//*[@id='username']").send_keys("caique.oliveira")
    # Inserindo dado no campo de senha
    driver.find_element(By.XPATH, "//*[@id='login']").send_keys("s357951")
    # Interagindo com o botao  Entrar
    driver.find_element(By.XPATH, "//button[@class='action-login action-primary']/span").click()
    # Aguardando pagina carregar
    def test_primeiro_acesso_norte():
        driver.get(url)

        try:
            ...
        except TimeoutException:
            ...
    time.sleep(15)
    # Interagindo com o botao de fechar da mensagem
    from selenium.common.exceptions import TimeoutException

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//button[contains(@class,'action-close')])[1]")
            )
        ).click()
        print("Modal fechado")
    except TimeoutException:
        print("Modal não apareceu — seguindo o teste")
    # Aguardando elemento carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='menu-magento-customer-customer']")))
    # Interagindo com o menu Customer
    driver.find_element(By.XPATH, "//*[@id='menu-magento-customer-customer']").click()
    # Aguardando elemento carregar
    time.sleep(3)
    # Interagindo com o submenu All Customers
    driver.find_element(By.XPATH, "//*[@id='menu-magento-customer-customer']/div/ul/li[1]/a").click()
    # Aguardando pagina carregar
    time.sleep(8)
    time.sleep(8)
    # Interagindo com o botao de Filters
    driver.find_element(By.XPATH, "(//div[@class='data-grid-filters-actions-wrap']//button)[1]").click()
    # Aguardando pagina carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='admin__form-field-control']/input[@name='email']")))
    # Inserindo dado no filtro Email
    element = driver.find_element(By.XPATH, "//*[@class='admin__form-field-control']/input[@name='email']")
    element.clear()
    element.send_keys("caique.oliveira2@infobase.com.br")
    # Interagindo com o botao Apply Filters
    driver.find_element(By.XPATH, "//*[@class='admin__footer-main-actions']//button[@class='action-secondary']").click()
    # Aguardando elemento carregar
    time.sleep(8)
    # Interagindo com o botao Edit do customer
    driver.find_element(By.XPATH, " //td[@class='data-grid-actions-cell data-action-position']/a[normalize-space(text())='Edit']").click()
    # Aguardando pagina carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tab_customer']")))
    # Interagindo com o menu do Customer
    driver.find_element(By.XPATH, "//*[@id='tab_customer']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com o scroll da pagina
    element = driver.find_element(By.XPATH, "//*[@class='admin__field-control']//input[@type='email']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o campo email
    driver.find_element(By.XPATH, "//*[@class='admin__field-control']//input[@type='email']").click()
    # Inserindo dado no campo email
    element = driver.find_element(By.XPATH, "//*[@class='admin__field-control']//input[@type='email']")
    element.clear()
    element.send_keys("12345@infobase.com.br")
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o scroll da pagina
    element = driver.find_element(By.XPATH, "//div[@data-index='primeiro_acesso']//span[normalize-space(text())='Primeiro Acesso']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com a flag Primeiro Acesso
    driver.find_element(By.XPATH, "//div[@data-index='primeiro_acesso']//span[normalize-space(text())='Primeiro Acesso']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o scroll da pagina
    element = driver.find_element(By.XPATH, "//*[@class='admin__field']//span[normalize-space(text())='Internal Store Image 1']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o botao de salvar
    driver.find_element(By.XPATH, "//button[@id='save_and_continue']/span").click()
    # Aguardando disprado do alerta de sucesso
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='messages']//*[@class='message message-success success']")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Abre o navegador e acessa a pagina do Meu Minerva
    driver.get("https://meuminerva.com/")
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
    # Interagindo com o menu do usuario
    driver.find_element(By.XPATH, "//*[@id='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("caique.oliveira2@infobase.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando modal de Primeiro Acesso ser apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='select-number']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Criar Senha
    driver.find_element(By.XPATH, "//input[@id='select-number']").click()
    # Aguardando modal de Validacao carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@class='type-send-option']/span[normalize-space(text())='E-MAIL']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao EMAIL
    driver.find_element(By.XPATH, "//li[@class='type-send-option']/span[normalize-space(text())='E-MAIL']").click()
    # Aguardando modal de Validacao carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "(//ul[@class='options-list']//input[@name='email'])[2]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o segundo input
    driver.find_element(By.XPATH, "(//ul[@class='options-list']//input[@name='email'])[2]").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Enviar Codigo
    driver.find_element(By.XPATH, "(//*[@id='resend-code'])[2]").click()
    # Aguardando modal de insercao de token se apresentado
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='token']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # inserindo token invalido no campo de insercao
    driver.find_element(By.XPATH, "//input[@id='token']").send_keys("4567")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Verificar
    driver.find_element(By.XPATH, "//input[@id='verify-token']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de insercao do token
    driver.find_element(By.XPATH, "//input[@id='token']").click()
    # inserindo token invalido no campo
    element = driver.find_element(By.XPATH, "//input[@id='token']")
    element.clear()
    element.send_keys("456798")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Verificar
    driver.find_element(By.XPATH, "//input[@id='verify-token']").click()
    # Aguardando modal de Criar Senha ser apresentado
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Inserindo dado no campo de E-mail de Acesso
    driver.find_element(By.XPATH, "//*[@id='email-first-access']").send_keys("automatizacao@teste")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de Senha de Acesso
    driver.find_element(By.XPATH, "(//*[@name='password'])[1]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Inserindo dado no campo de Senha de Acesso
    driver.find_element(By.XPATH, "(//*[@name='password'])[1]").send_keys("Min@1234")
    # Interagindo com o primeiro icone de visibilidade
    driver.find_element(By.XPATH, "(//*[@class='field choice'])[2]").click()
    # Aguardando termometro carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Confirme sua Senha
    driver.find_element(By.XPATH, "//*[@name='confirm-password']").click()
    # Inserindo dado no campo Confirme sua Senha
    driver.find_element(By.XPATH, "//*[@name='confirm-password']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Criar Senha
    driver.find_element(By.XPATH, "//*[@id='save-account']").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de E-mail de Acesso
    driver.find_element(By.XPATH, "//*[@id='email-first-access']").click()
    # Inserindo dado no campo de E-mail de Acesso
    element = driver.find_element(By.XPATH, "//*[@id='email-first-access']")
    element.clear()
    element.send_keys("caique.oliveira2@infobase.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Senha de Acesso
    driver.find_element(By.XPATH, "(//*[@name='password'])[1]").click()
    # Inserindo dado no campo de Senha de Acesso
    element = driver.find_element(By.XPATH, "(//*[@name='password'])[1]")
    element.clear()
    element.send_keys("mina12")
    # Aguardando termometro carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # interagindo com o campo Confirme sua Senha
    driver.find_element(By.XPATH, "//*[@name='confirm-password']").click()
    # Inserindo dado no campo Confirme sua Senha
    element = driver.find_element(By.XPATH, "//*[@name='confirm-password']")
    element.clear()
    element.send_keys("mina12")
    # Aguardando elemento carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Senha de Acesso
    driver.find_element(By.XPATH, "(//*[@name='password'])[1]").click()
    # Inserindo dado no campo de Senha de Acesso
    element = driver.find_element(By.XPATH, "(//*[@name='password'])[1]")
    element.clear()
    element.send_keys("Min@1234")
    # Aguardando termometro carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # interagindo com o campo Confirme sua Senha
    driver.find_element(By.XPATH, "//*[@name='confirm-password']").click()
    # Inserindo dado no campo Confirme sua Senha
    element = driver.find_element(By.XPATH, "//*[@name='confirm-password']")
    element.clear()
    element.send_keys("Min@1245")
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # interagindo com o campo Confirme sua Senha
    driver.find_element(By.XPATH, "//*[@name='confirm-password']").click()
    # Inserindo dado no campo Confirme sua Senha
    element = driver.find_element(By.XPATH, "//*[@name='confirm-password']")
    element.clear()
    element.send_keys("Min@1234")
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o segundo icone de visibilidade
    driver.find_element(By.XPATH, "(//*[@class='field choice'])[3]").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Criar Senha
    driver.find_element(By.XPATH, "//*[@id='save-account']").click()
    # Aguardando modal de senha criada ser apresentada
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='close-modal-login']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Entrar
    driver.find_element(By.XPATH, "//*[@id='close-modal-login']").click()
    # Aguardando roleta de cupons ser apresentada
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='action-close hj-spintowin-close_button']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao fechar da roleta de cupons
    driver.find_element(By.XPATH, "//button[@class='action-close hj-spintowin-close_button']").click()
    # Aguarda elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Ação não reconhecida: printMessage
    # Ação em lowerCase: printmessage
    # Elemento: , Valor: AUTOMACAO FINALIZADA COM SUCESSO

finally:
    driver.quit()