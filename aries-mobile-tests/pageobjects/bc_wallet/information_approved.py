from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class InformationApprovedPage(BasePage):
    """Proof Information approved page object"""

    # Locators
    on_this_page_text_locator = "Information received"
    approval_locator = (AppiumBy.ID, "com.ariesbifold:id/SentProofRequest")
    done_locator = (AppiumBy.ID, "com.ariesbifold:id/Done")

    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_done(self):
        if self.on_this_page():
            self.find_by(self.done_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


