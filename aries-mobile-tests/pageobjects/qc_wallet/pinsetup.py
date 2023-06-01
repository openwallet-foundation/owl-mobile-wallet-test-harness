from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.onboarding_biometrics import OnboardingBiometricsPage
from pageobjects.bc_wallet.pinsetup import PINSetupPage


class PINSetupPageQC(PINSetupPage):
    """PIN Setup page QC object"""

    # Locators
    first_pin_visibility_locator = (
        AppiumBy.ID, "com.ariesbifold:id/Show")
    second_pin_visibility_locator = (
        AppiumBy.ID, "com.ariesbifold:id/Show")


    def __init__(self, driver):
        super().__init__(driver)
    
    def get_pin(self):
        if self.on_this_page():
            # PIN must be visable.
            self.find_by(self.first_pin_visibility_locator).click()
            return self.find_by(self.first_pin_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_second_pin(self):
        if self.on_this_page():
            # PIN must be visable.
            self.find_by(self.second_pin_visibility_locator).click()
            return self.find_by(self.second_pin_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")
    
    def create_pin_throw_error(self):
        if self.on_this_page():
            try:
                screen_size = self.driver.get_window_size()
                x = int(int(screen_size['width']) * 0.5)
                y=int(int(screen_size['height']) * 0.2)
                touch_action = TouchAction(self.driver)
                touch_action.tap(x=x, y=y).perform()
                self.find_by(self.create_pin_button_tid_locator).click()
                self.find_by(self.modal_message_ok_locator)
            except:
                raise Exception("Unable to locate create pin button and modal error box")
        else:
            raise Exception(f"App not on the {type(self)} page")

    def create_pin(self):
        return super().create_pin()

    def select_ok_on_modal(self):
        # On Android the modal hides all the other PIN setup page elements, so we can't check on this page
        # if self.on_this_page():
        self.find_by(self.modal_message_ok_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

        return True
        # else:
        #     raise Exception(f"App not on the {type(self)} page

    def does_pin_match(self, header: str = "PINs do not match"):
        if self.on_this_page():
            if self.find_by(self.modal_message_title_locator).text == header:
                return True
            else:
                return False
        else:
            raise Exception(f"App not on the {type(self)} page")
