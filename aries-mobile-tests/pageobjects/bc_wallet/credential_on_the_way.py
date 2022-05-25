from appium.webdriver.common.mobileby import MobileBy
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class CredentialOnTheWayPage(BasePage):
    """Credential is on its way page object"""

    # Locators
    on_this_page_text_locator = "Your credential is on the way"
    home_locator = (MobileBy.ID, "com.ariesbifold:id/BackToHome")
    #cancel_locator = "Cancel"

    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_home(self):
        if self.on_this_page():
            self.find_by(self.home_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    # def select_cancel(self):
    #     if self.on_this_page():
    #         self.find_by_accessibility_id(self.cancel_locator).click()
    #         from pageobjects.bc_wallet.home import HomePage
    #         return HomePage(self.driver)
    #     else:
    #         raise Exception(f"App not on the {type(self)} page")
