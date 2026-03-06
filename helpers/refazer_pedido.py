import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from helpers.actions import scroll_to_middle, scroll_to_top, click_when_clickable
from locators.refazer_pedido import *


# ═══════════════════════════════════════════════════════════════════════════
# 1) LOGIN VIA ULTIMOS PEDIDOS
# ═══════════════════════════════════════════════════════════════════════════

def clicar_ultimos_pedidos(driver, wait):
    """CSV 11-12: Aguarda e clica no botao Ultimos Pedidos."""
    wait.until(EC.element_to_be_clickable(LAST_ORDERS_BTN))
    click_when_clickable(wait, LAST_ORDERS_BTN)


def preencher_email_login(driver, wait, username):
    """CSV 14-17: Aguarda modal, preenche e-mail e clica Avancar."""
    wait.until(EC.visibility_of_element_located(LOGIN_SEND_BTN))
    click_when_clickable(wait, USERNAME_INPUT)
    driver.find_element(*USERNAME_INPUT).send_keys(username)
    click_when_clickable(wait, LOGIN_SEND_BTN)


def preencher_senha_login(driver, wait, password):
    """CSV 19-24: Aguarda campo senha, preenche e clica Avancar."""
    wait.until(EC.visibility_of_element_located(PASSWORD_INPUT))
    click_when_clickable(wait, PASSWORD_INPUT)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    click_when_clickable(wait, LOGIN_SEND_BTN)


def aguardar_redirect_ultimos_pedidos(driver, wait):
    """CSV 26: Aguarda redirect (botao Ultimos Pedidos desaparece)."""
    wait.until(EC.invisibility_of_element_located(LAST_ORDERS_BTN))


def fechar_roleta_cupons(driver, wait):
    """CSV 28-30: Fecha a roleta de cupons (spin to win).
    A roleta pode nao aparecer dependendo da sessao/cookies,
    por isso usamos um timeout curto e ignoramos se nao encontrar.
    """
    try:
        short_wait = WebDriverWait(driver, 10)
        short_wait.until(EC.element_to_be_clickable(SPIN_CLOSE_BTN))
        click_when_clickable(short_wait, SPIN_CLOSE_BTN)
        time.sleep(2)
    except TimeoutException:
        pass


# ═══════════════════════════════════════════════════════════════════════════
# 2) ULTIMOS PEDIDOS - FILTRO
# ═══════════════════════════════════════════════════════════════════════════

def filtrar_ultimos_7_dias(driver, wait):
    """CSV 32-42: Seleciona filtro 'Ultimos 7 dias', filtra e limpa."""
    wait.until(EC.element_to_be_clickable(LAST_ORDERS_ADD_CART_BTN))

    click_when_clickable(wait, PERIOD_SELECT)
    time.sleep(1)
    click_when_clickable(wait, PERIOD_LAST_7_DAYS)
    click_when_clickable(wait, FILTER_BTN)

    wait.until(EC.element_to_be_clickable(CLEAR_FILTER_LINK))
    click_when_clickable(wait, CLEAR_FILTER_LINK)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))


# ═══════════════════════════════════════════════════════════════════════════
# 3) ULTIMOS PEDIDOS - VER SIMILAR + ADICIONAR
# ═══════════════════════════════════════════════════════════════════════════

def ver_similar_refazer_e_adicionar(driver, wait):
    """CSV 86-102: Clica Ver Similar, depois Adicionar pedido ao carrinho,
    aguarda mini-cart e vai ao checkout."""
    # Scroll ate o botao Ver Similar habilitado e clica
    scroll_to_middle(driver, wait, VER_SIMILAR_REFAZER_BTN)
    click_when_clickable(wait, VER_SIMILAR_REFAZER_BTN)
    time.sleep(2)  # Aguarda troca de produto para disponivel

    # Scroll ate o botao "Adicionar pedido ao carrinho" do pedido com similar
    scroll_to_middle(driver, wait, ADD_ORDER_WITH_SIMILAR_BTN)
    click_when_clickable(wait, ADD_ORDER_WITH_SIMILAR_BTN)

    # Mini-cart loading
    wait.until(EC.visibility_of_element_located(MINICART_LOADING))
    wait.until(EC.invisibility_of_element_located(MINICART_LOADING))
    time.sleep(8)

    # Finalizar compra
    wait.until(EC.element_to_be_clickable(CHECKOUT_BTN))
    click_when_clickable(wait, CHECKOUT_BTN)


# ═══════════════════════════════════════════════════════════════════════════
# 4) CHECKOUT - SHIPPING
# ═══════════════════════════════════════════════════════════════════════════

