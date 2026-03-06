from helpers.redefinir_senha import *

def test_10_redefinir_senha(driver, setup_site, wait):

    email = "caique.oliveira@infobase.com.br"
    senha_errada = "min@1234"
    senha_fraca = "min123"
    senha_sem_maiuscula = "min@1234"
    senha_nova = "Min@1234"
    admin_user = "caique.oliveira"
    admin_pass = "c357951"
    url_admin = "https://mcstaging.meuminerva.com/adm_Min138/admin"

    # 1️⃣ Abre login
    abrir_login(driver, wait)

    # 2️⃣ Preenche o e-mail
    preencher_email_login(driver, wait, email)

    # 3️⃣ Clica em avançar
    clicar_avancar_login(driver, wait)

    # 4️⃣ Preenche senha ERRADA
    preencher_senha_login(driver, wait, senha_errada)

    # 5️⃣ Clica Avançar (para disparar erro)
    clicar_avancar_login(driver, wait)

    # 6️⃣ Aguarda mensagem de erro de senha inválida
    aguardar_erro_senha(driver, wait)

    # 7️⃣ Clica em "Esqueci minha senha"
    clicar_esqueci_senha(driver, wait)

    # 8️⃣ Clica em SMS (teste de erro)
    clicar_sms_modal(driver, wait)

    # 9️⃣ Clica Avançar SEM selecionar input (provoca warning)
    clicar_avancar_modal(driver, wait)

    # 🔟 Aguarda alerta de warning na modal
    aguardar_alerta_modal(driver, wait)

    # 1️⃣1️⃣ Clica Voltar
    clicar_voltar_modal(driver, wait)

    # 1️⃣2️⃣ Clica em E-mail (agora segue o fluxo correto)
    clicar_email_modal(driver, wait)

    # 1️⃣3️⃣ Avança modal (sem selecionar — provoca warning)
    clicar_avancar_modal(driver, wait)

    # 1️⃣4️⃣ Aguarda alerta na modal
    aguardar_alerta_modal(driver, wait)

    # 1️⃣5️⃣ Seleciona o e-mail
    selecionar_email_option(driver, wait)

    # 1️⃣6️⃣ Avança novamente
    clicar_avancar_modal(driver, wait)

    # 1️⃣7️⃣ Clica em "Recebi o link"
    clicar_recebi_link(driver, wait)

    # ==========================================
    # ADMIN MAGENTO - Busca link de redefinição
    # ==========================================

    # 1️⃣8️⃣ Navega para o Admin
    driver.get(url_admin)

    # 1️⃣9️⃣ Login no Admin
    login_admin(driver, wait, admin_user, admin_pass)

    # 2️⃣0️⃣ Navega até Email Logs
    navegar_email_logs(driver, wait)

    # 2️⃣1️⃣ Filtra por e-mail
    filtrar_email_logs(driver, wait, email)

    # 2️⃣2️⃣ Abre o primeiro e-mail
    abrir_primeiro_email(driver, wait)

    # 2️⃣3️⃣ Entra no iframe e clica no link de redefinição
    obter_link_redefinicao_do_iframe(driver, wait)

    # ==========================================
    # CRIAR NOVA SENHA (com validações)
    # ==========================================

    # 2️⃣4️⃣ Tenta senha fraca primeiro
    preencher_nova_senha(driver, wait, senha_fraca)
    mostrar_nova_senha(driver)
    preencher_confirmar_senha(driver, wait, senha_fraca)
    mostrar_confirmar_senha(driver)

    # 2️⃣5️⃣ Corrige para senha sem maiúscula
    limpar_e_preencher_nova_senha(driver, senha_sem_maiuscula)
    limpar_e_preencher_confirmar_senha(driver, senha_sem_maiuscula)

    # 2️⃣6️⃣ Corrige para senha correta
    limpar_e_preencher_nova_senha(driver, senha_nova)
    limpar_e_preencher_confirmar_senha(driver, senha_nova)
    sleep(1)

    # 2️⃣7️⃣ Clica em Redefinir senha
    clicar_redefinir_senha(driver, wait)

    # 2️⃣8️⃣ Clica em Entrar após redefinição
    clicar_entrar_apos_redefinir(driver, wait)

    # ==========================================
    # LOGIN COM NOVA SENHA
    # ==========================================

    # 2️⃣9️⃣ Faz login com a nova senha
    login_com_nova_senha(driver, wait, email, senha_nova)