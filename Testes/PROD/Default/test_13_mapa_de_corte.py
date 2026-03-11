from helpers.mapa_de_corte import *


def test_13_mapaDeCorte(driver, setup_site, wait):
    """Smoke test completo do Mapa de Corte."""

    # ── CSV 12-23: Login ──────────────────────────────────────────
    fazer_login(driver, wait)

    # ── CSV 25-28: Fechar roleta (opcional) ───────────────────────
    fechar_roleta_cupons(driver, wait)

    # ── CSV 29-67: Mapa bovino - cliques rapidos ─────────────────
    interagir_mapa_bovino_cliques(driver, wait)

    # ── CSV 68-142: Paginacao modal bovino + carrossel marcas ────
    paginar_modal_bovino_e_carrossel(driver, wait)

    # ── CSV 143-156: Ver produtos bovino 20 ──────────────────────
    ver_produtos_bovino_20(driver, wait)

    # ── CSV 157-187: Aba Cordeiro - cliques rapidos ──────────────
    interagir_mapa_cordeiro_cliques(driver, wait)

    # ── CSV 188-217: Paginacao modal cordeiro + marca ────────────
    paginar_modal_cordeiro_e_marca(driver, wait)

    # ── CSV 218-238: Logout + footer ─────────────────────────────
    fazer_logout(driver, wait)

    # ── CSV 239-241: Footer - Mapa de Corte (nova janela) ────────
    abrir_mapa_corte_footer(driver, wait)

    # ── CSV 243-266: Pagina dedicada bovino - cliques ────────────
    interagir_mapa_corte_pagina_bovino(driver, wait)

    # ── CSV 267-329: Pagina dedicada bovino - paginacao + marca ──
    paginar_pagina_bovino_e_marca(driver, wait)

    # ── CSV 330-342: Ver produtos bovino 21 ──────────────────────
    ver_produtos_pagina_bovino_21(driver, wait)

    # ── CSV 343-372: Pagina dedicada cordeiro - cliques ──────────
    interagir_mapa_corte_pagina_cordeiro(driver, wait)

    # ── CSV 373-399: Pagina dedicada cordeiro - paginacao + marca
    paginar_pagina_cordeiro_e_marca(driver, wait)

    # ── CSV 400-412: Ver produtos cordeiro final ─────────────────
    ver_produtos_pagina_cordeiro_final(driver, wait)
