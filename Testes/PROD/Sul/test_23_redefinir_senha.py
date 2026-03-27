import os
import pytest

from helpers.redefinir_senha import *
from helpers.auth import open_login, submit_username_valid, login_password, clicar_esqueci_senha


# =========================
# Credenciais
# =========================
VALID_USER = "caique.oliveira2@infobase.com.br"

@pytest.mark.sul
def test_23_redefinir_senha_sul(driver, setup_site, wait):
    # 1) Abre login
    open_login(driver)

    # 2) Username válido: abrir senha
    submit_username_valid(driver, VALID_USER, "usuário válido")

    # 3) Senha inválida: erro
    login_password(driver, "SenhaErrada_", "senha inválida", expect_success=False)

    # 4) Clica em "Esqueci minha senha"
    clicar_esqueci_senha(driver, wait)

    # 5) Seleciona SMS
    clicar_sms_modal(driver, wait)

    # 6) Avançar SEM selecionar input (provoca warning)
    clicar_avancar_modal(driver, wait)
    aguardar_alerta_modal(driver, wait)

    # 7) Voltar step + selecionar E-mail
    clicar_voltar_modal(driver, wait)
    clicar_email_modal(driver, wait)

    # 8) Avançar SEM selecionar input (provoca warning)
    clicar_avancar_modal(driver, wait)
    aguardar_alerta_modal(driver, wait)

    # 9) Seleciona o e-mail + avançar step
    selecionar_email_option(driver, wait)
    clicar_avancar_modal(driver, wait)

    # 10) Clica em "Recebi o link"
    clicar_recebi_link(driver, wait)

    # 11) Acessa o painel administrativo
    driver.get(os.getenv("URL_ADMIN"))

    # 12) Login no painel administrativo
    login_admin(driver, wait, os.getenv("USER_ADMIN"), os.getenv("PASSWORD_ADMIN"))

    # 13) Navega até Email Logs + filtra por e-mail + abre o log do primeiro e-mail
    navegar_email_logs(driver, wait)
    filtrar_email_logs(driver, wait, VALID_USER)
    abrir_primeiro_email(driver, wait)

    # 14) Entra no iframe e clica no link de redefinição
    obter_link_redefinicao_do_iframe(driver, wait)

    # 15) Tenta senha fraca primeiro
    preencher_nova_senha(driver, wait, os.getenv("PASSWORD_LOWER"))
    mostrar_nova_senha(driver)
    preencher_confirmar_senha(driver, wait, os.getenv("PASSWORD_LOWER"))
    mostrar_confirmar_senha(driver)

    # 16) Corrige para senha sem maiúscula
    limpar_e_preencher_nova_senha(driver, os.getenv("PASSWORD_WITHOUT_UPPERCASE"))
    limpar_e_preencher_confirmar_senha(driver, os.getenv("PASSWORD_WITHOUT_UPPERCASE"))

    # 17) Corrige para senha correta
    limpar_e_preencher_nova_senha(driver, os.getenv("NEW_PASSWORD"))
    limpar_e_preencher_confirmar_senha(driver, os.getenv("NEW_PASSWORD"))
    time.sleep(1)

    # 18) Clica em Redefinir senha
    clicar_redefinir_senha(driver, wait)

    # 19) Clica em Entrar após redefinição
    clicar_entrar_apos_redefinir(driver, wait)

    # 20) Faz login com a nova senha
    submit_username_valid(driver, VALID_USER,"usuário válido")
    login_password(driver, os.getenv("NEW_PASSWORD"), "senha válida", expect_success=True)