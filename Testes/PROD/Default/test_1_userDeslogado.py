import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from locators.header import *
from locators.plp import *
from locators.pdp import BTN_ENTRAR_PDP, PRODUCT_TITLES
from locators.home import LAST_ORDERS, LAST_ITEMS

from helpers.actions import *
from helpers.waiters import *
from helpers.plp import *
from helpers.region import *
from helpers.home import *
from helpers.auth import *


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.deslogado
def test_1_userDeslogado(driver, setup_site, wait):
    """
    Usuário deslogado (visão default).
    Passa por modais, scroll, busca e cenários por categoria.
    """

    # 1) Termos de uso
    click_when_clickable(wait, LOGIN_NAME_SPAN)
    click_when_clickable(wait, BTN_TERMS)
    click_when_clickable(wait, BTN_CLOSE_MODAL)

    # 2) Quero ser cliente
    click_when_clickable(wait, BTN_QUERO_SER_CLIENTE)
    click_when_clickable(wait, BTN_CLOSE_QUERO_SER_CLIENTE)

    # 3) Scroll home e valida seções
    sections_xpaths = [
        "(//div[contains(@class, 'slider-products')])[1]",
        "//div[@class='brands-carousel']",
        "(//div[contains(@class, 'slider-products')])[2]",
        "//*[@class='cutting-map __home-section']",
        "//div[@class='footer-content']"
    ]
    for xp in sections_xpaths:
        scroll_and_confirm(wait, driver, xp)

    # 4) Busca simples -> paginação -> filtro congelado -> limpar -> ordenação A-Z e Z-A
    wait.until(EC.visibility_of_element_located(SEARCH_INPUT)).click()
    driver.find_element(*SEARCH_INPUT).send_keys("angus")
    click_when_clickable(wait, SEE_ALL_LINK)
    wait_category_loaded(wait, driver)

    wait.until(EC.visibility_of_element_located(FILTER_CONSERVACAO_OPEN))

    # paginação
    try_go_to_page(wait, driver, "2", timeout=6)
    try_go_to_page(wait, driver, "3", timeout=6)

    # garante filtro Congelado (OBRIGATÓRIO)
    aplicou_congelado = apply_filter_strict(driver, wait, FILTER_CONSERVACAO_OPEN, FILTER_CONSERVACAO_CONGELADO, timeout=12, retries=5)

    assert aplicou_congelado, "Busca (#4): não consegui aplicar o filtro Conservação = Congelado."

    wait.until(EC.visibility_of_element_located(SORTER_SELECT))
    wait.until(EC.visibility_of_element_located(FILTER_CLEAR_ALL))

    # limpar filtros (OBRIGATÓRIO)
    limpou_busca = clear_filters_strict(driver, wait, FILTER_CLEAR_ALL, timeout=15, retries=5)

    assert limpou_busca, "Busca (#4): não consegui limpar os filtros (Limpar Tudo)."

    # ordenação A-Z (OBRIGATÓRIO)
    ordenou_az = sort_strict(driver, wait, SORTER_SELECT, "name_asc", timeout=12, retries=4)
    assert ordenou_az, "Busca (#4): não consegui aplicar ordenação A-Z (name_asc)."

    # ordenação Z-A (OBRIGATÓRIO)
    ordenou_za = sort_strict(driver, wait, SORTER_SELECT, "name_desc", timeout=12, retries=4)
    assert ordenou_za, "Busca (#4): não consegui aplicar ordenação Z-A (name_desc)."

    # 5) Cenários por categoria
    # 5.1 Bovinos Premium: paginação 2 e 3 (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Bovinos Premium"))
    wait_category_loaded(wait, driver)
    try_go_to_page(wait, driver, "2", timeout=6)
    try_go_to_page(wait, driver, "3", timeout=6)

    # 5.2 Promoções: aplicar filtros Nacionalidade + Conservação (OBRIGATÓRIO)
    click_when_clickable(wait, CATEGORY_MENU("Promoções"))
    wait_category_loaded(wait, driver)

    # garante que os filtros carregaram na sidebar (senão o click “não acontece”)
    wait.until(EC.visibility_of_element_located(FILTER_NACIONALIDADE))
    wait.until(EC.visibility_of_element_located(FILTER_CONSERVACAO_OPEN))

    # aplica Nacionalidade (OBRIGATÓRIO) - strict
    aplicou_nat = apply_filter_strict(driver, wait, FILTER_NACIONALIDADE, FILTER_NACIONALIDADE_OPTION_1, timeout=12, retries=5)
    assert aplicou_nat, "Promoções (#5.2): não consegui aplicar filtro Nacionalidade."

    # aplica Conservação = Resfriado (OBRIGATÓRIO) - strict
    aplicou_cons = apply_filter_strict(driver, wait, FILTER_CONSERVACAO_OPEN, FILTER_CONSERVACAO_RESFRIADO, timeout=12, retries=5)
    assert aplicou_cons, "Promoções (#5.2): não consegui aplicar filtro Conservação (Resfriado)."

    # limpar filtros (OBRIGATÓRIO) - strict
    limpou_promo = clear_filters_strict(driver, wait, FILTER_CLEAR_ALL, timeout=15, retries=5)
    assert limpou_promo, "Promoções (#5.2): não consegui limpar os filtros (Limpar Tudo)."

    # 5.3 Pescados: ordenação (OBRIGATÓRIO)
    click_when_clickable(wait, CATEGORY_MENU("Pescados"))
    wait_category_loaded(wait, driver)

    wait.until(EC.visibility_of_element_located(SORTER_SELECT))

    # ordenação A-Z (OBRIGATÓRIO) - strict
    ok_pesc_az = sort_strict(driver, wait, SORTER_SELECT, "name_asc", timeout=12, retries=4)
    assert ok_pesc_az, "Pescados (#5.3): não consegui aplicar ordenação A-Z (name_asc)."

    # ordenação Z-A (OBRIGATÓRIO) - strict
    ok_pesc_za = sort_strict(driver, wait, SORTER_SELECT, "name_desc", timeout=12, retries=4)
    assert ok_pesc_za, "Pescados (#5.3): não consegui aplicar ordenação Z-A (name_desc)."

    # 5.4 Bovinos: apenas acessar
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    # 6) Tentativa de compra na lista (exige login) — só o 1º botão
    botoes_entrar = driver.find_elements(*BTN_ENTRAR_LISTA)
    if not botoes_entrar:
        raise AssertionError("Não encontrei botões 'Entrar' na listagem atual.")

    btn = botoes_entrar[0]

    # clica 1x e espera (rápido)
    safe_click(driver, wait, btn)
    try:
        expect_login_popup(driver, wait, label="listagem", timeout=8, retries=0)
    except TimeoutException:
        # fallback: reclica 1x (às vezes o primeiro click não dispara)
        safe_click(driver, wait, btn)
        expect_login_popup(driver, wait, label="listagem_retry", timeout=8, retries=0)

    # fecha/recolhe o dropdown/modal do header pra seguir o fluxo (mantém seu padrão)
    click_when_clickable(wait, LOGIN_NAME_SPAN)

    # 7) PDP de um produto (se houver produtos suficientes)
    produtos = driver.find_elements(*PRODUCT_TITLES)

    if len(produtos) >= 10:
        # abre PDP
        safe_click(driver, wait, produtos[9])

        # espera botão Entrar da PDP aparecer
        btn = wait.until(EC.visibility_of_element_located(BTN_ENTRAR_PDP))

        # 1º clique
        safe_click(driver, wait, btn)
        try:
            expect_login_popup(driver, wait, label="pdp", timeout=8, retries=0)
        except TimeoutException:
            # 1 retry rápido
            safe_click(driver, wait, btn)
            expect_login_popup(driver, wait, label="pdp_retry", timeout=8, retries=0)

    else:
        print("[WARN] Não há produtos suficientes para abrir a PDP (10º item).")

    # 8) Últimos pedidos/produtos exigem login
    click_when_clickable(wait, LOGO)  # garante que está no topo

    header_requires_login(driver, wait, LAST_ORDERS, label="last_orders")
    header_requires_login(driver, wait, LAST_ITEMS, label="last_items")

    # 9) Trocar região: default -> sul -> default (obrigatório)
    open_region_modal(driver)
    select_region(wait, "sul")

    open_region_modal(driver)
    select_region(wait, "default")

    wait.until(EC.visibility_of_element_located(LOGO))
