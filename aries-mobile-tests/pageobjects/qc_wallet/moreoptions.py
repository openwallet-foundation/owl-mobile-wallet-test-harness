from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.qc_wallet.settings import SettingsPageQC


class MoreOptionsPageQC(BasePage):
    """more options page object"""

    #Locators
    on_this_page_text_locator = "More Options"
    application_settings_locator = (AppiumBy.ID, "com.ariesbifold:id/AppParams")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_applicationSettings(self):
        if self.on_this_page():
            self.find_by(self.application_settings_locator).click()

            # return a new page object for the settings page
            return SettingsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
