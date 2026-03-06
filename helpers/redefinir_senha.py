import time
from selenium.webdriver.support import expected_conditions as EC
from locators.redefinir_senha import *


# ========================================
# UTILITARIOS
# ========================================

def screenshot(driver, nome="screenshot"):
    """Captura de tela com nome descritivo."""
    timestamp = int(time.time())
    path = f"screenshots/{nome}_{timestamp}.png"
    driver.save_screenshot(path)
    print(f"[SCREENSHOT] {path}")


def sleep(segundos):
    """Aguarda N segundos."""
    time.sleep(segundos)


def clear_and_type(driver, locator, texto):
    """Limpa o campo e digita o texto."""
    campo = driver.find_element(*locator)
    campo.clear()
    campo.send_keys(texto)


# ========================================
# LOGOUT
# ========================================

def ensure_logged_out(driver):
    """
    Garante que o usuario esta deslogado.
    Se botao de logout existir -> clica.
    Se nao existir -> ja esta deslogado.
    """
    try:
        driver.find_element(*BTN_LOGOUT_HEADER).click()
    except Exception:
        pass


# ========================================
# COOKIE BANNER
# ========================================

def aceitar_cookies(driver, wait):
    """Aguarda e aceita o banner de cookies."""
    wait.until(EC.element_to_be_clickable(BTN_ACEITAR_COOKIES)).click()
    wait.until(EC.invisibility_of_element_located(BTN_ACEITAR_COOKIES))


# ========================================
# MODAL DE REGIAO
# ========================================

def selecionar_regiao(driver, wait):
    """Aguarda e clica no botao Outras Regioes."""
    wait.until(EC.element_to_be_clickable(BTN_OUTRAS_REGIOES)).click()
    sleep(5)


# ========================================
# NAVEGACAO - LOGIN
# ========================================

def abrir_login(driver, wait):
    """Clica em 'Faca seu login' no header."""
    wait.until(EC.element_to_be_clickable(BTN_LOGIN_HEADER)).click()


def preencher_email_login(driver, wait, email):
    """Preenche o campo de e-mail/CNPJ e avanca."""
    wait.until(EC.element_to_be_clickable(INPUT_USERNAME)).click()
    driver.find_element(*INPUT_USERNAME).send_keys(email)


def preencher_senha_login(driver, wait, senha):
    """Preenche o campo de senha."""
    wait.until(EC.visibility_of_element_located(INPUT_PASSWORD)).click()
    driver.find_element(*INPUT_PASSWORD).send_keys(senha)


def clicar_avancar_login(driver, wait):
    """Clica no botao Avancar da pagina de login."""
    wait.until(EC.element_to_be_clickable(BTN_AVANCAR_LOGIN)).click()


def aguardar_erro_senha(driver, wait):
    """Aguarda mensagem de erro de senha invalida."""
    wait.until(EC.visibility_of_element_located(MSG_ERRO_SENHA))


# ========================================
# MODAL ESQUECI MINHA SENHA
# ========================================

def clicar_esqueci_senha(driver, wait):
    """Clica no link 'Esqueci minha senha'."""
    wait.until(EC.element_to_be_clickable(LINK_ESQUECI_SENHA)).click()
    sleep(3)


def clicar_sms_modal(driver, wait):
    """Clica no botao SMS da modal de recuperacao."""
    wait.until(EC.element_to_be_clickable(BTN_SMS_MODAL)).click()
    sleep(3)


def clicar_email_modal(driver, wait):
    """Clica no botao E-mail da modal de recuperacao."""
    wait.until(EC.element_to_be_clickable(BTN_EMAIL_MODAL)).click()
    sleep(3)


def clicar_avancar_modal(driver, wait):
    """Clica no botao Avancar da modal."""
    wait.until(EC.element_to_be_clickable(BTN_AVANCAR_MODAL)).click()


def clicar_voltar_modal(driver, wait):
    """Clica no botao Voltar da modal."""
    wait.until(EC.element_to_be_clickable(BTN_VOLTAR_MODAL)).click()
    sleep(2)


