from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from locators.lp_marcas_logado_deslogado import *
import time

EMAIL = "caique.oliveira@infobase.com.br"
SENHA = "Min@1234"


# ================= UTIL =================

def scroll_into_view(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )
    time.sleep(1)


def click_when_clickable(wait, locator):
    element = wait.until(EC.element_to_be_clickable(locator))
    element.click()
    time.sleep(1)


def interagir_quero_ser_cliente(wait):
    try:
        click_when_clickable(wait, BTN_QUERO_SER_CLIENTE)
        click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)
        print("✔ Modal Quero ser cliente validado")
    except:
        print("⚠ Modal Quero ser cliente não exibido")


def fechar_modal_login(wait):
    try:
        click_when_clickable(wait, BTN_CLOSE_MODAL_LOGIN)
    except:
        pass


# ================= HOME =================

def entrar_alma_lusa_via_home(driver, wait):
    print("→ HOME - Interagindo carrossel marcas")

    item = wait.until(
        EC.presence_of_element_located(BRANDS_CAROUSEL_ITEM(1))
    )
    scroll_into_view(driver, item)

    # Interage seta do carrossel
    try:
        next_btn = wait.until(
            EC.element_to_be_clickable(SLICK_NEXT)
        )
        next_btn.click()
        time.sleep(1)
    except:
        pass

    # Clica Alma Lusa
    click_when_clickable(wait, BRANDS_CAROUSEL_ITEM(1))
    time.sleep(4)


# ================= ALMA LUSA DESLOGADO =================

def fluxo_alma_lusa_deslogado(driver, wait):
    print("→ Digitando 'carne' na busca do header")

    campo = wait.until(
        EC.element_to_be_clickable(SEARCH_INPUT)
    )
    campo.clear()
    campo.send_keys("carne")

    time.sleep(2)

    print("→ Clicando em 'Faça seu login' (header)")

    login_header = wait.until(
        EC.element_to_be_clickable(LOGIN_MENU)
    )
    login_header.click()

    time.sleep(2)
    fechar_modal_login(wait)

    print("→ Alma Lusa DESLOGADO")

    interagir_quero_ser_cliente(wait)

    for texto in ["Sobre", "Diferenciais", "Produto"]:
        try:
            anchor = wait.until(
                EC.element_to_be_clickable(ANCHOR_LINK(texto))
            )
            scroll_into_view(driver, anchor)
            anchor.click()
            time.sleep(2)

            # ✅ Depois de clicar em Diferenciais, interage com o carrossel
            if texto == "Diferenciais":
                print("→ Interagindo com carrossel Diferenciais")

                try:
                    # Seta direita
                    seta_next = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//*[@id='diferenciais']/div/div[1]/button[2]")
                        )
                    )
                    driver.execute_script("arguments[0].click();", seta_next)
                    time.sleep(1)

                    # Seta esquerda
                    seta_prev = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//*[@id='diferenciais']/div/div[1]/button[1]")
                        )
                    )
                    driver.execute_script("arguments[0].click();", seta_prev)
                    time.sleep(1)

                except:
                    print("⚠ Não conseguiu interagir com carrossel Diferenciais")
            if texto == "Produto":
                print("→ Clicando no botão Entrar da seção Produto")

                try:
                    botao_entrar_produto = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//*[@id='produto']//a[normalize-space()='Entrar']")
                        )
                    )

                    driver.execute_script("arguments[0].click();", botao_entrar_produto)

                    wait.until(
                        EC.visibility_of_element_located(USERNAME_INPUT)
                    )

                    time.sleep(2)

                except Exception as e:
                    print("⚠ Não conseguiu clicar no Entrar do Produto:", e)

        except:
            pass


# ================= IR PARA ESTÂNCIA =================

