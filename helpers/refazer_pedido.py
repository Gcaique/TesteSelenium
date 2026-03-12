import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from helpers.actions import scroll_to_middle, scroll_to_top, click_when_clickable, mobile_click_strict
from helpers.minicart import wait_minicart_loading, wait_minicart_ready

from locators.lastOrders_lastItems import *
from locators.home import LAST_ORDERS, LAST_ITEMS
from locators.cart import MINICART_LOADING_1
from locators.dashboard import FORMA_PAGAMENTO_COL, ORDER_DETAIL_FIRST, ORDERS_TABLE, REORDER_BTN, GRID_ORDERS_READY, MOBILE_ORDER_DETAIL_FIRST


def clicar_ultimos_pedidos(driver, wait):
    """Aguarda e clica no botao Ultimos Pedidos."""
    wait.until(EC.element_to_be_clickable(LAST_ORDERS))
    click_when_clickable(wait, LAST_ORDERS)

def aguardar_redirect_ultimos_pedidos(driver, wait):
    """Aguarda redirect (botao Ultimos Pedidos desaparece)."""
    wait.until(EC.invisibility_of_element_located(LAST_ORDERS))

def filtrar_ultimos_7_dias(driver, wait):
    """Seleciona filtro 'Ultimos 7 dias', filtra e limpa."""
    wait.until(EC.element_to_be_clickable(LAST_ORDERS_ADD_CART_BTN))

    click_when_clickable(wait, PERIOD_SELECT)
    time.sleep(1)
    click_when_clickable(wait, PERIOD_LAST_7_DAYS)
    click_when_clickable(wait, FILTER_BTN)

    wait.until(EC.element_to_be_clickable(CLEAR_FILTER_LINK))
    click_when_clickable(wait, CLEAR_FILTER_LINK)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))

def ver_similar_refazer_e_adicionar(driver, wait):
    """Clica Ver Similar se existir. Caso contrário adiciona pedido direto."""
    botoes_ver_similar = driver.find_elements(*VER_SIMILAR_REFAZER_BTN)

    if botoes_ver_similar:
        scroll_to_middle(driver, wait, VER_SIMILAR_REFAZER_BTN)
        click_when_clickable(wait, VER_SIMILAR_REFAZER_BTN)
        time.sleep(2)

        scroll_to_middle(driver, wait, ADD_ORDER_WITH_SIMILAR_BTN)
        click_when_clickable(wait, ADD_ORDER_WITH_SIMILAR_BTN)

    else:
        scroll_to_middle(driver, wait, ADD_ORDER_BTN)
        click_when_clickable(wait, ADD_ORDER_BTN)

    # Mini-cart loading
    wait_minicart_ready(driver, 10)

def navegar_comprados_recentemente(driver, wait):
    """Clica no bloco Comprados recentemente."""
    click_when_clickable(wait, LAST_ITEMS)
    wait.until(EC.invisibility_of_element_located(LAST_ITEMS))


def filtrar_comprados_recentemente(driver, wait):
    """Filtro 'Ultimos 7 dias' e limpa."""
    wait.until(EC.element_to_be_clickable(ADD_ALL_TO_CART_BTN))

    click_when_clickable(wait, PERIOD_SELECT)
    time.sleep(1)
    click_when_clickable(wait, PERIOD_LAST_7_DAYS)
    click_when_clickable(wait, FILTER_BTN)

    wait.until(EC.element_to_be_clickable(CLEAR_FILTER_LINK))
    click_when_clickable(wait, CLEAR_FILTER_LINK)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))


def scroll_ate_adicionar_todos(driver, wait):
    """Scroll ate ultimo produto e botao Adicionar todos."""
    scroll_to_middle(driver, wait, PAGE_SIZE)
    scroll_to_middle(driver, wait, ADD_ALL_TO_CART_BTN)

def favoritar_e_desfavoritar(driver, wait):
    """Favorita e desfavorita o primeiro item."""
    click_when_clickable(wait, FAVORITE_BTN_FIRST)
    wait.until(EC.visibility_of_element_located(FAVORITE_ON_WISHLIST_FIRST))

    click_when_clickable(wait, FAVORITE_ON_WISHLIST_FIRST)
    wait.until(EC.visibility_of_element_located(FAVORITE_ADD_TO_FIRST))

def interagir_avise_me(driver, wait):
    """Clica no Avise-me, aguarda status, atualiza a pagina, clica em
    'Ok, avisaremos' e aguarda voltar ao status original."""
    scroll_to_middle(driver, wait, AVISE_ME_SPAN)
    click_when_clickable(wait, AVISE_ME_SPAN)
    wait.until(EC.element_to_be_clickable(AVISE_ME_CLICKED_SPAN))
    time.sleep(2)

    driver.refresh()
    time.sleep(5)

    click_when_clickable(wait, AVISE_ME_CLICKED_SPAN)
    wait.until(EC.element_to_be_clickable(AVISE_ME_SPAN))
    time.sleep(2)

