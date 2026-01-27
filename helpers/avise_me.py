import time

from helpers.waiters import visible, wait, wait_any_visible, wait_visible_any
from helpers.actions import scroll_and_click

from locators.plp import (
    SORTER_SELECT,
    AVISE_DISABLED_ANY,
    AVISE_ENABLED_ANY,
)


def open_pdp_from_first_avise_in_plp(driver):
    visible(driver, SORTER_SELECT, timeout=25)

    avise = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=5)
    if not avise:
        avise = wait_any_visible(driver, AVISE_ENABLED_ANY, timeout=2)

    if not avise:
        return False

    card = driver.execute_script(
        "return arguments[0].closest('[id^=\"product-item-info_\"]');",
        avise,
    )

    if not card:
        return False

    link = driver.execute_script(
        "return arguments[0].querySelector('a.product-item-link, a.product-item-photo');",
        card,
    )

    if not link:
        link = driver.execute_script(
            "return arguments[0].querySelector('span.product-image-wrapper');",
            card,
        )
        if not link:
            return False

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        link,
    )

    time.sleep(0.2)
    driver.execute_script("arguments[0].click();", link)

    return True


def toggle_avise_me_requires_refresh(
    driver,
    page_ready_locator=None,
    timeout=25,
    wait_click_class=False,
):
    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(
            driver,
            [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY],
            timeout=timeout,
        )

    disabled = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=timeout)
    if not disabled:
        return False

    scroll_and_click(driver, disabled)

    if wait_click_class:
        wait(driver, timeout).until(
            lambda d: any(
                (
                    "alert-active" in (e.get_attribute("class") or "")
                    and "clicked" in (e.get_attribute("class") or "")
                )
                for e in d.find_elements(*AVISE_DISABLED_ANY)
            )
        )

    driver.refresh()

    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(
            driver,
            [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY],
            timeout=timeout,
        )

    enabled = wait_any_visible(driver, AVISE_ENABLED_ANY, timeout=timeout)
    if not enabled:
        return False

    scroll_and_click(driver, enabled)

    if wait_click_class:
        wait(driver, timeout).until(
            lambda d: any(
                (
                    "alert-active" in (e.get_attribute("class") or "")
                    and "clicked" in (e.get_attribute("class") or "")
                )
                for e in d.find_elements(*AVISE_ENABLED_ANY)
            )
        )

    driver.refresh()

    if page_ready_locator:
        visible(driver, page_ready_locator, timeout=timeout)
    else:
        wait_visible_any(
            driver,
            [AVISE_DISABLED_ANY, AVISE_ENABLED_ANY],
            timeout=timeout,
        )

    disabled2 = wait_any_visible(driver, AVISE_DISABLED_ANY, timeout=timeout)
    return bool(disabled2)
