from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.pinsetup import PINSetupPage
from pageobjects.qc_wallet.onboarding_biometrics import OnboardingBiometricsPageQC
import logging


class PINSetupPageQC(PINSetupPage):
    """PIN Setup page QC object"""

    on_this_page_text_locator = "Create a PIN to secure your wallet"
    first_pin_visibility_locator = (
        AppiumBy.ID,
        "com.ariesbifold:id/Show",
    )
    second_pin_visibility_locator = (
        AppiumBy.ID,
        "com.ariesbifold:id/Show",
    )
    create_pin_button_tid_locator = (AppiumBy.ID, "com.ariesbifold:id/CreatePIN")
    modal_message_body_locator = (AppiumBy.ID, "com.ariesbifold:id/InlineErrorText")
    error_message_pin_locator = (AppiumBy.XPATH, "//*[@resource-id='com.ariesbifold:id/InlineErrorText']")


    def __init__(self, driver):
        super().__init__(driver)

    def enter_pin(self, pin):
        first_pin = self.find_by(self.first_pin_locator)
        if self.on_this_page():
            first_pin.click()
            first_pin.send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")
    
    def enter_second_pin(self, pin):
        second_pin = self.find_by(self.second_pin_locator)
        if self.on_this_page():
            second_pin.click()
            second_pin.send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")


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
                x = int(int(screen_size["width"]) * 0.5)
                y = int(int(screen_size["height"]) * 0.2)
                touch_action = TouchAction(self.driver)
                touch_action.tap(x=x, y=y).perform()
                self.find_by(self.create_pin_button_tid_locator).click()
                self.find_by(self.modal_message_ok_locator)
            except:
                raise Exception(
                    "Unable to locate create pin button and modal error box"
                )
        else:
            raise Exception(f"App not on the {type(self)} page")

    def create_pin(self):
        if self.on_this_page():
            el_visible = self.is_element_visible(self.create_pin_button_tid_locator)
            timeout = 30
            while not el_visible and timeout > 0:
                self.swipe_down()
                el_visible = self.is_element_visible(self.create_pin_button_tid_locator)
                timeout -= 1
            self.find_by(self.create_pin_button_tid_locator).click()
            # Maybe should check if it is checked or let the test call is_accept_checked()?
            # return a new page object? The Pin Setup page.
        else:
            raise Exception(f"App not on the {type(self)} page")


        # return the wallet enable notifications page
        return OnboardingBiometricsPageQC(self.driver)

    def select_ok_on_modal(self):
        # On Android the modal hides all the other PIN setup page elements, so we can't check on this page
        # if self.on_this_page():
        self.find_by(
            self.modal_message_ok_locator,
            timeout=30,
            wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE,
        ).click()

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

    def get_error(self):
        # On Android the modal hides all the other PIN setup page elements, so we can't check on this page
        # if self.on_this_page():        
        return self.find_by(self.modal_message_body_locator).text
        # else:
        #     raise Exception(f"App not on the {type(self)} page")