def aguardar_alerta_modal(driver, wait):
    """Aguarda o alerta/warning na modal."""
    wait.until(EC.visibility_of_element_located(MSG_ALERTA_MODAL))


def selecionar_email_option(driver, wait):
    """Seleciona a primeira opcao de e-mail na modal."""
    wait.until(EC.element_to_be_clickable(INPUT_EMAIL_OPTION_0)).click()
    sleep(1)


def clicar_recebi_link(driver, wait):
    """Clica no botao 'Recebi o link' na modal de verificacao."""
    wait.until(EC.element_to_be_clickable(BTN_RECEBI_LINK)).click()
    sleep(2)


# ========================================
# ADMIN - LOGIN
# ========================================

def login_admin(driver, wait, usuario, senha):
    """Faz login no painel admin do Magento."""
    wait.until(EC.visibility_of_element_located(ADMIN_INPUT_USERNAME)).click()
    driver.find_element(*ADMIN_INPUT_USERNAME).send_keys(usuario)
    driver.find_element(*ADMIN_INPUT_PASSWORD).send_keys(senha)
    driver.find_element(*ADMIN_BTN_ENTRAR).click()
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_FECHAR_MODAL))
    sleep(15)
    driver.find_element(*ADMIN_BTN_FECHAR_MODAL).click()


# ========================================
# ADMIN - NAVEGACAO ATE EMAIL LOGS
# ========================================

def navegar_email_logs(driver, wait):
    """Navega ate a pagina de Email Logs no admin."""
    wait.until(EC.element_to_be_clickable(ADMIN_MENU_STORES)).click()
    sleep(5)
    wait.until(EC.element_to_be_clickable(ADMIN_SUBMENU_EMAIL_LOGS)).click()
    sleep(25)


def filtrar_email_logs(driver, wait, email_destinatario):
    """Aplica filtro de Recipient no grid de Email Logs."""
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_FILTERS)).click()
    wait.until(EC.visibility_of_element_located(ADMIN_INPUT_RECIPIENT))
    clear_and_type(driver, ADMIN_INPUT_RECIPIENT, email_destinatario)
    driver.find_element(*ADMIN_BTN_APPLY_FILTERS).click()
    sleep(25)


def abrir_primeiro_email(driver, wait):
    """Abre o primeiro resultado de e-mail via botao Select > View."""
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_SELECT_FIRST)).click()
    wait.until(EC.element_to_be_clickable(ADMIN_BTN_VIEW)).click()
    sleep(3)


def obter_link_redefinicao_do_iframe(driver, wait):
    """
    Entra no iframe do template de email, clica no link de redefinicao
    e muda para a nova janela 'Criar nova senha'.
    """
    iframe = wait.until(EC.presence_of_element_located(ADMIN_IFRAME_EMAIL))
    driver.switch_to.frame(iframe)
    driver.find_element(*ADMIN_LINK_EMAIL_BODY).click()
    sleep(5)
    driver.switch_to.default_content()

    # Muda para a janela "Criar nova senha"
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "Criar nova senha" in driver.title:
            break


# ========================================
# PAGINA CRIAR NOVA SENHA
# ========================================

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
    sleep(3)


def clicar_entrar_apos_redefinir(driver, wait):
    """Clica no botao 'Entrar' apos redefinicao bem-sucedida."""
    wait.until(EC.element_to_be_clickable(BTN_ENTRAR_APOS_REDEFINIR)).click()
    sleep(8)


# ========================================
# LOGIN POS-REDEFINICAO
# ========================================

def login_com_nova_senha(driver, wait, email, senha):
    """Faz login completo com a nova senha apos redefinicao."""
    preencher_email_login(driver, wait, email)
    screenshot(driver, "login_nova_senha_email")
    clicar_avancar_login(driver, wait)
    preencher_senha_login(driver, wait, senha)
    # Mostrar senha para validacao visual
    wait.until(EC.element_to_be_clickable(BTN_MOSTRAR_SENHA)).click()
    screenshot(driver, "login_nova_senha_visivel")
    clicar_avancar_login(driver, wait)
    sleep(8)
