import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class InformationSentSuccessfullyPage(BasePage):
    """Information Sent Successfully page object"""

    # Locators
    on_this_page_text_locator = "Information sent successfully"
    back_to_home_locator = "Go back to home"
    done_locator = (MobileBy.ID, "com.ariesbifold:id/Done")

    def on_this_page(self):
        print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_back_to_home(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.back_to_home_locator).click()
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
