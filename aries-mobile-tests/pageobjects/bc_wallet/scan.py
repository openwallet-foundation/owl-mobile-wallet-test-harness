import logging

from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition


# These classes can inherit from a BasePage to do common setup and functions
class ScanPage(BasePage):
    """Camera Scan page object"""

    # Locators
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    close_locator = (AppiumBy.ID, "com.ariesbifold:id/ScanClose")
    flash_locator = (AppiumBy.ID, "com.ariesbifold:id/ScanTorch")
    error_locator = (AppiumBy.ID, "com.ariesbifold:id/ErrorText")

    def on_this_page(self):
        return super().on_this_page(self.flash_locator)

    def get_error(self) -> str:
        return self.find_by(self.error_locator).text

    def select_close(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
        else:
            # we may have already moved on from this page.
            logging.warning(
                f"Soft Assert: App not on the {type(self)} page. Assuming scan was successful and is connecting."
            )

    def select_flash(self):
        self.find_by(
            self.flash_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
        ).click()
