import os

from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage


class BiometricsPage(BasePage):
    """Biometrics enter page object"""

    # Locators
    on_this_page_text_locator = "Biometrics"
    on_this_page_locator = (AppiumBy.NAME, "Biometrics")

    def on_this_page(self, language="English"):
        # print(self.driver.page_source)
        timeout = 50
        if "Local" in os.environ["DEVICE_CLOUD"]:
            timeout = 100
        # if self.current_platform.lower() == "Android".lower():
        return super().on_this_page(self.on_this_page_text_locator, timeout)
        # return super().on_this_page(self.on_this_page_locator, timeout)