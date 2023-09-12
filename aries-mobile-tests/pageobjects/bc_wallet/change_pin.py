from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage


class ChangePINPage(PINSetupPage):
    """PIN Change page object"""

    # Locators
    on_this_page_text_locator = "Change your PIN"
    change_pin_button_locator = (
        AppiumBy.ID, "com.ariesbifold:id/ChangePIN")
    old_pin_locator = (AppiumBy.ID, "com.ariesbifold:id/EnterOldPIN")

    def on_this_page(self):
        return BasePage.on_this_page(self, self.on_this_page_text_locator)

    def enter_old_pin(self, pin):
        if self.on_this_page():
            self.find_by(self.old_pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_change_pin(self):
        if self.on_this_page():
            self.find_by(self.change_pin_button_locator).click()

            # Not sure what happens here yet
            #return OnboardingBiometricsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")