def ver_similar_comprados_e_adicionar(driver, wait):
    """Executa fluxo de similar comprados apenas se o botão existir."""

    # Verifica se o botão existe
    botoes_ver_similar = driver.find_elements(*VER_SIMILAR_COMPRADOS_BTN)

    if not botoes_ver_similar:
        return

    # Scroll e clica Ver Similar
    scroll_to_middle(driver, wait, VER_SIMILAR_COMPRADOS_BTN)
    click_when_clickable(wait, VER_SIMILAR_COMPRADOS_BTN)
    wait.until(EC.element_to_be_clickable(SWITCH_BACK_BTN))

    # Incrementa qty 2x
    click_when_clickable(wait, SIMILAR_INCREMENT_QTY)
    click_when_clickable(wait, SIMILAR_INCREMENT_QTY)

    # Decrementa qty 1x
    click_when_clickable(wait, SIMILAR_DECREMENT_QTY)

    # Clica Adicionar
    click_when_clickable(wait, SIMILAR_ADD_TO_CART_BTN)

    # Mini-cart loading
    wait.until(EC.visibility_of_element_located(MINICART_LOADING_1))
    wait.until(EC.invisibility_of_element_located(MINICART_LOADING_1))
    time.sleep(2)

    # Voltar ao card original
    click_when_clickable(wait, SWITCH_BACK_BTN)
    time.sleep(1)

def adicionar_todos_ao_carrinho(driver, wait):
    """Scroll, adiciona todos ao carrinho, aguarda mini-cart"""
    scroll_to_middle(driver, wait, ADD_ALL_TO_CART_BTN)
    click_when_clickable(wait, ADD_ALL_TO_CART_BTN)

    wait_minicart_loading(driver)

def ordenar_por_forma_pagamento(driver, wait):
    """Ordena por Forma de pagamento."""
    click_when_clickable(wait, FORMA_PAGAMENTO_COL)
    wait.until(EC.visibility_of_element_located(GRID_ORDERS_READY))

def abrir_detalhe_primeiro_pedido(driver, wait):
    """Abre detalhe do primeiro pedido e scroll ate grid."""
    click_when_clickable(wait, ORDER_DETAIL_FIRST)
    time.sleep(8)
    scroll_to_middle(driver, wait, ORDERS_TABLE)

def refazer_pedido(driver, wait):
    """Scroll ate Refazer pedido, clica e limpa filtro."""
    scroll_to_middle(driver, wait, REORDER_BTN)
    click_when_clickable(wait, REORDER_BTN)

    wait.until(EC.visibility_of_element_located(FILTER_BTN_DISABLED))

    click_when_clickable(wait, CLEAR_FILTER_LINK)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def ver_similar_refazer_e_adicionar_mobile(driver, wait):
    """Clica Ver Similar se existir. Caso contrário adiciona pedido direto."""
    botoes_ver_similar = driver.find_elements(*VER_SIMILAR_REFAZER_BTN)

    if botoes_ver_similar:
        scroll_to_middle(driver, wait, VER_SIMILAR_REFAZER_BTN)
        click_when_clickable(wait, VER_SIMILAR_REFAZER_BTN)
        time.sleep(2)

        scroll_to_middle(driver, wait, ADD_ORDER_WITH_SIMILAR_BTN)
        click_when_clickable(wait, ADD_ORDER_WITH_SIMILAR_BTN)

    else:
        scroll_to_middle(driver, wait, ADD_ORDER_BTN)
        click_when_clickable(wait, ADD_ORDER_BTN)

    # Mini-cart loading
    time.sleep(8)

def filtrar_ultimos_7_dias_mobile(driver, wait):
    """Seleciona filtro 'Ultimos 7 dias', filtra e limpa."""

    mobile_click_strict(driver, PERIOD_SELECT, 10, 4, 0.25)
    time.sleep(1)
    mobile_click_strict(driver, PERIOD_LAST_7_DAYS, 10, 4, 0.25)
    mobile_click_strict(driver, FILTER_BTN, 10, 4, 0.25)

    time.sleep(3)
    mobile_click_strict(driver, CLEAR_FILTER_LINK, 10, 4, 0.25)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))

def ver_similar_comprados_e_adicionar_mobile(driver, wait):
    """Executa fluxo de similar comprados apenas se o botão existir."""

    # Verifica se o botão existe
    botoes_ver_similar = driver.find_elements(*VER_SIMILAR_COMPRADOS_BTN)

    if not botoes_ver_similar:
        return

    # Scroll e clica Ver Similar
    scroll_to_middle(driver, wait, VER_SIMILAR_COMPRADOS_BTN)
    click_when_clickable(wait, VER_SIMILAR_COMPRADOS_BTN)
    wait.until(EC.element_to_be_clickable(SWITCH_BACK_BTN))

    # Incrementa qty 2x
    click_when_clickable(wait, SIMILAR_INCREMENT_QTY)
    click_when_clickable(wait, SIMILAR_INCREMENT_QTY)

    # Decrementa qty 1x
    click_when_clickable(wait, SIMILAR_DECREMENT_QTY)

    # Clica Adicionar
    click_when_clickable(wait, SIMILAR_ADD_TO_CART_BTN)

    # Mini-cart loading
    time.sleep(5)

    # Voltar ao card original
    click_when_clickable(wait, SWITCH_BACK_BTN)
    time.sleep(1)

def adicionar_todos_ao_carrinho_mobile(driver, wait):
    """Scroll, adiciona todos ao carrinho, aguarda mini-cart"""
    scroll_to_middle(driver, wait, ADD_ALL_TO_CART_BTN)
    click_when_clickable(wait, ADD_ALL_TO_CART_BTN)

    time.sleep(8)

def abrir_detalhe_primeiro_pedido_mobile(driver, wait):
    """Abre detalhe do primeiro pedido."""
    mobile_click_strict(driver, MOBILE_ORDER_DETAIL_FIRST, 10, 4, 0.25)
    time.sleep(8)