def avancar_shipping(driver, wait):
    """CSV 55-60 / 103-108: Aguarda shipping, fecha cupons e avanca."""
    wait.until(EC.element_to_be_clickable(SHIPPING_NEXT_BTN))
    time.sleep(5)
    click_when_clickable(wait, CUPONS_EXPANDED)
    wait.until(EC.presence_of_element_located(CUPONS_COLLAPSED))
    click_when_clickable(wait, SHIPPING_NEXT_BTN)


# ═══════════════════════════════════════════════════════════════════════════
# 5) CHECKOUT - PAYMENT BOLETO
# ═══════════════════════════════════════════════════════════════════════════

def selecionar_boleto_e_finalizar(driver, wait, condicao_locator):
    """Seleciona Boleto, condicao, aceita termos e finaliza."""
    # Aguarda loading
    wait.until(EC.presence_of_element_located(BODY_AJAX_LOADING))
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))
    time.sleep(3)

    # Seleciona Boleto
    click_when_clickable(wait, BOLETO_LABEL)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))
    time.sleep(3)

    # Scroll ate Finalizar
    scroll_to_middle(driver, wait, FINALIZAR_COMPRA_BTN)

    # Seleciona condicao
    click_when_clickable(wait, BOLETO_CONDITIONS_SELECT)
    wait.until(EC.element_to_be_clickable(condicao_locator))
    click_when_clickable(wait, condicao_locator)
    wait.until(EC.invisibility_of_element_located(BODY_AJAX_LOADING))
    time.sleep(3)

    # Aceita termos
    click_when_clickable(wait, TERMS_CHECKBOX)

    # Finaliza compra
    click_when_clickable(wait, FINALIZAR_COMPRA_BTN)

    # Aguarda pagina de sucesso
    wait.until(EC.presence_of_element_located(SUCCESS_PAGE_BODY))


# ═══════════════════════════════════════════════════════════════════════════
# 6) VOLTA PARA HOME
# ═══════════════════════════════════════════════════════════════════════════

def ir_para_home(driver, wait):
    """CSV 131-135: Clica Ir Para Home, aguarda e refresh."""
    click_when_clickable(wait, IR_PARA_HOME_BTN)
    time.sleep(8)
    driver.refresh()
    time.sleep(5)


# ═══════════════════════════════════════════════════════════════════════════
# 7) COMPRADOS RECENTEMENTE - NAVEGACAO E FILTRO
# ═══════════════════════════════════════════════════════════════════════════

def navegar_comprados_recentemente(driver, wait):
    """CSV 136-137: Clica no bloco Comprados recentemente."""
    click_when_clickable(wait, LAST_ITEMS_BTN)
    wait.until(EC.invisibility_of_element_located(LAST_ORDERS_BTN))


def filtrar_comprados_recentemente(driver, wait):
    """CSV 139-150: Filtro 'Ultimos 7 dias' e limpa."""
    wait.until(EC.element_to_be_clickable(ADD_ALL_TO_CART_BTN))

    click_when_clickable(wait, PERIOD_SELECT)
    time.sleep(1)
    click_when_clickable(wait, PERIOD_LAST_7_DAYS)
    click_when_clickable(wait, FILTER_BTN)

    wait.until(EC.element_to_be_clickable(CLEAR_FILTER_LINK))
    click_when_clickable(wait, CLEAR_FILTER_LINK)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))


def scroll_ate_adicionar_todos(driver, wait):
    """CSV 151-154: Scroll ate ultimo produto e botao Adicionar todos."""
    scroll_to_middle(driver, wait, PAGE_SIZE)
    scroll_to_middle(driver, wait, ADD_ALL_TO_CART_BTN)


def favoritar_e_desfavoritar(driver, wait):
    """CSV 155-160: Favorita e desfavorita o primeiro item."""
    click_when_clickable(wait, FAVORITE_BTN_FIRST)
    wait.until(EC.visibility_of_element_located(FAVORITE_ON_WISHLIST_FIRST))

    click_when_clickable(wait, FAVORITE_ON_WISHLIST_FIRST)
    wait.until(EC.visibility_of_element_located(FAVORITE_ADD_TO_FIRST))


# ═══════════════════════════════════════════════════════════════════════════
# 8) COMPRADOS RECENTEMENTE - AVISE-ME / SEM ESTOQUE
# ═══════════════════════════════════════════════════════════════════════════

