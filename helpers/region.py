from helpers.waiters import visible
from helpers.actions import click

from locators.common import (
    REGION_OPEN,
    BTN_SUL_REGION,
    BTN_DEFAULT_REGION
)

from locators.header import (
    SEARCH_INPUT
)

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


#TESTE_1
'''def open_region_modal(wait, driver):
    driver.execute_script("window.scrollTo(0, 0);")
    click_when_clickable(wait, BTN_OPEN_REGION_MODAL)
    wait.until(EC.visibility_of_element_located(REGION_MODAL))


def select_region(wait, region: str):
    if region == "default":
        click_when_clickable(wait, BTN_DEFAULT_REGION)
    elif region == "sul":
        click_when_clickable(wait, BTN_SUL_REGION)
    else:
        raise ValueError("region deve ser 'default' ou 'sul'")

    wait.until(EC.invisibility_of_element_located(REGION_MODAL))'''
