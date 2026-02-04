import pytest

from helpers.auth import ensure_logged_in
from helpers.popups import try_close_popups

from helpers.wishlist import *
from helpers.home import add_favorite_from_home_first_carousel
from helpers.plp import add_favorite_from_category_first_item, search_and_add_favorite_by_index
from helpers.pdp import open_out_of_stock_product_and_add_to_favorites

from locators.plp import *




# =========================
# Credenciais
# =========================
VALID_USER = "caique.oliveira4@infobase.com.br"
VALID_PASS = "Min@1234"


@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.favoritos
def test_6_lista_de_favoritos(driver, setup_site, wait):
    """
    Conversão do seu script:
      - Login
      - Favoritar itens: Home, Pescados, Busca, Bovinos (paginando) + PDP
      - Abrir Lista de favoritos
      - Interações: qty, add all, inc/dec, add item, avise-me (não opcional)
      - Toggle favoritos e remoções + esvaziar minicart e voltar pra Home
    """

    # 1) Login
    ensure_logged_in(driver, VALID_USER, VALID_PASS)
    assert minicart_visible(driver), "Era para estar logado, mas o minicart não apareceu."
    try_close_popups(driver)

    # 2) Favorita na Home (primeiro carrossel)
    add_favorite_from_home_first_carousel(driver, wait)

    # 3) Favorita na categoria Pescados (primeiro item)
    add_favorite_from_category_first_item(driver, wait, CATEGORY_PESCADOS)

    # 4) Busca "peixe" e favorita o item 6 (igual script)
    search_and_add_favorite_by_index(driver, wait, term="peixe", index=6)

    # 5) Favorita na PDP um produto fora de estoque
    open_out_of_stock_product_and_add_to_favorites(driver, wait, category_locator=CATEGORY_CORDEIROS, pages=(1,2,3,4,5,6)) # Para alterar a categoria é só alterar 'category_locator'

    # 6) Abre Lista de favoritos
    open_favorites_page(driver, wait)

    # 7) Incrementa item 2
    wishlist_increment_by_index(driver, wait, 2)

    # 8) Ajusta input qty do item 3:
    wishlist_set_qty_input_by_index(driver, 3, "0")

    # 9) Adicionar todos ao carrinho
    wishlist_add_all_to_cart(driver, wait)

    # 10) Interações no primeiro item: ++, - e adiciona
    wishlist_increment_by_index(driver, wait, 1)
    wishlist_increment_by_index(driver, wait, 1)
    wishlist_decrement_by_index(driver, wait, 1)
    wishlist_add_item_to_cart_by_index(driver, wait, 1)

    # 11) Avise-me
    wishlist_avise_me_flow(driver, wait)

    # 12) Botão favorito dentro do minicart (remove produto dos favoritos pelo minicart, favorita novamente pelo minicart)
    wishlist_toggle_remove_onwishlist(driver, wait, 1)
    wishlist_toggle_add_towishlist(driver, wait)

    # 13) Remover itens da lista pelo o botão do card
    remove_card_item_with_confirm(driver, wait, 1)
    remove_card_item_with_confirm(driver, wait, 1)
    remove_card_item_with_confirm(driver, wait, 1)
    remove_card_item_with_confirm(driver, wait, 1)

    # 14) Esvaziar minicart e clicar "Ver produtos"
    wishlist_empty_and_go_products(driver, wait)

    # valida que segue logado
    assert minicart_visible(driver), "Era para continuar logado ao final do fluxo."
