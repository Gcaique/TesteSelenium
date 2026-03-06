import pytest
from helpers.lp_marcas_logado_deslogado import *
@pytest.mark.lp
@pytest.mark.full
def test_lp_marcas(driver, setup_site, wait):
   print("PASSO 1 - HOME")
   entrar_alma_lusa_via_home(driver, wait)
   print("PASSO 2 - Alma Lusa DESLOGADO")
   fluxo_alma_lusa_deslogado(driver, wait)
   print("PASSO 3 - Ir Estância")
   ir_para_estancia_via_outras_marcas(driver, wait)
   print("PASSO 4 - Estância DESLOGADO")
   fluxo_estancia_deslogado(driver, wait)
   print("PASSO 5 - LOGIN")
   login_via_estancia(driver, wait)
   marcas = [
       "alma-lusa",
       "pul",
       "pul-pro",
       "pul-selection",
       "estancia-92",
       "cabana",
   ]
   for marca in marcas:
       print(f"PASSO - Marca {marca}")
       navegar_para_marca_via_ancora(driver, wait, marca)
       buscar_e_adicionar(driver, wait, "sal")
       scroll_lento(driver)