import time
from urllib.parse import urljoin
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from helpers.actions import scroll_to_middle, click_when_clickable

from locators.mapa_de_corte import *
from locators.header import LOGO

def _abrir_e_fechar_modal(wait, locator_click, locator_confirmacao):
    """Clica no corte, espera modal, fecha, espera confirmacao."""
    click_when_clickable(wait, locator_click)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_CLOSE)
    wait.until(EC.presence_of_element_located(locator_confirmacao))

def _clicar_next(wait, vezes):
    """Clica no botao next da modal N vezes, com sleep de 1s entre cada."""
    for _ in range(vezes):
        click_when_clickable(wait, MODAL_NEXT)
        time.sleep(0.5)

def _clicar_prev(wait, vezes):
    """Clica no botao previous da modal N vezes, com sleep de 1s entre cada."""
    for _ in range(vezes):
        click_when_clickable(wait, MODAL_PREV)
        time.sleep(0.5)

def interagir_mapa_bovino_cliques_home(driver, wait):
    """Scroll ate mapa, abre/fecha diversas areas e itens bovinos."""
    # aguarda home e scroll
    wait.until(EC.presence_of_element_located(MAPA_CORTE_LOADED))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)

    # imagem 2, fecha, imagem 11, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_2, BOVINE_AREA_2)
    _abrir_e_fechar_modal(wait, BOVINE_IMG_11, BOVINE_AREA_11)

    # imagem 9, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_9, BOVINE_AREA_9)

    # item 3 da lista, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_03, BOVINE_AREA_3)

    # item 5 da lista, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_05, BOVINE_AREA_5)

    # item 20 da lista, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_20, BOVINE_AREA_20)

def paginar_modal_bovino_e_carrossel_home(driver, wait):
    """Abre img 2, pagina next 18x, prev 2x, carrossel marcas, PUL."""
    click_when_clickable(wait, BOVINE_IMG_2)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    _clicar_next(wait, 18)
    _clicar_prev(wait, 2)

    click_when_clickable(wait, CAROUSEL_BTN_2)
    time.sleep(0.5)
    click_when_clickable(wait, CAROUSEL_BTN_3)
    time.sleep(0.5)
    click_when_clickable(wait, CAROUSEL_BTN_4)
    time.sleep(0.5)

    short_wait = WebDriverWait(driver, 3)

    try:
        click_when_clickable(short_wait, CAROUSEL_MARCA_PUL)
    except TimeoutException:
        click_when_clickable(wait, MOBILE_CAROUSEL_MARCA_PUL)

    time.sleep(5)

def interagir_ver_produtos_modal_bovinos_home(driver, wait):
    """Volta pra home, abre img 20, clica Ver produtos, scroll."""
    click_when_clickable(wait, LOGO)
    wait.until(EC.presence_of_element_located(BOVINE_IMG_20))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)

    # abre img 20, clica Ver produtos
    click_when_clickable(wait, BOVINE_IMG_20)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)


def interagir_mapa_cordeiro_cliques_home(driver, wait):
    """Volta pra home, aba Cordeiro, abre/fecha areas e itens."""
    # volta home, scroll
    click_when_clickable(wait, LOGO)
    wait.until(EC.presence_of_element_located(BOVINE_IMG_20))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)

    # clica aba Cordeiro
    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    # imagem 2 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_2, LAMB_AREA_2)

    # imagem 9 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_9, LAMB_AREA_9)

    # item 3 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_03, LAMB_AREA_3)

    # item 6 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_06, LAMB_AREA_6_CSV)

def paginar_modal_cordeiro_e_marca_home(driver, wait):
    """Abre img 1 cordeiro, pagina next 7x, prev 1x, clica marca."""
    # abre imagem 1 cordeiro
    click_when_clickable(wait, LAMB_IMG_1)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # next 7 vezes
    _clicar_next(wait, 7)

    # prev 1 vez
    _clicar_prev(wait, 1)

    # clica na primeira marca do carrossel
    click_when_clickable(wait, CAROUSEL_FIRST_BRAND)
    time.sleep(3)

