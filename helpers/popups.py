from helpers.actions import try_click, click
from locators.common import SPIN_CLOSE, HOTJAR_CLOSE


def try_close_popups(driver):
    """Fecha popups ocasionais (spin/hotjar)"""
    try_click(driver, SPIN_CLOSE, timeout=1.5)
    try_click(driver, HOTJAR_CLOSE, timeout=1.5)


def try_close_hotjar(driver):
    """Fecha popup do Hotjar se aparecer (não falha se não existir)."""
    try:
        click(driver, HOTJAR_CLOSE, timeout=1.5)
    except Exception:
        pass
