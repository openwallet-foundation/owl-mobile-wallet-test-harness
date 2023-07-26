from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By

# These classes can inherit from a BasePage to do commone setup and functions
class AuthCodePage(WebBasePage):
    """BC VP Issuer GitHub Auth Code page object"""

    # Locators
    on_this_page_text_locator = "Device verification"
    auth_code_locator = (By.ID, 'otp')

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def enter_auth_code(self, auth_code):
        if self.on_this_page():
            self.find_by(self.auth_code_locator).send_keys(auth_code)
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")
    