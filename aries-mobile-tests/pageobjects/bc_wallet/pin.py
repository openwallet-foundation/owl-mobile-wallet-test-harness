from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition
from pageobjects.bc_wallet.initialization import InitializationPage


class PINPage(BasePage):
    """PIN Entry page object"""

    # Locators
    on_this_page_text_locator = "Enter PIN"
    pin_locator = (AppiumBy.ID, "com.ariesbifold:id/EnterPIN")
    pin_visibility_locator = (AppiumBy.ID, "com.ariesbifold:id/Show")
    enter_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Enter")
    modal_message_ok_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay")
    modal_message_title_locator = (AppiumBy.ID, "com.ariesbifold:id/HeaderText")

    def on_this_page(self, language="English"):
        self.on_this_page_text_locator = (
            "Enter PIN" if language == "English" else "Entrer le NIP"
        )
        return super().on_this_page(self.on_this_page_text_locator, 50)

    def enter_pin(self, pin):
        if self.on_this_page():
            self.find_by(self.pin_locator).send_keys(pin)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_ok_on_modal(self):
        # On Android the modal hides all the other PIN page elements, so we can't check on this page
        self.find_by(
            self.modal_message_ok_locator,
            timeout=30,
            wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED,
        ).click()

        return True

    def get_error(self):
        # On Android the modal hides all the other PIN page elements, so we can't check on this page
        # if self.on_this_page():
        return self.find_by(self.modal_message_title_locator).text
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_enter(self):
        if self.on_this_page():
            self.find_by(self.enter_button_locator).click()

            # return the wallet initialization page
            return InitializationPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
