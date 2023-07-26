import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage



class DeveloperSettingsPage(BasePage):
    """Developer Settings page object"""

    # Locators
    on_this_page_text_locator = "Developer"
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    environment_locator = (AppiumBy.ID, "com.ariesbifold:id/environment")
    production_locator = (AppiumBy.ID, "com.ariesbifold:id/production")
    development_locator = (AppiumBy.ID, "com.ariesbifold:id/development")
    test_locator = (AppiumBy.ID, "com.ariesbifold:id/test")

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_env(self, env):
        if self.on_this_page():
            self.find_by(self.environment_locator).click()
            if env == 'Production':
                self.find_by(self.production_locator).click()
            elif env == 'Development':
                self.find_by(self.development_locator).click()
            elif env == 'Test':
                self.find_by(self.test_locator).click()
            # TODO check that the appopriate env is selected.
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        if self.on_this_page():
            self.find_by(self.back_locator).click()
            from pageobjects.bc_wallet.settings import SettingsPage
            return SettingsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")


