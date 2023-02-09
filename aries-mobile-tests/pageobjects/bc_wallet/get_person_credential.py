from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition



# These classes can inherit from a BasePage to do common setup and functions
class GetPersonCredentialPage(BasePage):
    """Get Person Credential page object"""

    # Locators
    on_this_page_text_locator = "Person Credential"
    get_your_person_credential_locator = (AppiumBy.ACCESSIBILITY_ID, "Get your Person credential")
    get_this_later_locator = (AppiumBy.ACCESSIBILITY_ID, "Get this later")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_get_your_person_credential(self, scroll=False):
        if self.on_this_page():
            self.find_by(self.get_your_person_credential_locator).click()
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_decline(self):
        if self.on_this_page():
            self.find_by(self.get_this_later_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

