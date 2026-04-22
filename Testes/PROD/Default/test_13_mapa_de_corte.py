import pytest

from helpers.mapa_de_corte import *
from helpers.auth import ensure_logged_in, logout
from helpers.popups import try_close_popups
from helpers.minicart import minicart_visible
from helpers.credentials import get_creds


# =========================
# Credenciais
# =========================
VALID_USER, VALID_PASS = get_creds("HUB_TESTE2_BRUNO_POPUP")


@pytest.mark.regressao
@pytest.mark.default
@pytest.mark.mapa
def test_13_mapa_de_corte(driver, setup_site, wait):
    # 1) Login
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    assert minicart_visible(driver), "Era para estar logado, mas o minicart não apareceu."
    try_close_popups(driver)

    # 2) Interagir com Mapa de corte Bovinos na Home
    interagir_mapa_bovino_cliques_home(driver, wait)

    # 3) Paginacao modal bovino + carrossel marcas + acessa alguma categoria de marca
    paginar_modal_bovino_e_carrossel_home(driver, wait)

    # 4) Interagir com 'Ver produtos' da modal do corte Bovinos - HOME
    interagir_ver_produtos_modal_bovinos_home(driver, wait)

    # 5) Interagir com Mapa de corte Cordeiro na Home
    interagir_mapa_cordeiro_cliques_home(driver, wait)

    # 6) Paginacao modal cordeiro + carrossel marcas + acessa alguma categoria de marca
    paginar_modal_cordeiro_e_marca_home(driver, wait)

    # 7) Interagir com 'Ver produtos' da modal do corte Cordeiro - HOME
    interagir_ver_produtos_modal_cordeiro_home(driver, wait)

    # 8) Efetuar logout
    logout(driver)

    # 9) Footer - Mapa de Corte (nova janela)
    abrir_mapa_corte_footer(driver, wait)

    # 10) Interagir com Mapa de corte Bovinos na pagina "/mapa-de-corte"
    interagir_mapa_bovino_cliques_pagina(driver, wait)

    # 11) Paginacao modal bovino + carrossel marcas + acessa alguma categoria de marca
    paginar_modal_bovino_e_carrossel_pagina(driver, wait)

    # 12) Interagir com 'Ver produtos' da modal do corte Bovinos - "/mapa-de-corte"
    driver.back()
    interagir_ver_produtos_modal_bovinos_pagina(driver, wait)

    # 13) Interagir com Mapa de corte Cordeiro na pagina "/mapa-de-corte"
    driver.back()
    interagir_mapa_cordeiro_cliques_pagina(driver, wait)

    # 14) Paginacao modal cordeiro + carrossel marcas + acessa alguma categoria de marca
    paginar_modal_cordeiro_e_marca_pagina(driver, wait)

    # 15) Interagir com 'Ver produtos' da modal do corte Cordeiro - "/mapa-de-corte"
    driver.back()
    interagir_ver_produtos_modal_cordeiro_pagina(driver, wait)