def ir_para_estancia_via_outras_marcas(driver, wait):
    print("→ Indo para Estância via âncora")

    anchor = wait.until(
        EC.element_to_be_clickable(ANCHOR_LINK("Outras Marcas"))
    )
    scroll_into_view(driver, anchor)
    anchor.click()

    card = wait.until(
        EC.element_to_be_clickable(CARD_ESTANCIA_92)
    )
    scroll_into_view(driver, card)

    driver.execute_script("arguments[0].click();", card)
    time.sleep(4)


# ================= ESTÂNCIA DESLOGADO =================
def fluxo_estancia_header(driver, wait):
    print("→ Estância DESLOGADO - Interagindo header completo")
    # 🔹 Busca
    campo = wait.until(
        EC.element_to_be_clickable(SEARCH_INPUT)
    )
    campo.clear()
    campo.send_keys("carne")
    time.sleep(2)
    # 🔹 Login header
    login_header = wait.until(
        EC.element_to_be_clickable(LOGIN_MENU)
    )
    login_header.click()
    time.sleep(2)
    fechar_modal_login(wait)
    # 🔹 Quero ser cliente
    interagir_quero_ser_cliente(wait)


def fluxo_estancia_deslogado(driver, wait):
    # 🔥 CHAMA O HEADER PRIMEIRO
    fluxo_estancia_header(driver, wait)
    print("→ Estância DESLOGADO - Interagindo carrosseis")
    # Âncoras
    for texto in ["Nossa História", "Angus", "Novilho", "Cordeiro"]:
        try:
            anchor = wait.until(
                EC.element_to_be_clickable(ANCHOR_LINK(texto))
            )
            scroll_into_view(driver, anchor)
            anchor.click()
            time.sleep(2)
        except:
            pass
        # -------- CARROSSEL ANGUS --------
    angus = wait.until(
        EC.presence_of_element_located(CARROSSEL_ANGUS)
    )
    scroll_into_view(driver, angus)

    try:
        next_btn = angus.find_element(*SLICK_NEXT_INSIDE)
        next_btn.click()
        time.sleep(1)
    except:
        pass

    # -------- CARROSSEL NOVILHO --------
    novilho = wait.until(
        EC.presence_of_element_located(CARROSSEL_NOVILHO)
    )
    scroll_into_view(driver, novilho)

    try:
        next_btn = novilho.find_element(*SLICK_NEXT_INSIDE)
        next_btn.click()
        time.sleep(1)
    except:
        pass

    # -------- CARROSSEL CORDEIRO --------
    cordeiro = wait.until(
        EC.presence_of_element_located(CARROSSEL_CORDEIRO)
    )
    scroll_into_view(driver, cordeiro)

    try:
        next_btn = cordeiro.find_element(*SLICK_NEXT_INSIDE)
        next_btn.click()
        time.sleep(1)
    except:
        pass

    # Clicar Entrar no último
    try:
        entrar = cordeiro.find_element(
            *BTN_ENTRAR_DENTRO_CARROSSEL
        )
        scroll_into_view(driver, entrar)
        driver.execute_script(
            "arguments[0].click();",
            entrar
        )
        time.sleep(2)
    except:
        print("⚠ Não encontrou botão Entrar no Cordeiro")


# ================= LOGIN =================

from selenium.common.exceptions import TimeoutException


def login_via_estancia(driver, wait):
    email_input = wait.until(
        EC.visibility_of_element_located(USERNAME_INPUT)
    )
    email_input.clear()
    email_input.send_keys(EMAIL)

    click_when_clickable(wait, BTN_AVANCAR)

    senha_input = wait.until(
        EC.visibility_of_element_located(PASSWORD_INPUT)
    )
    senha_input.clear()
    senha_input.send_keys(SENHA)

    click_when_clickable(wait, BTN_AVANCAR)

    time.sleep(5)

    print("✔ Login finalizado")


# ================= NAVEGAR ENTRE MARCAS =================