def interagir_avise_me(driver, wait):
    """CSV 161-172: Clica no Avise-me, aguarda status, clica em
    'Ok, avisaremos' e aguarda voltar ao status original."""
    scroll_to_middle(driver, wait, AVISE_ME_SPAN)
    click_when_clickable(wait, AVISE_ME_SPAN)
    wait.until(EC.element_to_be_clickable(AVISE_ME_CLICKED_SPAN))
    time.sleep(2)

    click_when_clickable(wait, AVISE_ME_CLICKED_SPAN)
    wait.until(EC.element_to_be_clickable(AVISE_ME_SPAN))
    time.sleep(2)


# ═══════════════════════════════════════════════════════════════════════════
# 9) COMPRADOS RECENTEMENTE - VER SIMILAR + ADICIONAR
# ═══════════════════════════════════════════════════════════════════════════

def ver_similar_comprados_e_adicionar(driver, wait):
    """CSV 173-193: Clica Ver Similar, incrementa/decrementa qty,
    clica Adicionar, aguarda mini-cart e volta ao card original."""
    # Scroll e clica Ver Similar
    scroll_to_middle(driver, wait, VER_SIMILAR_COMPRADOS_BTN)
    click_when_clickable(wait, VER_SIMILAR_COMPRADOS_BTN)
    wait.until(EC.element_to_be_clickable(SWITCH_BACK_BTN))

    # Incrementa qty 2x
    click_when_clickable(wait, SIMILAR_INCREMENT_QTY)
    click_when_clickable(wait, SIMILAR_INCREMENT_QTY)

    # Decrementa qty 1x
    click_when_clickable(wait, SIMILAR_DECREMENT_QTY)

    # Clica Adicionar (adiciona o similar ao carrinho)
    click_when_clickable(wait, SIMILAR_ADD_TO_CART_BTN)

    # Mini-cart loading
    wait.until(EC.visibility_of_element_located(MINICART_LOADING))
    wait.until(EC.invisibility_of_element_located(MINICART_LOADING))
    time.sleep(2)

    # Clica Voltar para retornar ao card original
    click_when_clickable(wait, SWITCH_BACK_BTN)
    time.sleep(1)


# ═══════════════════════════════════════════════════════════════════════════
# 10) COMPRADOS RECENTEMENTE - ADICIONAR TODOS AO CARRINHO
# ═══════════════════════════════════════════════════════════════════════════

def adicionar_todos_ao_carrinho_e_checkout(driver, wait):
    """CSV 194-203: Scroll, adiciona todos ao carrinho, aguarda mini-cart
    e vai ao checkout."""
    scroll_to_middle(driver, wait, ADD_ALL_TO_CART_BTN)
    click_when_clickable(wait, ADD_ALL_TO_CART_BTN)

    # Mini-cart loading (add all usa classe diferente)
    wait.until(EC.visibility_of_element_located(MINICART_ACTIVE_LOADING))
    wait.until(EC.invisibility_of_element_located(MINICART_ACTIVE_LOADING))
    time.sleep(2)

    # Finalizar compra
    wait.until(EC.element_to_be_clickable(CHECKOUT_BTN))
    click_when_clickable(wait, CHECKOUT_BTN)


# ═══════════════════════════════════════════════════════════════════════════
# 11) MEUS PEDIDOS
# ═══════════════════════════════════════════════════════════════════════════

def abrir_meus_pedidos(driver, wait):
    """CSV 289-294: Abre menu do usuario e acessa Meus Pedidos."""
    time.sleep(5)
    click_when_clickable(wait, LOGIN_NAME_MENU)
    time.sleep(1)
    click_when_clickable(wait, MEUS_PEDIDOS_LINK)
    wait.until(EC.visibility_of_element_located(ORDERS_PAGINATION_SELECT))


def ordenar_por_forma_pagamento(driver, wait):
    """CSV 296-298: Ordena por Forma de pagamento."""
    click_when_clickable(wait, FORMA_PAGAMENTO_COL)
    wait.until(EC.visibility_of_element_located(ORDERS_PAGINATION_SELECT))


def abrir_detalhe_primeiro_pedido(driver, wait):
    """CSV 300-304: Abre detalhe do primeiro pedido e scroll ate grid."""
    click_when_clickable(wait, ORDER_DETAIL_FIRST)
    time.sleep(8)
    scroll_to_middle(driver, wait, ORDERS_TABLE)


def refazer_pedido(driver, wait):
    """CSV 305-313: Scroll ate Refazer pedido, clica e limpa filtro."""
    scroll_to_middle(driver, wait, REORDER_BTN)
    click_when_clickable(wait, REORDER_BTN)

    wait.until(EC.visibility_of_element_located(FILTER_BTN_DISABLED))

    click_when_clickable(wait, CLEAR_FILTER_LINK)
    wait.until(EC.invisibility_of_element_located(CLEAR_FILTER_LINK))
