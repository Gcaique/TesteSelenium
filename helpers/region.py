from selenium.webdriver.support import expected_conditions as EC

from helpers.waiters import visible
from helpers.actions import click, mobile_click_strict
from helpers.actions import click_when_clickable


from locators.common import (REGION_OPEN, BTN_SUL_REGION, BTN_DEFAULT_REGION, REGION_MODAL, MOBILE_REGION_OPEN)
from locators.header import (SEARCH_INPUT)

DEFAULT_CNPJ = "13.446.703/0001-90"
SUL_CNPJ = "36.454.420/0001-95"


def cnpj_por_regiao(region: str) -> str:
    region_lower = region.lower()
    if region_lower not in ["sul", "default"]:
        raise ValueError("region deve ser 'default' ou 'sul'")
    return SUL_CNPJ if region_lower == "sul" else DEFAULT_CNPJ


def open_region_modal(driver):
    click(driver, REGION_OPEN, timeout=10)
    visible(driver, BTN_SUL_REGION, timeout=10)


def switch_region(driver, to: str):
    if to not in ["sul", "default"]:
        raise ValueError("to deve ser 'sul' ou 'default'")

    open_region_modal(driver)

    if to == "sul":
        click(driver, BTN_SUL_REGION, timeout=10)
    else:
        click(driver, BTN_DEFAULT_REGION, timeout=10)

    visible(driver, SEARCH_INPUT, timeout=15)


def select_region(wait, region: str):
    if region == "default":
        click_when_clickable(wait, BTN_DEFAULT_REGION)
    elif region == "sul":
        click_when_clickable(wait, BTN_SUL_REGION)
    else:
        raise ValueError("region deve ser 'default' ou 'sul'")

    # O que realmente some é o modal
    wait.until(EC.invisibility_of_element_located(REGION_MODAL))

    # (extra) garante que a página “respirou” após troca
    wait.until(EC.visibility_of_element_located(SEARCH_INPUT))


#---------------------------------------------------------------
# 📱 MOBILE
#---------------------------------------------------------------
def open_region_modal_mobile(driver):
    mobile_click_strict(driver, MOBILE_REGION_OPEN, timeout=10, retries=4, sleep_between=0.25)
    visible(driver, BTN_SUL_REGION, timeout=15)

def switch_region_mobile(driver, to: str):
    if to not in ["sul", "default"]:
        raise ValueError("to deve ser 'sul' ou 'default'")

    open_region_modal_mobile(driver)

    if to == "sul":
        mobile_click_strict(driver, BTN_SUL_REGION, timeout=10, retries=4, sleep_between=0.25)
    else:
        mobile_click_strict(driver, BTN_DEFAULT_REGION, timeout=10, retries=4, sleep_between=0.25)

    visible(driver, SEARCH_INPUT, timeout=15)
