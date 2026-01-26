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
    nome_teste="dashboard sul_prod",
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
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("smoketesting1@automatizacao.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    time.sleep(5)
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
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando roleta de cupons ser apresentada
    if driver.find_elements(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button"):
        driver.find_element(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button").click()
    # Interagindo com o botao fechar da roleta de cupons
    if driver.find_elements(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button"):
        driver.find_element(By.CSS_SELECTOR, "button.action-close.hj-spintowin-close_button").click()
    # Interagindo com Minha conta
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Minha conta']").click()
    # Aguardando pagina Minha conta carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando bloco de enderecos ser apresentado
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='box-content']//button[@class='button-main-address hj-account_dashboard_address-main_button']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Definir como principal
    driver.find_element(By.XPATH, "//*[@class='box-content']//button[@class='button-main-address hj-account_dashboard_address-main_button']").click()
    # Aguardando a apresentacao do modal
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='modal-inner-wrap']//button[@class='action action-primary action-accept']")))
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Definir da modal
    driver.find_element(By.XPATH, "//*[@class='modal-inner-wrap']//button[@class='action action-primary action-accept']").click()
    # Aguardando a ocultacao da modal
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='modal-inner-wrap']//button[@class='action action-primary action-accept']")))
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando bloco de enderecos ser apresentado
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='box-content']//button[@class='button-main-address hj-account_dashboard_address-main_button']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao ver todos Enderecos
    driver.find_element(By.XPATH, "//*[@class='block block-dashboard-addresses']//span[normalize-space(text())='Ver todos']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu Minha Conta
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space(text())='Minha conta']").click()
    # Aguardando pagina carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='action edit hj-account-order_history']/span")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao ver todos Pedido Recentes
    driver.find_element(By.XPATH, "//a[@class='action edit hj-account-order_history']/span").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu Minha Conta
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space(text())='Minha conta']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu Meus Pedidos
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space(text())='Meus pedidos']").click()
    # Aguardando grid carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='order-pagination __items-per-page']//select")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o filtro Periodo
    driver.find_element(By.XPATH, "//*[@class='order-filter __item __period-status']/select[@id='period']").click()
    # Selecionando filtro Ultimos 7 dias
    driver.find_element(By.XPATH, "//*[@class='order-filter __item __period-status']/select[@id='period']/option[@value='last_seven_days']").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Filtrar
    driver.find_element(By.XPATH, "//*[@class='order-filter __item __actions']/button").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando carregamento da grid
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Limpar filtro
    driver.find_element(By.XPATH, "//*[@class='order-filter __item __actions filter-active-enabled']//a").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando grid carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='order-pagination __items-per-page']//select")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu Lista de favoritos
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space(text())='Lista de favoritos']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu Enderecos
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[contains(normalize-space(text()),'Endere')]").click()
    # Aguardando pagina carregar
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "(//*[@class='box-content']//button[@class='button-main-address hj-account_default_address-main_button'])[2]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o sroll da pagina
    element = driver.find_element(By.XPATH, "(//*[@class='addresses-container']//*[@class='box-content'])[2]")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o segundo botao Definir como principal
    driver.find_element(By.XPATH, "(//*[@class='box-content']//button[@class='button-main-address hj-account_default_address-main_button'])[2]").click()
    # Aguardando a apresentacao do modal
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='modal-inner-wrap']//button[@class='action action-primary action-accept']")))
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Definir da modal
    driver.find_element(By.XPATH, "//*[@class='modal-inner-wrap']//button[@class='action action-primary action-accept']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando bloco de enderecos ser apresentado
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='box-content']//button[@class='button-main-address hj-account_default_address-main_button']")))
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu Meus pontos
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space(text())='Meus pontos']").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o filtro Tudo
    driver.find_element(By.XPATH, "//*[@class='reward-filter __container']//li[@id='reward-all']").click()
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o filtro Ganhou
    driver.find_element(By.XPATH, "//*[@class='reward-filter __container']//li[@id='reward-earnings']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o filtro Usados
    driver.find_element(By.XPATH, "//*[@class='reward-filter __container']//li[@id='reward-used']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o filtro Expirados
    driver.find_element(By.XPATH, "//*[@class='reward-filter __container']//li[@id='reward-expired']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o filtro Cancelados/devolvidos
    driver.find_element(By.XPATH, "//*[@class='reward-filter __container']//li[@id='reward-canceled']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando pagina carregar
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ver relatorios de pontos
    driver.find_element(By.XPATH, "//a[@class='report-action']").click()
    # Aguardando Relatorios de pontos ser carregada
    wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@class='rewardquests__filter__dropdown']")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o dropdown do filtro
    driver.find_element(By.XPATH, "//select[@class='rewardquests__filter__dropdown']").click()
    # Aguardando apresentacao do dropdown
    wait.until(EC.visibility_of_element_located((By.XPATH, "(//select[@class='rewardquests__filter__dropdown']/option)[2]")))
    # Interagindo com a segunda opcao do select
    driver.find_element(By.XPATH, "(//select[@class='rewardquests__filter__dropdown']/option)[2]").click()
    # Aguardando Relatorio carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@class='rewardquests__filter__dropdown']")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o link de Voltar para as missoes
    driver.find_element(By.XPATH, "//a[@class='rewardquests__go-to-missions__link']").click()
    # Aguardando pagina carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='rewardquests __see-rules hj-fidelity_see-rules']//span")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o menu Cadastro de redes
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space(text())='Cadastro de redes']").click()
    # Aguardando grid carregar
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='assigned-grid']//button[normalize-space(text())='Agrupar outro CNPJ']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a aba Agrupar CNPJ
    driver.find_element(By.XPATH, "(//*[@class='steps']//li)[2]").click()
    # Aguardando aba carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a aba Informacoes
    driver.find_element(By.XPATH, "(//*[@class='steps']//li)[3]").click()
    # Aguardando aba carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a aba Regras de agrupamento
    driver.find_element(By.XPATH, "(//*[@class='steps']//li)[4]").click()
    # Aguardando aba carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu  Meus cupons
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//*[normalize-space(text())='Meus cupons']").click()
    # Aguardando grid de cupons carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "(//*[@class='coupon-info']//span[@class='coupon-name'])[1]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ver mais
    driver.find_element(By.XPATH, "(//*[@class='coupon-info']//a[@class='coupon-action hj-my_coupons-action'])[1]").click()
    # Aguardando a expansao da descricao do cupom
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo o botao de copiar cupom
    driver.find_element(By.XPATH, "(//*[@class='coupon-content']//span[@class='code-copy'])[1]").click()
    # Aguardando disparo do alerta
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Ocultar
    driver.find_element(By.XPATH, "(//*[@class='coupon-info']//a[@class='coupon-action hj-my_coupons-action'])[1]").click()
    # Aguardando a expansao da descricao do cupom
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com a grid de indisponiveis
    driver.find_element(By.XPATH, "//li[@class='tabs-header-item hj-my_coupons-tab_item unavailable']/a").click()
    # Aguardando carregamento da grid
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o menu  Minhas missoes
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//*[contains(normalize-space(text()), 'Minhas miss')]").click()
    # Aguardando grid minhas missoes carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='rewardquests __see-rules hj-fidelity_see-rules']//span")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Redirecionando a pagina para a missao Recorrencia Frequencia
    element = driver.find_element(By.XPATH, "//*[@class='rewardquests __missions-item hj-fidelity_mission-recurrency_purchase']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com a missao Recorrencia Frequencia
    driver.find_element(By.XPATH, "//*[@class='rewardquests __missions-item hj-fidelity_mission-recurrency_purchase']").click()
    # Aguardando apresentacao da modal
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='rewardquests __modal-close hj-fidelity_action-modal-close']")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o botao Fechar da modal
    driver.find_element(By.XPATH, "//*[@class='rewardquests __modal-close hj-fidelity_action-modal-close']").click()
    # Aguardando ocultacao da modal Recorrencia Frequencia
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='rewardquests __modal-close hj-fidelity_action-modal-close']")))
    # Aguardando ocultacao da modal Recorrencia Frequencia
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com a missao Marca Recorrencia
    driver.find_element(By.XPATH, "//*[@class='rewardquests __missions-item hj-fidelity_mission-brand_recurrency_purchase']").click()
    # Aguardando apresentacao da modal
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='rewardquests __modal-close hj-fidelity_action-modal-close']")))
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o botao Fechar da modal
    driver.find_element(By.XPATH, "//*[@class='rewardquests __modal-close hj-fidelity_action-modal-close']").click()
    # Aguardando ocultacao da modal Marca Recorrencia
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[@class='rewardquests __modal-close hj-fidelity_action-modal-close']")))
    # Aguardando ocultacao da modal Marca Recorrencia
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o botao Ver meus pontos
    driver.find_element(By.XPATH, "//*[@class='rewardquests __view-points hj-fidelity_view-points']/span").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("-")
    # Interagindo com o menu Informacoes da conta
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[contains(normalize-space(text()),'Informa')]").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o primeiro botao Definir como principal
    driver.find_element(By.XPATH, "(//button[normalize-space(text())='Definir como principal'])[1]").click()
    # Aguardando modal de confirmacao ser apresentada
    wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='action-primary action-accept']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Definir da modal
    driver.find_element(By.XPATH, "//button[@class='action-primary action-accept']").click()
    # Aguardando disparo do alerta de sucesso
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='message-success success message']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o icone de WhatsApp
    driver.find_element(By.XPATH, "//*[@class='content sequence-1-1']//span[@class='slider hj-account_info-action_switch_whatsapp']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando finalizacao do loader
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//body[@class='account customer-account-edit page-layout-2columns-left mm-wrapper ajax-loading']")))
    # Aguardando finalizacao do loader
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o icone de WhatsApp
    driver.find_element(By.XPATH, "//*[@class='content sequence-1-1']//span[@class='slider hj-account_info-action_switch_whatsapp']").click()
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Aguardando finalizacao do loader
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//body[@class='account customer-account-edit page-layout-2columns-left mm-wrapper ajax-loading']")))
    # Aguardando finalizacao do loader
    time.sleep(2)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Editar do campo e-mail
    driver.find_element(By.XPATH, "//label[@for='change-email']//span[normalize-space(text())='Editar']").click()
    # Aguardando elemento carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='current-password']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail
    driver.find_element(By.XPATH, "//*[@id='current-email']").click()
    # Inserindo dado no campo E-mail
    element = driver.find_element(By.XPATH, "//*[@id='current-email']")
    element.clear()
    element.send_keys("smoketesting11@automatizacao.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Confirme seu E-mail
    driver.find_element(By.XPATH, "//*[@id='email']").click()
    # Inserindo dado no campo Confirme seu E-mail
    element = driver.find_element(By.XPATH, "//*[@id='email']")
    element.clear()
    element.send_keys("smoketesting11@automatizacao.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Insira sua Senha
    driver.find_element(By.XPATH, "//*[@id='current-password']").click()
    # Inserindo dado no campo Insira sua Senha
    driver.find_element(By.XPATH, "//*[@id='current-password']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Salvar
    driver.find_element(By.XPATH, "//button[@class='action save hj-customer-action_save']").click()
    # Aguardando disparo do alerta de sucesso
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='message-return']/*[@class='message-success success message']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Redirecionando a pagina para o botao Cancelar
    element = driver.find_element(By.XPATH, "//a[@class='action back cancel hj-customer-action_back_cancel']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Cancelar do campo e-mail
    driver.find_element(By.XPATH, "//a[@class='action back cancel hj-customer-action_back_cancel']").click()
    # Aguardando elemento carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='change-email']//span[normalize-space(text())='Editar']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Editar do campo senha
    driver.find_element(By.XPATH, "//label[@for='change-password']//span[normalize-space(text())='Editar']").click()
    # Aguardando elemento carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='current-password']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Insira sua senha atual
    driver.find_element(By.XPATH, "//*[@id='current-password']").click()
    # Inserindo dado no campo Insira sua senha atual
    driver.find_element(By.XPATH, "//*[@id='current-password']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo Insira sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password']").click()
    # Inserindo dado no campo Insira sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys("Min@1234567")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll da pagina
    element = driver.find_element(By.XPATH, "//*[@id='password-confirmation']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Interagindo com o campo Confirme sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password-confirmation']").click()
    # Inserindo dado no campo Confirme sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password-confirmation']").send_keys("Min@1234567")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o scroll da pagina
    element = driver.find_element(By.XPATH, "//button[@class='action save hj-customer-action_save']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Salvar
    driver.find_element(By.XPATH, "//button[@class='action save hj-customer-action_save']").click()
    # Aguardando disparo do alerta de sucesso
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='message-return']/*[@class='message-success success message']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Redirecionando a pagina para o alerta
    element = driver.find_element(By.XPATH, "//*[@id='message-return']/*[@class='message-success success message']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o sroll da pagina
    element = driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space(text())='Minha conta']")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element)
    # Interagindo com o menu Minha Conta
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[normalize-space(text())='Minha conta']").click()
    # Aguardando pagina carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Aguardando menu carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='action-logout']")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Sair
    driver.find_element(By.XPATH, "//*[@id='action-logout']").click()
    # Aguardando home deslogada carregar
    time.sleep(5)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Faca seu login
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Aguardando elemento carregar
    time.sleep(1)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").click()
    # Inserindo dado no campo E-mail/CNPJ
    driver.find_element(By.XPATH, "//input[@id='username']").send_keys("smoketesting1@automatizacao.com.br")
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
    element.send_keys("smoketesting11@automatizacao.com.br")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando campo de senha a ser apresentado
    time.sleep(3)
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Inserindo dado no campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").send_keys("Min@1234")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando disparo de alerta de senha invalida
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='message-error error message']//*[contains(normalize-space(text()),'A senha digitada')]")))
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o campo de senha
    driver.find_element(By.XPATH, "//*[@name='login[password]']").click()
    # Alterando dado no campo de senha
    element = driver.find_element(By.XPATH, "//*[@name='login[password]']")
    element.clear()
    element.send_keys("Min@1234567")
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com o botao Avancar
    driver.find_element(By.XPATH, "//button[@id='send2']").click()
    # Aguardando Home logada carregar
    time.sleep(8)
    # Captura de tela
    # driver.save_screenshot("screenshot.png")
    # Interagindo com Menu do usuario
    driver.find_element(By.XPATH, "//div[@id='login-name']").click()
    # Aguardando elemento carregar
    time.sleep(2)
    # Interagindo com Minha conta
    driver.find_element(By.XPATH, "//*[@id='login-dropdown']//a[normalize-space(text())='Minha conta']").click()
    # Aguardando pagina Minha conta carregar
    time.sleep(3)
    # Interagindo com o menu Informacoes da conta
    driver.find_element(By.XPATH, "//*[@id='block-collapsible-nav']//a[contains(normalize-space(text()),'Informa')]").click()
    # Aguardando pagina carregar
    time.sleep(3)
    # Interagindo com o botao Editar do campo e-mail
    driver.find_element(By.XPATH, "//label[@for='change-email']//span[normalize-space(text())='Editar']").click()
    # Aguardando elemento carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='current-password']")))
    # Interagindo com o campo E-mail
    driver.find_element(By.XPATH, "//*[@id='current-email']").click()
    # Inserindo dado no campo E-mail
    element = driver.find_element(By.XPATH, "//*[@id='current-email']")
    element.clear()
    element.send_keys("smoketesting1@automatizacao.com.br")
    # Interagindo com o campo Confirme seu E-mail
    driver.find_element(By.XPATH, "//*[@id='email']").click()
    # Inserindo dado no campo Confirme seu E-mail
    driver.find_element(By.XPATH, "//*[@id='email']").send_keys("smoketesting1@automatizacao.com.br")
    # Interagindo com o campo Insira sua Senha
    driver.find_element(By.XPATH, "//*[@id='current-password']").click()
    # Inserindo dado no campo Insira sua Senha
    driver.find_element(By.XPATH, "//*[@id='current-password']").send_keys("Min@1234567")
    # Interagindo com o botao Salvar
    driver.find_element(By.XPATH, "//button[@class='action save hj-customer-action_save']").click()
    # Aguardando disparo do alerta de sucesso
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='message-return']/*[@class='message-success success message']")))
    # Interagindo com o botao Cancelar do campo senha
    driver.find_element(By.XPATH, "//a[@class='action back cancel hj-customer-action_back_cancel']").click()
    # Aguardando elemento carregar
    wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='change-password']//span[normalize-space(text())='Editar']")))
    # Interagindo com o botao Editar do campo senha
    driver.find_element(By.XPATH, "//label[@for='change-password']//span[normalize-space(text())='Editar']").click()
    # Aguardando elemento carregar
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='current-password']")))
    # Inserindo dado no campo Insira sua senha atual
    driver.find_element(By.XPATH, "//*[@id='current-password']").send_keys("Min@1234567")
    # Interagindo com o campo Insira sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password']").click()
    # Inserindo dado no campo Insira sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password']").send_keys("Min@1234")
    # Interagindo com o campo Confirme sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password-confirmation']").click()
    # Inserindo dado no campo Confirme sua nova senha
    driver.find_element(By.XPATH, "//*[@id='password-confirmation']").send_keys("Min@1234")
    # Interagindo com o botao Salvar
    driver.find_element(By.XPATH, "//button[@class='action save hj-customer-action_save']").click()
    # Aguardando disparo do alerta de sucesso
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='message-return']/*[@class='message-success success message']")))
    # Ação não reconhecida: printMessage
    # Ação em lowerCase: printmessage
    # Elemento: , Valor: AUTOMACAO FINALIZADA COM SUCESSO

finally:
    driver.quit()