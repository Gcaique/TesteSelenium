from helpers.actions import try_click
from locators.common import SPIN_CLOSE, HOTJAR_CLOSE


def try_close_popups(driver):
    """Fecha popups ocasionais (spin/hotjar)"""
    try_click(driver, SPIN_CLOSE, timeout=1.5)
    try_click(driver, HOTJAR_CLOSE, timeout=1.5)
