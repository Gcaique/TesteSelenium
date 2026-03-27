from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from helpers.actions import click_when_clickable, safe_click_loc, mobile_click_strict
from helpers.waiters import visible
from helpers.dropdown import mobile_open_login_dropdown, mobile_open_login_modal_from_dropdown,mobile_open_quero_ser_cliente_from_dropdown

from locators.lp_deslogado_logado import *
from locators.home import BRANDS_CAROUSEL_ITEM, MOBILE_BRANDS_CAROUSEL_ITEM
from locators.header import *
import time


def scroll_into_view(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )
    time.sleep(1)

def interagir_quero_ser_cliente(wait):
    click_when_clickable(wait, BTN_QUERO_SER_CLIENTE)
    click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)

def fechar_modal_login(wait):
    click_when_clickable(wait, LOGIN_MENU)

def entrar_alma_lusa_via_home(driver, wait):
    item = wait.until(EC.presence_of_element_located(BRANDS_CAROUSEL_ITEM(1)))
    scroll_into_view(driver, item)
    click_when_clickable(wait, BRANDS_CAROUSEL_ITEM(1))
    time.sleep(4)

def fluxo_alma_lusa_deslogado(driver, wait):
    """Fluxo Alma Lusa deslogado"""
    campo = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
    campo.clear()
    campo.send_keys("carne")
    visible(driver, SEE_ALL_LINK)

    login_header = wait.until(EC.element_to_be_clickable(LOGIN_MENU))
    login_header.click()


    time.sleep(2)
    fechar_modal_login(wait)
    interagir_quero_ser_cliente(wait)

    for texto in ["Sobre", "Diferenciais", "Produto"]:
        anchor = wait.until(EC.element_to_be_clickable(ANCHOR_LINK(texto)))
        scroll_into_view(driver, anchor)
        driver.execute_script("arguments[0].click();", anchor)
        time.sleep(2)

        if texto == "Diferenciais":
            seta_next = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='diferenciais']/div/div[1]/button[2]")
                )
            )
            driver.execute_script("arguments[0].click();", seta_next)
            time.sleep(1)

            seta_prev = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='diferenciais']/div/div[1]/button[1]")
                )
            )
            driver.execute_script("arguments[0].click();", seta_prev)
            time.sleep(1)

        if texto == "Produto":
            botao_entrar_produto = wait.until(
                EC.element_to_be_clickable(
                    BTN_ENTRAR
                )
            )
            driver.execute_script("arguments[0].click();", botao_entrar_produto)

            wait.until(EC.visibility_of_element_located(USERNAME_INPUT))
            time.sleep(2)

def ir_para_estancia_via_outras_marcas(driver, wait):
    """Acessando Estância 92 via Outras marcas"""
    anchor = wait.until(EC.element_to_be_clickable(ANCHOR_LINK("Outras Marcas")))
    scroll_into_view(driver, anchor)
    anchor.click()

    card = wait.until(
        EC.element_to_be_clickable(CARD_ESTANCIA_92)
    )
    scroll_into_view(driver, card)

    driver.execute_script("arguments[0].click();", card)
    time.sleep(4)

def fluxo_estancia_header(driver, wait):
    """Fluxo header outras marcas deslogado"""
    campo = wait.until(
        EC.element_to_be_clickable(SEARCH_INPUT)
    )
    campo.clear()
    campo.send_keys("carne")
    visible(driver, SEE_ALL_LINK)

    login_header = wait.until(EC.element_to_be_clickable(LOGIN_MENU))
    login_header.click()
    time.sleep(2)

    fechar_modal_login(wait)
    interagir_quero_ser_cliente(wait)

def fluxo_estancia_deslogado(driver, wait):
    """Fluxo Estância 92 deslogado"""
    fluxo_estancia_header(driver, wait)

    for texto in ["Nossa História", "Angus", "Novilho", "Cordeiro"]:
        anchor = wait.until(
            EC.element_to_be_clickable(ANCHOR_LINK(texto))
        )
        scroll_into_view(driver, anchor)
        driver.execute_script("arguments[0].click();", anchor)
        time.sleep(2)

    angus = wait.until(
        EC.visibility_of_element_located(CARROSSEL_ANGUS)
    )
    scroll_into_view(driver, angus)

    next_btn = angus.find_element(*SLICK_NEXT_INSIDE)
    driver.execute_script("arguments[0].click();", next_btn)
    time.sleep(1)

    novilho = wait.until(
        EC.visibility_of_element_located(CARROSSEL_NOVILHO)
    )
    scroll_into_view(driver, novilho)

    next_btn = novilho.find_element(*SLICK_NEXT_INSIDE)
    driver.execute_script("arguments[0].click();", next_btn)
    time.sleep(1)

    cordeiro = wait.until(
        EC.visibility_of_element_located(CARROSSEL_CORDEIRO)
    )
    scroll_into_view(driver, cordeiro)

    next_btn = cordeiro.find_element(*SLICK_NEXT_INSIDE)
    driver.execute_script("arguments[0].click();", next_btn)
    time.sleep(1)

    entrar = cordeiro.find_element(*BTN_ENTRAR_DENTRO_CARROSSEL)
    scroll_into_view(driver, entrar)
    driver.execute_script("arguments[0].click();", entrar)
    time.sleep(2)

def entrar_alma_lusa_via_home_mobile(driver, wait):
    item = wait.until(EC.presence_of_element_located(MOBILE_BRANDS_CAROUSEL_ITEM(1)))
    scroll_into_view(driver, item)
    click_when_clickable(wait, MOBILE_BRANDS_CAROUSEL_ITEM(1))
    time.sleep(4)

