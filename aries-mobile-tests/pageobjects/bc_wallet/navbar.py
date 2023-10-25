from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.credentials import CredentialsPage

class NavBar(BasePage):
    """Nav Bar Footer object"""

    # Locators
    scan_locator = (AppiumBy.ID, "com.ariesbifold:id/Scan")
    notifications_locator = (AppiumBy.ID, "com.ariesbifold:id/Notifications")
    credentials_locator = (AppiumBy.ID, "com.ariesbifold:id/Credentials")
    settings_locator = (AppiumBy.ID, "com.ariesbifold:id/Settings")
    notification_locator = (AppiumBy.ID, "com.ariesbifold:id/Notification")
    

    def select_home(self):
        self.find_by(self.notifications_locator).click()
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

    def has_notification(self):
        try:
            # get the home element and check for the word notifications on the element text.
            notifications_element = self.find_by(self.notifications_locator)
            if "0 Notifications" in notifications_element.text:
                return False
            else:
                return True
        except:
            return False