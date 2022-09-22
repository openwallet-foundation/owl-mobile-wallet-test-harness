from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.onboarding_biometrics import OnboardingBiometricsPage


class PINSetupPage(BasePage):
    """PIN Setup page object"""

    # Locators
    on_this_page_text_locator = "Remember your PIN"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/ReenterPIN")
    first_pin_locator = (AppiumBy.ID, "com.ariesbifold:id/EnterPIN")
    first_pin_visibility_locator = (
        AppiumBy.ID, "com.ariesbifold:id/EnterPINVisability")
    second_pin_locator = (AppiumBy.ID, "com.ariesbifold:id/ReenterPIN")
    second_pin_visibility_locator = (
        AppiumBy.ID, "com.ariesbifold:id/ReenterPINVisability")
    create_pin_button_tid_locator = (
        AppiumBy.ID, "com.ariesbifold:id/CreatePIN")
    modal_message_title_locator = (
        AppiumBy.ID, "com.ariesbifold:id/HeaderText")
    modal_message_body_locator = (AppiumBy.ID, "com.ariesbifold:id/BodyText")
    modal_message_ok_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_locator)

    def enter_pin(self, pin):
        if self.on_this_page():
            self.find_by(self.first_pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_pin(self):
        if self.on_this_page():
            # PIN must be visable.
            self.find_by(self.first_pin_visibility_locator).click()
            size = len(self.first_pin_locator[1])
            return self._construct_pin_from_boxes(self.first_pin_aid_locator[1][:size - 2])
        else:
            raise Exception(f"App not on the {type(self)} page")

    def enter_second_pin(self, pin):
        if self.on_this_page():
            self.find_by(self.second_pin_locator).click()
            self.find_by(self.second_pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_second_pin(self):
        if self.on_this_page():
            # PIN must be visable.
            self.find_by(self.second_pin_visibility_locator).click()
            size = len(self.second_pin_locator[1])
            return self._construct_pin_from_boxes(self.second_pin_aid_locator[1][:size - 2])
            # return self.find_by(self.second_pin_tid_locator).text
        else:
            raise Exception(f"App not on the {type(self)} page")

    def create_pin(self):
        if self.on_this_page():
            self.find_by(self.create_pin_button_tid_locator).click()

            # return the wallet initialization page
            return OnboardingBiometricsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def does_pin_match(self, header: str = "PINs do not match"):
        if self.on_this_page():
            if self.find_by(self.modal_message_title_locator).text == header:
                return True
            else:
                return False
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_ok_on_modal(self):
        # On Android the modal hides all the other PIN setup page elements, so we can't check on this page
        # if self.on_this_page():
        self.find_by(self.modal_message_ok_locator).click()

        return True
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def get_pin_error(self):
        # On Android the modal hides all the other PIN setup page elements, so we can't check on this page
        # if self.on_this_page():
        return self.find_by(self.modal_message_body_locator).text
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def _construct_pin_from_boxes(self, pin_locator, find_by=AppiumBy.ID, pin_length=6):
        pin = ""
        if find_by == AppiumBy.ID:
            find_by_routine = getattr(self, "find_by_element_id")
        else:
            find_by_routine = getattr(self, "find_by_accessibility_id")
        for i in range(pin_length):
            element_index = i + 1
            pin = pin + find_by_routine(f"{pin_locator}-{element_index}").text

        return pin
