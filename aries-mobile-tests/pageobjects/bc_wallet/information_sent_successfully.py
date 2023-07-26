from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class InformationSentSuccessfullyPage(BasePage):
    """Information Sent Successfully page object"""

    # Locators
    on_this_page_text_locator = "Information sent successfully"
    on_this_page_locator = (AppiumBy.ID, "com.ariesbifold:id/SentProofRequest")
    back_to_home_locator = (AppiumBy.ID, "com.ariesbifold:id/BackToHome")
    done_locator = (AppiumBy.ID, "com.ariesbifold:id/Done")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_locator)

    def select_back_to_home(self):
        if self.on_this_page():
            self.find_by(self.back_to_home_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_done(self):
        if self.on_this_page():
            self.find_by(self.done_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
