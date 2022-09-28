from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.credentials import CredentialsPage

class NavBar(BasePage):
    """Nav Bar Footer object"""

    # Locators
    scan_locator = (AppiumBy.ACCESSIBILITY_ID, "Scan")
    home_locator = (AppiumBy.ACCESSIBILITY_ID, "Home")
    credentials_locator = (AppiumBy.ACCESSIBILITY_ID, "Credentials")
    settings_locator = (AppiumBy.ACCESSIBILITY_ID, "Settings")


    def select_home(self):
        self.find_by(self.home_locator).click()
        return HomePage(self.driver)

    def select_scan(self):
        self.find_by(self.scan_locator).click()

        # return a new page object? The scan page.
        return ConnectingPage(self.driver)

    def select_credentials(self):
        self.find_by(self.credentials_locator).click()
        return CredentialsPage(self.driver)

    def select_settings(self):
        self.find_by(self.settings_locator).click()

        # return a new page objectfor the settings page
        return SettingsPage(self.driver)