def interagir_ver_produtos_modal_cordeiro_home(driver, wait):
    """Volta home, abre Cordeiro item 8, ver produtos"""
    click_when_clickable(wait, LOGO)
    wait.until(EC.presence_of_element_located(BOVINE_IMG_20))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)
    click_when_clickable(wait, ABA_CORDEIRO)
    time.sleep(2)

    # item 8 cordeiro, ver produtos
    click_when_clickable(wait, LAMB_ITEM_08)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)

def abrir_mapa_corte_footer(driver, wait):
    """Clica no link Mapa de Corte no footer e troca de janela."""
    scroll_to_middle(driver, wait, FOOTER_CONTENT)
    click_when_clickable(wait, FOOTER_MAPA_CORTE)
    time.sleep(3)

    # switchToWindow - troca para a nova janela
    janelas = driver.window_handles
    driver.switch_to.window(janelas[-1])

def interagir_mapa_bovino_cliques_pagina(driver, wait):
    """Na pagina '/mapa-de-corte', abre/fecha areas e itens bovinos."""
    # imagem 4, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_4, BOVINE_AREA_4)

    # imagem 14, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_14, BOVINE_AREA_14)

    # item 13, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_13, BOVINE_AREA_13)

    # item 5, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_05, BOVINE_AREA_5)

def paginar_modal_bovino_e_carrossel_pagina(driver, wait):
    """Abre img 2, next 18x, prev 1x, clica marca ativa."""
    # abre imagem 2
    click_when_clickable(wait, BOVINE_IMG_2)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # next 18 vezes
    _clicar_next(wait, 18)

    # prev 1 vez
    _clicar_prev(wait, 1)

    # clica na primeira marca ativa do carrossel
    click_when_clickable(wait, CAROUSEL_FIRST_BRAND_ACTIVE)
    time.sleep(3)

def interagir_ver_produtos_modal_bovinos_pagina(driver, wait):
    """Navega /mapa-de-corte, abre img 21, ver produtos, scroll."""
    wait.until(EC.presence_of_element_located(BOVINE_IMG_21))

    click_when_clickable(wait, BOVINE_IMG_21)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(3)


def interagir_mapa_cordeiro_cliques_pagina(driver, wait):
    """Navega /mapa-de-corte, aba Cordeiro, abre/fecha areas e itens."""
    wait.until(EC.presence_of_element_located(BOVINE_IMG_21))

    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    # imagem 4 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_4, LAMB_AREA_4)

    # imagem 8 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_8, LAMB_AREA_8)

    # item 2 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_02, LAMB_AREA_2)

    # item 9 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_09, LAMB_AREA_9)

def paginar_modal_cordeiro_e_marca_pagina(driver, wait):
    """Abre img 1 cordeiro, next 7x, clica marca."""
    click_when_clickable(wait, LAMB_IMG_1)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # next 7 vezes
    _clicar_next(wait, 7)

    # clica na primeira marca
    click_when_clickable(wait, CAROUSEL_FIRST_BRAND)
    time.sleep(3)

def interagir_ver_produtos_modal_cordeiro_pagina(driver, wait):
    """Navega /mapa-de-corte, aba Cordeiro, img 9, ver produtos."""
    wait.until(EC.presence_of_element_located(BOVINE_IMG_21))

    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    click_when_clickable(wait, LAMB_IMG_9)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def abrir_mapa_corte_footer_mobile(driver, wait):
    """Captura o href do Mapa de Corte e abre diretamente a página."""
    scroll_to_middle(driver, wait, FOOTER_CONTENT)

    elemento = wait.until(EC.presence_of_element_located(FOOTER_MAPA_CORTE))
    href = elemento.get_attribute("href")

    link_mapa_corte = urljoin(driver.current_url, href)

    driver.get(link_mapa_corte)