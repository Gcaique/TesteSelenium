import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from helpers.actions import scroll_to_middle, click_when_clickable
from locators.mapa_de_corte import *


# ── Login (CSV 12-23) ─────────────────────────────────────────────
def fazer_login(driver, wait):
    """CSV 12-23: Faz login com email e senha."""
    click_when_clickable(wait, FACA_SEU_LOGIN)
    click_when_clickable(wait, INPUT_EMAIL)
    el_email = wait.until(EC.presence_of_element_located(INPUT_EMAIL))
    el_email.clear()
    el_email.send_keys("hub.teste2-bruno-popup@minervafoods.com")
    click_when_clickable(wait, BTN_AVANCAR)
    wait.until(EC.presence_of_element_located(INPUT_SENHA))
    click_when_clickable(wait, INPUT_SENHA)
    el_senha = wait.until(EC.presence_of_element_located(INPUT_SENHA))
    el_senha.clear()
    el_senha.send_keys("Min@1234")
    click_when_clickable(wait, BTN_AVANCAR)
    time.sleep(8)


# ── Roleta de cupons (CSV 25-28) ─────────────────────────────────
def fechar_roleta_cupons(driver, wait):
    """CSV 25-27: Fecha a roleta de cupons (pode nao aparecer)."""
    try:
        short_wait = WebDriverWait(driver, 10)
        short_wait.until(EC.element_to_be_clickable(SPIN_CLOSE_BTN))
        click_when_clickable(short_wait, SPIN_CLOSE_BTN)
        time.sleep(2)
    except TimeoutException:
        pass


# ── Helper: abre imagem/item, espera modal, fecha, confirma ──────
def _abrir_e_fechar_modal(wait, locator_click, locator_confirmacao):
    """Clica no corte, espera modal, fecha, espera confirmacao."""
    click_when_clickable(wait, locator_click)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_CLOSE)
    wait.until(EC.presence_of_element_located(locator_confirmacao))


# ── Helper: clica next N vezes ────────────────────────────────────
def _clicar_next(wait, vezes):
    """Clica no botao next da modal N vezes, com sleep de 1s entre cada."""
    for _ in range(vezes):
        click_when_clickable(wait, MODAL_NEXT)
        time.sleep(1)


# ── Helper: clica prev N vezes ────────────────────────────────────
def _clicar_prev(wait, vezes):
    """Clica no botao previous da modal N vezes, com sleep de 1s entre cada."""
    for _ in range(vezes):
        click_when_clickable(wait, MODAL_PREV)
        time.sleep(1)


# ── Mapa bovino - cliques rapidos (CSV 29-67) ────────────────────
def interagir_mapa_bovino_cliques(driver, wait):
    """CSV 29-67: Scroll ate mapa, abre/fecha diversas areas e itens bovinos."""
    # CSV 29-30: aguarda home e scroll
    wait.until(EC.presence_of_element_located(MAPA_CORTE_LOADED))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)

    # CSV 32-37: imagem 2, fecha, imagem 11, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_2, BOVINE_AREA_2)
    _abrir_e_fechar_modal(wait, BOVINE_IMG_11, BOVINE_AREA_11)

    # CSV 44-49: imagem 9, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_9, BOVINE_AREA_9)

    # CSV 50-55: item 3 da lista, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_03, BOVINE_AREA_3)

    # CSV 56-61: item 5 da lista, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_05, BOVINE_AREA_5)

    # CSV 62-67: item 20 da lista, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_20, BOVINE_AREA_20)


# ── Mapa bovino - paginacao e carrossel (CSV 68-142) ──────────────
def paginar_modal_bovino_e_carrossel(driver, wait):
    """CSV 68-142: Abre img 2, pagina next 18x, prev 2x, carrossel marcas, PUL."""
    # CSV 68-69: abre imagem 2 novamente
    click_when_clickable(wait, BOVINE_IMG_2)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # CSV 71-124: next 18 vezes
    _clicar_next(wait, 18)

    # CSV 125-130: prev 2 vezes
    _clicar_prev(wait, 2)

    # CSV 131-139: carrossel de marcas btn 2, 3, 4
    click_when_clickable(wait, CAROUSEL_BTN_2)
    time.sleep(1)
    click_when_clickable(wait, CAROUSEL_BTN_3)
    time.sleep(1)
    click_when_clickable(wait, CAROUSEL_BTN_4)
    time.sleep(1)

    # CSV 140-141: clica na marca PUL
    click_when_clickable(wait, CAROUSEL_MARCA_PUL)
    time.sleep(5)


