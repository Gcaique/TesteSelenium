import pytest

from conftest import click_if_present

from helpers.mapa_de_corte import *
from helpers.auth import ensure_logged_in_mobile, logout_mobile
from helpers.popups import try_close_popups
from helpers.minicart import minicart_visible

from locators.common import COOKIE_ACCEPT


# =========================
# Credenciais
# =========================
VALID_USER = "hub.teste2-bruno-popup@minervafoods.com"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.mapa
@pytest.mark.mobile
def test_13_mapa_de_corte_mobile(driver, setup_site, wait):
    # 1) Login
    click_if_present(driver, COOKIE_ACCEPT, seconds=20)
    ensure_logged_in_mobile(driver, VALID_USER, VALID_PASS)
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
    logout_mobile(driver)

    # 9) Footer - Mapa de Corte (nova janela)
    abrir_mapa_corte_footer_mobile(driver, wait)

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