def navegar_para_marca_via_ancora(driver, wait, slug_marca):
    """Navegar nas LPs de Marcas"""
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
        botao_add = wait.until(
            EC.element_to_be_clickable(
                BTN_ADICIONAR_ALMA_LUSA
            )
        )
        scroll_into_view(driver, botao_add)
        driver.execute_script("arguments[0].click();", botao_add)
        time.sleep(2)

def buscar_e_add_produto_marca(driver, wait, termo, marca):
    """Efetuar uma busca e adicionar um item nas marcas selecionadas"""
    if marca not in {"alma-lusa", "pul"}:
        return

    campo = wait.until(
        EC.element_to_be_clickable(SEARCH_INPUT)
    )
    campo.click()
    campo.clear()
    campo.send_keys(termo)

    wait.until(
        EC.visibility_of_element_located(SEE_ALL_LINK)
    )

    safe_click_loc(driver, wait, LOGIN_NAME_CONTAINER, 10)
    time.sleep(0.5)
    safe_click_loc(driver, wait, LOGIN_NAME_CONTAINER, 10)

def scroll_lento(driver):
    """Scroll lento"""
    altura = driver.execute_script("return document.body.scrollHeight")

    for i in range(0, altura, 300):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.3)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------

def scroll_ate_elemento_visivel(driver, locator, max_scrolls=8):
    for _ in range(max_scrolls):
        elementos = driver.find_elements(*locator)
        if elementos and elementos[0].is_displayed():
            return elementos[0]

        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)

    raise Exception(f"Elemento não encontrado após scroll: {locator}")

def fluxo_alma_lusa_deslogado_mobile(driver, wait):
    """Fluxo Alma Lusa deslogado mobile"""
    campo = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
    campo.clear()
    campo.send_keys("carne")
    visible(driver, SEE_ALL_LINK)
    time.sleep(2)

    mobile_open_login_modal_from_dropdown(driver, 12)
    time.sleep(2)

    fechar_modal_login(wait)
    mobile_open_quero_ser_cliente_from_dropdown(driver, 12)
    click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)

    mobile_click_strict(driver, MOBILE_BTN_CONHECA_MAIS, 10, 4, 0.25)
    time.sleep(2)

    secao_sobre = scroll_ate_elemento_visivel(driver, MOBILE_SECAO_SOBRE)
    scroll_into_view(driver, secao_sobre)
    time.sleep(2)

    secao_diferenciais = scroll_ate_elemento_visivel(driver, MOBILE_SECAO_DIFERENCIAIS)
    scroll_into_view(driver, secao_diferenciais)
    time.sleep(2)

    dots_next = wait.until(EC.element_to_be_clickable(MOBILE_DOTS_CARROSSEL(2)))
    driver.execute_script("arguments[0].click();", dots_next)
    time.sleep(1)

    dots_prev = wait.until(EC.element_to_be_clickable(MOBILE_DOTS_CARROSSEL(1)))
    driver.execute_script("arguments[0].click();", dots_prev)
    time.sleep(1)

    click_when_clickable(wait, MOBILE_BTN_COMPRE_AGORA_2)
    time.sleep(2)

    mobile_click_strict(driver, BTN_ENTRAR, 12, 4, 0.25)

    wait.until(EC.visibility_of_element_located(MOBILE_LOGIN_ACESSO))
    time.sleep(2)

def ir_para_estancia_via_outras_marcas_mobile(driver, wait):
    """Acessando Estância 92 via Outras marcas"""
    card = wait.until(EC.element_to_be_clickable(CARD_ESTANCIA_92))
    scroll_into_view(driver, card)

    driver.execute_script("arguments[0].click();", card)
    time.sleep(4)

def fluxo_estancia_deslogado_mobile(driver, wait):
    """Fluxo Estância 92 deslogado mobile"""
    campo = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
    campo.clear()
    campo.send_keys("carne")
    visible(driver, SEE_ALL_LINK)
    time.sleep(2)

    mobile_open_login_modal_from_dropdown(driver, 12)
    time.sleep(2)

    fechar_modal_login(wait)
    mobile_open_quero_ser_cliente_from_dropdown(driver, 12)
    click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)

    nossa_historia = scroll_ate_elemento_visivel(driver, MOBILE_SECAO_NOSSA_HISTORIA)
    scroll_into_view(driver, nossa_historia)
    time.sleep(2)

    angus = scroll_ate_elemento_visivel(driver, CARROSSEL_ANGUS)
    scroll_into_view(driver, angus)
    time.sleep(1)

    novilho = scroll_ate_elemento_visivel(driver, CARROSSEL_NOVILHO)
    scroll_into_view(driver, novilho)
    time.sleep(1)

    cordeiro = scroll_ate_elemento_visivel(driver, CARROSSEL_CORDEIRO)
    scroll_into_view(driver, cordeiro)
    time.sleep(1)

    entrar = cordeiro.find_element(*BTN_ENTRAR_DENTRO_CARROSSEL)
    scroll_into_view(driver, entrar)
    driver.execute_script("arguments[0].click();", entrar)
    time.sleep(2)

def navegar_para_marca_mobile(driver, wait, slug_marca):
    """Navegar nas LPs de Marcas no mobile"""

    card = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'_{slug_marca}')]//a")
        )
    )
    scroll_into_view(driver, card)
    driver.execute_script("arguments[0].click();", card)
    time.sleep(4)

    if slug_marca == "alma-lusa":
        botao_add = wait.until(
            EC.element_to_be_clickable(
                BTN_ADICIONAR_ALMA_LUSA
            )
        )
        scroll_into_view(driver, botao_add)
        driver.execute_script("arguments[0].click();", botao_add)
        time.sleep(2)