import time

from selenium.webdriver.support import expected_conditions as EC

from locators.redefinir_senha import *

from helpers.actions import clear_and_type, mobile_click_strict

def clicar_sms_modal(driver, wait):
    """Clica no botao SMS da modal de recuperacao."""
    wait.until(EC.element_to_be_clickable(BTN_SMS_MODAL)).click()
    time.sleep(3)

def clicar_email_modal(driver, wait):
    """Clica no botao E-mail da modal de recuperacao."""
    wait.until(EC.element_to_be_clickable(BTN_EMAIL_MODAL)).click()
    time.sleep(3)

def clicar_avancar_modal(driver, wait):
    """Clica no botao Avancar da modal."""
    wait.until(EC.element_to_be_clickable(BTN_AVANCAR_MODAL)).click()

def clicar_voltar_modal(driver, wait):
    """Clica no botao Voltar da modal."""
    wait.until(EC.element_to_be_clickable(BTN_VOLTAR_MODAL)).click()
    time.sleep(2)

def aguardar_alerta_modal(driver, wait):
    """Aguarda o alerta/warning na modal."""
    wait.until(EC.visibility_of_element_located(MSG_ALERTA_MODAL))

def selecionar_email_option(driver, wait):
    """Seleciona a primeira opcao de e-mail na modal."""
    wait.until(EC.element_to_be_clickable(INPUT_EMAIL_OPTION_0)).click()
    time.sleep(1)

def clicar_recebi_link(driver, wait):
    """Clica no botao 'Recebi o link' na modal de verificacao."""
    wait.until(EC.element_to_be_clickable(BTN_RECEBI_LINK)).click()
    time.sleep(2)


# ADMIN
def login_admin(driver, wait, usuario, senha):
    """Faz login no painel admin do Magento."""
    wait.until(EC.visibility_of_element_located(ADMIN_INPUT_USERNAME)).click()
    driver.find_element(*ADMIN_INPUT_USERNAME).send_keys(usuario)
    driver.find_element(*ADMIN_INPUT_PASSWORD).send_keys(senha)
    driver.find_element(*ADMIN_BTN_ENTRAR).click()
    time.sleep(5)
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_FECHAR_MODAL))
    driver.find_element(*ADMIN_BTN_FECHAR_MODAL).click()

def navegar_email_logs(driver, wait):
    """Navega ate a pagina de Email Logs no admin."""
    wait.until(EC.element_to_be_clickable(ADMIN_MENU_STORES)).click()
    wait.until(EC.element_to_be_clickable(ADMIN_SUBMENU_EMAIL_LOGS)).click()
    time.sleep(5)

def filtrar_email_logs(driver, wait, email_destinatario):
    """Aplica filtro de Recipient no grid de Email Logs."""
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_FILTERS)).click()
    wait.until(EC.visibility_of_element_located(ADMIN_INPUT_RECIPIENT))
    clear_and_type(driver, ADMIN_INPUT_RECIPIENT, email_destinatario)
    driver.find_element(*ADMIN_BTN_APPLY_FILTERS).click()
    time.sleep(5)

def abrir_primeiro_email(driver, wait):
    """Abre o primeiro resultado de e-mail via botao Select > View."""
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_SELECT_FIRST)).click()
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_VIEW)).click()
    time.sleep(3)


def obter_link_redefinicao_do_iframe(driver, wait):
    """
    Entra no iframe do template de email, clica no link de redefinicao
    e muda para a nova janela 'Criar nova senha'.
    """
    iframe = wait.until(EC.presence_of_element_located(ADMIN_IFRAME_EMAIL))
    driver.switch_to.frame(iframe)
    driver.find_element(*ADMIN_LINK_EMAIL_BODY).click()
    time.sleep(5)
    driver.switch_to.default_content()

    # Muda para a janela "Criar nova senha"
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "Criar nova senha" in driver.title:
            break



# Pagina criar senha
def preencher_nova_senha(driver, wait, senha):
    """Preenche o campo 'Nova senha'."""
    wait.until(EC.element_to_be_clickable(INPUT_NOVA_SENHA)).click()
    driver.find_element(*INPUT_NOVA_SENHA).send_keys(senha)

def limpar_e_preencher_nova_senha(driver, senha):
    """Limpa e preenche o campo 'Nova senha'."""
    clear_and_type(driver, INPUT_NOVA_SENHA, senha)