# ── Volta pra home, abre img 20, ver produtos (CSV 143-156) ──────
def ver_produtos_bovino_20(driver, wait):
    """CSV 143-156: Volta pra home, abre img 20, clica Ver produtos, scroll."""
    click_when_clickable(wait, LOGO_HEADER)
    wait.until(EC.presence_of_element_located(BOVINE_IMG_20))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)

    # CSV 147-150: abre img 20, clica Ver produtos
    click_when_clickable(wait, BOVINE_IMG_20)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)

    # CSV 153-156: scroll ate item 5 e item 9
    scroll_to_middle(driver, wait, PRODUCT_ITEM_5)
    scroll_to_middle(driver, wait, PRODUCT_ITEM_9)


# ── Aba Cordeiro - cliques rapidos (CSV 157-187) ─────────────────
def interagir_mapa_cordeiro_cliques(driver, wait):
    """CSV 157-187: Volta pra home, aba Cordeiro, abre/fecha areas e itens."""
    # CSV 157-160: volta home, scroll
    click_when_clickable(wait, LOGO_HEADER)
    wait.until(EC.presence_of_element_located(BOVINE_IMG_20))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)

    # CSV 161-162: clica aba Cordeiro
    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    # CSV 164-169: imagem 2 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_2, LAMB_AREA_2)

    # CSV 170-175: imagem 9 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_9, LAMB_AREA_9)

    # CSV 176-181: item 3 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_03, LAMB_AREA_3)

    # CSV 182-187: item 6 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_06, LAMB_AREA_6_CSV)


# ── Cordeiro - paginacao e marca (CSV 188-217) ────────────────────
def paginar_modal_cordeiro_e_marca(driver, wait):
    """CSV 188-217: Abre img 1 cordeiro, pagina next 7x, prev 1x, clica marca."""
    # CSV 188-189: abre imagem 1 cordeiro
    click_when_clickable(wait, LAMB_IMG_1)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # CSV 191-208: next 7 vezes
    _clicar_next(wait, 7)

    # CSV 212-214: prev 1 vez
    _clicar_prev(wait, 1)

    # CSV 215-216: clica na primeira marca do carrossel
    click_when_clickable(wait, CAROUSEL_FIRST_BRAND)
    time.sleep(5)


# ── Logout (CSV 218-238) ─────────────────────────────────────────
def fazer_logout(driver, wait):
    """CSV 218-238: Volta home, abre Cordeiro item 8, ver produtos, logout, footer."""
    # CSV 218-224: volta home, aba cordeiro
    click_when_clickable(wait, LOGO_HEADER)
    wait.until(EC.presence_of_element_located(BOVINE_IMG_20))
    scroll_to_middle(driver, wait, MAPA_CORTE_SECTION)
    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    # CSV 225-228: item 8 cordeiro, ver produtos
    click_when_clickable(wait, LAMB_ITEM_08)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)

    # CSV 231-234: menu usuario, sair
    click_when_clickable(wait, MENU_USUARIO)
    wait.until(EC.element_to_be_clickable(BTN_SAIR))
    click_when_clickable(wait, BTN_SAIR)

    # CSV 235-238: aguarda home deslogada, scroll footer
    wait.until(EC.presence_of_element_located(MAPA_CORTE_LOADED))
    scroll_to_middle(driver, wait, FOOTER_CONTENT)


# ── Footer: Mapa de Corte nova janela (CSV 239-241) ──────────────
def abrir_mapa_corte_footer(driver, wait):
    """CSV 239-241: Clica no link Mapa de Corte no footer e troca de janela."""
    click_when_clickable(wait, FOOTER_MAPA_CORTE)
    time.sleep(5)
    # CSV 241: switchToWindow - troca para a nova janela
    janelas = driver.window_handles
    driver.switch_to.window(janelas[-1])


