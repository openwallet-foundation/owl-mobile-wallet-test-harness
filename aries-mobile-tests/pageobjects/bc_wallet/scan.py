import logging
from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition


# These classes can inherit from a BasePage to do common setup and functions
class ScanPage(BasePage):
    """Camera Scan page object"""

    # Locators
    close_locator = (AppiumBy.ID, "com.ariesbifold:id/ScanClose")
    flash_locator = (AppiumBy.ID, "com.ariesbifold:id/ScanTorch")
    error_locator = (AppiumBy.ID, "com.ariesbifold:id/ErrorText")

    def on_this_page(self):
        return super().on_this_page(self.close_locator)

    def get_error(self) -> str:
        return self.find_by(self.error_locator).text
        
    def select_close(self):
        if self.on_this_page():
            try:
                self.find_by(self.close_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            except:
                logging.warning("Soft Assert: Could not select close button on scan page. Assuming scan was successful and is connecting.")
            # This goes to the page that called it could be one of may app pages. Let the test handle it.
        else:
            # we may have already moved on from this page.
            logging.warning(f"Soft Assert: App not on the {type(self)} page. Assuming scan was successful and is connecting.")

    def select_flash(self):
        self.find_by(self.flash_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

