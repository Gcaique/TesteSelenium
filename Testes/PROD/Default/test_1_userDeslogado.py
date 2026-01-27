import pytest

from locators.header import *
from locators.plp import *
from locators.pdp import BTN_ENTRAR_PDP
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
    click_when_clickable(wait, (By.XPATH, "//div[@id='login-name']/span"))
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

    # 4) Busca simples
    wait.until(EC.visibility_of_element_located(SEARCH_INPUT)).click()
    driver.find_element(*SEARCH_INPUT).send_keys("angus")
    click_when_clickable(wait, SEARCH_BUTTON)
    try_visible(wait, PAGES_UL, timeout=5)


    # 5) Cenários por categoria
    # 5.1 Bovinos Premium: paginação 2 e 3 (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Bovinos Premium"))
    wait_category_loaded(wait, driver)
    try_go_to_page(wait, driver, "2", timeout=4)
    try_go_to_page(wait, driver, "3", timeout=4)

    # 5.2 Promo: filtros Nacionalidade + Conservação (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Promoções"))
    wait_category_loaded(wait, driver)

    try_apply_filter(wait, FILTER_NACIONALIDADE, FILTER_NACIONALIDADE_OPTION_1, timeout=5)
    try_apply_filter(wait, FILTER_CONSERVACAO_OPEN, FILTER_CONSERVACAO_RESFRIADO, timeout=5)

    # se aplicar filtro, tenta limpar (sem travar)
    try_clear_filters(wait, timeout=4)

    # 5.3 Pescados: ordenação (sem travar)
    click_when_clickable(wait, CATEGORY_MENU("Pescados"))
    wait_category_loaded(wait, driver)

    try_sort(wait, driver, "name_asc", timeout=4)
    try_sort(wait, driver, "name_desc", timeout=4)

    # 5.4 Bovinos: apenas acessar
    click_when_clickable(wait, CATEGORY_MENU("Bovinos"))
    wait_category_loaded(wait, driver)

    # 6) Tentativa de compra na lista (exige login) — sem travar se não existir botão
    botoes_entrar = driver.find_elements(*BTN_ENTRAR_LISTA)

    if not botoes_entrar:
        raise AssertionError("Não encontrei botões 'Entrar' na listagem atual.")

    abriu = False

    # tenta alguns botões (evita depender do índice 9 que pode estar fora do viewport)
    for btn in botoes_entrar[:10]:
        safe_click(driver, wait, btn)

        try:
            expect_login_popup(driver, wait, "listagem")  # ou "pdp"
            abriu = True
            break
        except TimeoutException:
            # não abriu com esse botão, tenta o próximo
            continue

    if not abriu:
        driver.save_screenshot("debug_entrar_nao_abriu_login.png")
        raise AssertionError("Cliquei em botões 'Entrar', mas o pop-up do header com #username não apareceu.")

    # segue o fluxo
    click_when_clickable(wait, (By.XPATH, "//div[@id='login-name']/span"))

    # 7) PDP de um produto (se houver produtos suficientes)
    produtos = driver.find_elements(By.XPATH, "//*[contains(@id,'product-item-info')]//strong")
    if len(produtos) >= 10:
        produtos[9].click()
        wait.until(EC.visibility_of_element_located(BTN_ENTRAR_PDP))
        click_when_clickable(wait, BTN_ENTRAR_PDP)
        expect_login_popup(driver, wait, "pdp")

    else:
        print("[WARN] Não há produtos suficientes para abrir a PDP (10º item).")

    # 8) Últimos pedidos/produtos exigem login
    click_when_clickable(wait, LOGO)

    for item in [LAST_ORDERS, LAST_ITEMS]:
        if try_click(wait, item, timeout=5):
            expect_login_popup(driver, wait, label="header_last_orders_items")
            click_when_clickable(wait, (By.XPATH, "//div[@id='login-name']/span"))

    # 9) Trocar região: default -> sul -> default (obrigatório)
    open_region_modal(wait, driver)
    switch_region(wait, "sul")

    open_region_modal(wait, driver)
    switch_region(wait, "default")

    # Assert final
    wait.until(EC.visibility_of_element_located(LOGO))
