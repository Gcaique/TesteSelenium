import pytest

from locators.cart import MINICART_ICON

from helpers.lp_deslogado_logado import *
from helpers.auth import submit_username_valid, login_password
from helpers.minicart import remove_simple_delete
from helpers.popups import try_close_popups

VALID_USER = "caique.oliveira@infobase.com.br"
VALID_PASS = "Min@1234"

@pytest.mark.smoke
@pytest.mark.default
@pytest.mark.lp
def test_11_lp_marcas(driver, setup_site, wait):

   # 1) Acessar LP Alma lusa pelo carrossel da HOME
   entrar_alma_lusa_via_home(driver, wait)

   # 2) Alma Lusa DESLOGADO
   fluxo_alma_lusa_deslogado(driver, wait)

   # 3) Ir para Estância
   ir_para_estancia_via_outras_marcas(driver, wait)

   # 4) Estância DESLOGADO
   fluxo_estancia_deslogado(driver, wait)

   # 5) Efetuar login
   submit_username_valid(driver, VALID_USER, "usuário válido")
   login_password(driver, VALID_PASS, "senha válida", expect_success=True)
   wait.until(EC.visibility_of_element_located(MINICART_ICON))
   try_close_popups(driver)

   # 6) Navegar nas LPs de marcas logado + adicionar produtos em marcas selecionadas (Alma-lusa e Pul)
   marcas = [
       "alma-lusa",
       "pul",
       "pul-pro",
       "pul-selection",
       "estancia-92",
       "cabana",
   ]
   for marca in marcas:
       navegar_para_marca_via_ancora(driver, wait, marca)
       scroll_lento(driver)
       buscar_e_add_produto_marca(driver, wait, "sal", marca)

   # 7) Removendo item do mini-cart
   remove_simple_delete(driver, wait, 1)
   time.sleep(5)