def preencher_confirmar_senha(driver, wait, senha):
    """Preenche o campo 'Confirmar nova senha'."""
    wait.until(EC.element_to_be_clickable(INPUT_CONFIRMAR_SENHA)).click()
    driver.find_element(*INPUT_CONFIRMAR_SENHA).send_keys(senha)

def limpar_e_preencher_confirmar_senha(driver, senha):
    """Limpa e preenche o campo 'Confirmar nova senha'."""
    clear_and_type(driver, INPUT_CONFIRMAR_SENHA, senha)


def mostrar_nova_senha(driver):
    """Clica no icone de visibilidade do campo Nova senha."""
    driver.find_element(*BTN_MOSTRAR_NOVA_SENHA).click()

def mostrar_confirmar_senha(driver):
    """Clica no icone de visibilidade do campo Confirmar nova senha."""
    driver.find_element(*BTN_MOSTRAR_CONFIRMAR_SENHA).click()

def clicar_redefinir_senha(driver, wait):
    """Clica no botao 'Redefinir senha'."""
    wait.until(EC.element_to_be_clickable(BTN_REDEFINIR_SENHA)).click()
    time.sleep(3)

def clicar_entrar_apos_redefinir(driver, wait):
    """Clica no botao 'Entrar' apos redefinicao bem-sucedida."""
    wait.until(EC.element_to_be_clickable(BTN_ENTRAR_APOS_REDEFINIR)).click()
    time.sleep(8)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def navegar_email_logs_mobile(driver, wait):
    """Navega ate a pagina de Email Logs no admin."""
    mobile_click_strict(driver, ADMIN_MENU_STORES, timeout=12, retries=4, sleep_between=0.25)
    mobile_click_strict(driver, ADMIN_SUBMENU_EMAIL_LOGS, timeout=12, retries=4, sleep_between=0.25)
    time.sleep(5)

def filtrar_email_logs_mobile(driver, wait, email_destinatario):
    """Aplica filtro de Recipient no grid de Email Logs."""
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_FILTERS)).click()
    wait.until(EC.visibility_of_element_located(ADMIN_INPUT_RECIPIENT))
    campo = driver.find_element(*ADMIN_INPUT_RECIPIENT)
    valor = campo.get_attribute('value')
    if valor != email_destinatario:
        clear_and_type(driver, ADMIN_INPUT_RECIPIENT, email_destinatario)
        driver.find_element(*ADMIN_BTN_APPLY_FILTERS).click()
        time.sleep(5)

def obter_link_redefinicao_mobile(driver, wait):
    """
    Obtenho o link do botão Redefinir senha e acesso a pagina Criar senha diretamente pelo o link
    """
    iframe = wait.until(EC.presence_of_element_located(ADMIN_IFRAME_EMAIL))
    driver.switch_to.frame(iframe)
    link = driver.find_element(*ADMIN_LINK_EMAIL_BODY)
    driver.get(link.get_attribute('href'))

def preencher_nova_senha_mobile(driver, wait, senha):
    """Preenche o campo 'Nova senha'."""
    mobile_click_strict(driver, INPUT_NOVA_SENHA, 12, 4, 0.25)
    driver.find_element(*INPUT_NOVA_SENHA).send_keys(senha)

def preencher_confirmar_senha_mobile(driver, wait, senha):
    """Preenche o campo 'Confirmar nova senha'."""
    mobile_click_strict(driver, INPUT_CONFIRMAR_SENHA, 12, 4, 0.25)
    driver.find_element(*INPUT_CONFIRMAR_SENHA).send_keys(senha)

def limpar_e_preencher_nova_senha_mobile(driver, senha):
    """Limpa e preenche o campo 'Nova senha'."""
    mobile_click_strict(driver, INPUT_NOVA_SENHA, 12, 4, 0.25)
    clear_and_type(driver, INPUT_NOVA_SENHA, senha)

def limpar_e_preencher_confirmar_senha_mobile(driver, senha):
    """Limpa e preenche o campo 'Confirmar nova senha'."""
    mobile_click_strict(driver, INPUT_CONFIRMAR_SENHA, 12, 4, 0.25)
    clear_and_type(driver, INPUT_CONFIRMAR_SENHA, senha)