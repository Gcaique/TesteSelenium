import time
from helpers.actions import click
from locators.header import LOGIN_NAME_CONTAINER


def open_user_dropdown(driver):
    """Abre dropdown do usuário"""
    click(driver, LOGIN_NAME_CONTAINER, timeout=10)
    time.sleep(0.5)


def open_dropdown_item(driver, locator, timeout=10):
    """Abre item específico do dropdown"""
    open_user_dropdown(driver)
    click(driver, locator, timeout=timeout)
