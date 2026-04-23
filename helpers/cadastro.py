import os
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from helpers.dropdown import mobile_open_quero_ser_cliente_from_dropdown
from helpers.actions import click_when_clickable
from helpers.region import cnpj_por_regiao

from locators.cadastro import *
from locators.header import BTN_QUERO_SER_CLIENTE


def iniciar_fluxo_cadastro(driver, wait, regiao):
    "Iniciar cadastro"
    cnpj = cnpj_por_regiao(regiao)
    btn_home = wait.until(EC.element_to_be_clickable(BTN_QUERO_SER_CLIENTE))
    driver.execute_script("arguments[0].click();", btn_home)

    campo = wait.until(EC.visibility_of_element_located(INPUT_CNPJ))
    campo.clear()
    campo.send_keys(cnpj)
    campo.send_keys(Keys.TAB)

    btn = wait.until(EC.element_to_be_clickable(BTN_INICIAR_CADASTRO))
    driver.execute_script("arguments[0].click();", btn)

    wait.until(lambda d: "customer/account/create" in d.current_url.lower())
    wait.until(EC.visibility_of_element_located(INPUT_BUSINESS_NAME))


def continuar(driver, wait):
    "Função padrão do botão Continuar"
    btn = wait.until(EC.element_to_be_clickable(BTN_CONTINUAR))
    driver.execute_script("arguments[0].click();", btn)


def preencher_dados_empresa(driver, wait, email_cliente):
    "Preencher dados no step Dados Gerais"
    wait.until(EC.visibility_of_element_located(INPUT_BUSINESS_NAME)).send_keys("Teste Automatizado")
    wait.until(EC.visibility_of_element_located(INPUT_NOME_CONTATO)).send_keys("Teste Automatizado")
    campo_email = wait.until(EC.visibility_of_element_located(INPUT_EMAIL))
    campo_email.clear()
    campo_email.send_keys(email_cliente)
    wait.until(EC.visibility_of_element_located(INPUT_CELULAR)).send_keys("11999999999")
    wait.until(EC.visibility_of_element_located(INPUT_TELEFONE)).send_keys("1133333333")

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(SWITCH_TELEFONE_PRINCIPAL))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECKBOX_TELEFONE_WHATSAPP))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(SWITCH_CELULAR_PRINCIPAL))
    )

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECKBOX_CELULAR_WHATSAPP))
    )

    wait.until(EC.visibility_of_element_located(INPUT_PASSWORD)).send_keys("Min@1234")
    wait.until(EC.visibility_of_element_located(INPUT_PASSWORD_CONFIRM)).send_keys("Min@1234")

    Select(wait.until(EC.visibility_of_element_located(SELECT_TIPOLOGIA))).select_by_index(1)

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECKBOX_TERMOS))
    )

    continuar(driver, wait)

    wait.until(EC.visibility_of_element_located(INPUT_TOKEN_SMS))


def validar_token_invalido(driver, wait):
    "Inserir token inválido"
    campo = wait.until(EC.visibility_of_element_located(INPUT_TOKEN_SMS))
    campo.clear()
    campo.send_keys("1234")

    continuar(driver, wait)

    wait.until(EC.visibility_of_element_located(MSG_TOKEN_INVALIDO))


def validar_token_valido(driver, wait):
    "Inserir token válido e avançar para próxima etapa"
    campo = wait.until(EC.visibility_of_element_located(INPUT_TOKEN_SMS))
    token = (os.getenv("TOKEN") or "").strip()
    if not token:
        raise RuntimeError("Defina TOKEN no .env.")
    campo.send_keys(token)

    # Validação → Fotos
    continuar(driver, wait)

    # Fotos → Criar Conta
    continuar(driver, wait)

    # Revisão
    wait.until(EC.presence_of_element_located(BTN_CRIAR_CONTA))


def finalizar_cadastro(driver, wait):
    "Finalizar cadastro step Revisão"
    # Scroll até o final da página
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Checkbox Marcar todas
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECK_MARCAR_TODAS))
    )

    # Checkbox WhatsApp
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECK_WHATSAPP))
    )

    # Checkbox SMS
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECK_SMS))
    )

    # Checkbox E-mail
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.presence_of_element_located(CHECK_EMAIL))
    )

    # Espera botão Criar Conta ficar clicável
    botao_criar = wait.until(
        EC.element_to_be_clickable(BTN_CRIAR_CONTA)
    )

    driver.execute_script("arguments[0].click();", botao_criar)

    # Espera modal de sucesso
    wait.until(EC.visibility_of_element_located(MODAL_SUCESSO))

    # Clique no botão de copiar e-mail
    click_when_clickable(wait, BTN_COPIAR_EMAIL)
    time.sleep(1)

    # Clique no botão Ir para home
    click_when_clickable(wait, BTN_IR_HOME)
    time.sleep(3)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def iniciar_fluxo_cadastro_mobile(driver, wait, regiao):
    "Iniciar cadastro"
    cnpj = cnpj_por_regiao(regiao)
    mobile_open_quero_ser_cliente_from_dropdown(driver)

    campo = wait.until(EC.visibility_of_element_located(INPUT_CNPJ))
    campo.clear()
    campo.send_keys(cnpj)
    campo.send_keys(Keys.TAB)

    btn = wait.until(EC.element_to_be_clickable(BTN_INICIAR_CADASTRO))
    driver.execute_script("arguments[0].click();", btn)

    wait.until(lambda d: "customer/account/create" in d.current_url.lower())
    wait.until(EC.visibility_of_element_located(INPUT_BUSINESS_NAME))