def navegar_para_marca_via_ancora(driver, wait, slug_marca):
    print(f"→ Navegando para {slug_marca}")

    anchor = wait.until(
        EC.element_to_be_clickable(ANCHOR_LINK("Outras Marcas"))
    )
    scroll_into_view(driver, anchor)
    anchor.click()

    card = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'_{slug_marca}')]//a")
        )
    )

    scroll_into_view(driver, card)
    driver.execute_script("arguments[0].click();", card)
    time.sleep(4)

    if slug_marca == "alma-lusa":
        print("→ Alma Lusa LOGADO - Adicionando azeite")
        botao_add = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="produto"]//form/button')
            )
        )
        scroll_into_view(driver, botao_add)
        driver.execute_script("arguments[0].click();", botao_add)
        print("✔ Azeite adicionado")
        time.sleep(2)


def buscar_e_adicionar(driver, wait, termo):
    print(f"→ Buscando '{termo}' via autocomplete")

    # Fim da função

    def adicionar_produto_pul_carrossel(driver, wait):
        print("→ PUL - Scroll até BOVINOS")

        # Scroll até âncora Bovinos

        anchor_bovinos = wait.until(

            EC.element_to_be_clickable(ANCHOR_LINK("Bovinos"))

        )

        scroll_into_view(driver, anchor_bovinos)

        anchor_bovinos.click()

        time.sleep(2)

        print("→ PUL - Aguardando carrossel carregar")

        # Espera todos os botões do carrossel

        botoes = wait.until(

            EC.presence_of_all_elements_located(

                (By.XPATH, "//section[contains(@class,'bovinos')]//button[contains(.,'Adicionar')]")

            )

        )

        print("→ PUL - Clicando no segundo produto")

        segundo_botao = botoes[1]  # índice 1 = segundo produto

        scroll_into_view(driver, segundo_botao)

        driver.execute_script("arguments[0].click();", segundo_botao)

        print("✔ Produto da PUL adicionado ao minicart")

        time.sleep(2)

    def adicionar_produto_pul_carrossel(driver, wait):
        print("→ PUL - Scroll até BOVINOS")

        # Scroll até âncora Bovinos

        anchor_bovinos = wait.until(

            EC.element_to_be_clickable(ANCHOR_LINK("Bovinos"))

        )

        scroll_into_view(driver, anchor_bovinos)

        anchor_bovinos.click()

        time.sleep(2)

        print("→ PUL - Aguardando carrossel carregar")

        # Espera todos os botões do carrossel

        botoes = wait.until(

            EC.presence_of_all_elements_located(

                (By.XPATH, "//section[contains(@class,'bovinos')]//button[contains(.,'Adicionar')]")

            )

        )

        print("→ PUL - Clicando no segundo produto")

        segundo_botao = botoes[1]  # índice 1 = segundo produto

        scroll_into_view(driver, segundo_botao)

        driver.execute_script("arguments[0].click();", segundo_botao)

        print("✔ Produto da PUL adicionado ao minicart")

        time.sleep(2)

    campo = wait.until(
        EC.element_to_be_clickable(SEARCH_INPUT)
    )
    campo.click()
    campo.clear()
    campo.send_keys(termo)

    # espera o botão da sugestão aparecer
    wait.until(
        EC.visibility_of_element_located(SEARCH_SUGGEST_ADD_2)
    )

    # clica no botão da sugestão
    botao = wait.until(
        EC.element_to_be_clickable(SEARCH_SUGGEST_ADD_2)
    )
    botao.click()

    print("✔ Produto adicionado")


# ================= HEADER GLOBAL =================

def interagir_header(driver, wait):
    print("→ Validando Header")

    campo = wait.until(
        EC.element_to_be_clickable(SEARCH_INPUT)
    )

    campo.click()
    campo.clear()
    campo.send_keys("carne")

    time.sleep(1)

    print("✔ Header interagido")


# ================= SCROLL LENTO =================

def scroll_lento(driver):
    print("→ Scroll lento na página")

    altura = driver.execute_script("return document.body.scrollHeight")

    for i in range(0, altura, 300):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.3)

    print("✔ Scroll finalizado")
