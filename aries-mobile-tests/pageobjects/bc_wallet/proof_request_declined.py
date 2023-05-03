from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class ProofRequestDeclinedPage(BasePage):
    """Proof Request Declined page object"""
    
    # Locators
    on_this_page_text_locator = "Proof request declined"
    done_locator = (AppiumBy.ID, "com.ariesbifold:id/Done")


    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)

    def select_done(self):
        if self.on_this_page():
            self.find_by(self.done_locator).click()
            from pageobjects.bc_wallet.home import HomePage
            return HomePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
