from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from pageobjects.basepage import WaitCondition


class ChangePINPage(PINSetupPage):
    """PIN Change page object"""

    # Locators
    on_this_page_text_locator = "Change your PIN"
    change_pin_button_locator = (
        AppiumBy.ID, "com.ariesbifold:id/ChangePIN")
    old_pin_locator = (AppiumBy.ID, "com.ariesbifold:id/EnterOldPIN")

    def __init__(self, driver):
        super().__init__(driver)
        # Instantiate possible Modals and Alerts for this page
        self.successfully_changed_pin_modal = SuccessfullyChangedPINModal(driver)

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
        
class SuccessfullyChangedPINModal(BasePage):
    """Successully Changed PIN Modal page object"""

    # Locators
    on_this_page_text_locator = "Successfully changed your PIN"
    success_title_locator = (AppiumBy.ID, "com.ariesbifold:id/HeaderText")
    success_details_locator = (AppiumBy.ID, "com.ariesbifold:id/BodyText")
    okay_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay") 

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)
    
    def is_displayed(self):
        return self.on_this_page()

    def get_success_title(self) -> str:
        return self.find_by(self.success_title_locator).text
        
    def get_success_message(self) -> str:
        return self.find_by(self.success_details_locator).text

    def select_okay(self):
        self.find_by(self.okay_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        from pageobjects.bc_wallet.settings import SettingsPage
        return SettingsPage(self.driver)