# ── Pagina dedicada bovino - cliques (CSV 243-266) ───────────────
def interagir_mapa_corte_pagina_bovino(driver, wait):
    """CSV 243-266: Na pagina /mapa-de-corte, abre/fecha areas e itens bovinos."""
    # CSV 243-248: imagem 4, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_4, BOVINE_AREA_4)

    # CSV 249-254: imagem 14, fecha
    _abrir_e_fechar_modal(wait, BOVINE_IMG_14, BOVINE_AREA_14)

    # CSV 255-260: item 13, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_13, BOVINE_AREA_13)

    # CSV 261-266: item 5, fecha
    _abrir_e_fechar_modal(wait, BOVINE_ITEM_05, BOVINE_AREA_5)


# ── Pagina dedicada bovino - paginacao e marca (CSV 267-329) ─────
def paginar_pagina_bovino_e_marca(driver, wait):
    """CSV 267-329: Abre img 2, next 18x, prev 1x, clica marca ativa."""
    # CSV 267-268: abre imagem 2
    click_when_clickable(wait, BOVINE_IMG_2)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # CSV 270-323: next 18 vezes
    _clicar_next(wait, 18)

    # CSV 324-326: prev 1 vez
    _clicar_prev(wait, 1)

    # CSV 327-328: clica na primeira marca ativa do carrossel
    click_when_clickable(wait, CAROUSEL_FIRST_BRAND_ACTIVE)
    time.sleep(5)


# ── Pagina dedicada - ver produtos bovino 21 (CSV 330-342) ───────
def ver_produtos_pagina_bovino_21(driver, wait):
    """CSV 330-342: Navega /mapa-de-corte, abre img 21, ver produtos, scroll."""
    driver.get("https://meuminerva.com/mapa-de-corte")
    wait.until(EC.presence_of_element_located(BOVINE_IMG_21))

    click_when_clickable(wait, BOVINE_IMG_21)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)

    scroll_to_middle(driver, wait, PRODUCT_ITEM_5)
    scroll_to_middle(driver, wait, PRODUCT_ITEM_9)


# ── Pagina dedicada cordeiro - cliques (CSV 343-372) ─────────────
def interagir_mapa_corte_pagina_cordeiro(driver, wait):
    """CSV 343-372: Navega /mapa-de-corte, aba Cordeiro, abre/fecha areas e itens."""
    driver.get("https://meuminerva.com/mapa-de-corte")
    wait.until(EC.presence_of_element_located(BOVINE_IMG_21))

    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    # CSV 349-354: imagem 4 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_4, LAMB_AREA_4)

    # CSV 355-360: imagem 8 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_IMG_8, LAMB_AREA_8)

    # CSV 361-366: item 2 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_02, LAMB_AREA_2)

    # CSV 367-372: item 9 cordeiro, fecha
    _abrir_e_fechar_modal(wait, LAMB_ITEM_09, LAMB_AREA_9)


# ── Pagina dedicada cordeiro - paginacao e marca (CSV 373-399) ───
def paginar_pagina_cordeiro_e_marca(driver, wait):
    """CSV 373-399: Abre img 1 cordeiro, next 7x, clica marca."""
    click_when_clickable(wait, LAMB_IMG_1)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))

    # CSV 376-396: next 7 vezes
    _clicar_next(wait, 7)

    # CSV 397-398: clica na primeira marca
    click_when_clickable(wait, CAROUSEL_FIRST_BRAND)
    time.sleep(5)


# ── Pagina dedicada cordeiro - ver produtos (CSV 400-412) ────────
def ver_produtos_pagina_cordeiro_final(driver, wait):
    """CSV 400-412: Navega /mapa-de-corte, aba Cordeiro, img 9, ver produtos."""
    driver.get("https://meuminerva.com/mapa-de-corte")
    wait.until(EC.presence_of_element_located(BOVINE_IMG_21))

    click_when_clickable(wait, ABA_CORDEIRO)
    wait.until(EC.presence_of_element_located(ABA_CORDEIRO_ACTIVE))

    click_when_clickable(wait, LAMB_IMG_9)
    wait.until(EC.element_to_be_clickable(MODAL_CLOSE))
    click_when_clickable(wait, MODAL_VER_PRODUTOS)
    time.sleep(5)
