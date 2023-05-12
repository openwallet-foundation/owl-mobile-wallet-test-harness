import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.developer_settings import DeveloperSettingsPage
from pageobjects.bc_wallet.contacts import ContactsPage


class SettingsPage(BasePage):
    """Settings page object"""

    # Locators
    on_this_page_text_locator = "App Settings"
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    contacts_locator = (AppiumBy.ID, "com.ariesbifold:id/Contacts")
    version_locator = (AppiumBy.ID, "com.ariesbifold:id/Version")
    version_partial_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Version")
    intro_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Introduction to the app")
    intro_locator = (AppiumBy.ID, "com.ariesbifold:id/IntroductionToTheApp")
    developer_locator = (AppiumBy.ID, "com.ariesbifold:id/DeveloperOptions")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def enable_developer_mode(self):
        # TODO check if Developer Mode is already enabled

        # Check if the app is on the correct page
        if not self.on_this_page():
            raise Exception(f"App not on the {type(self)} page")

        self.scroll_to_bottom()
        #version_element = self.find_by(self.version_locator)
        if self.current_platform == "iOS" and self.driver.capabilities['platformVersion'] <= '15':
            # Need to find the element py partial text or accessibility id for iOS 14 and lower
            version_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@label, '{}')]".format(self.version_partial_aid_locator[1]))
            # take the last one on the page
            version_element = version_elements[len(version_elements)-1]
        else:
            # this works for iOS 15+ and Android only
            version_element = self.find_by(self.version_locator)

        # Click the version element 10 times to enable Developer Mode
        for i in range(10):
            version_element.click()

        # TODO: check if Developer Mode is now enabled


    def select_developer(self):
        #if self.on_this_page():
        self.find_by(self.developer_locator).click()

        return DeveloperSettingsPage(self.driver)
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_back(self):
        # Don't check if on this page becasue android (unless you scroll back to the top) can't see the App Settings accessibility ID
        # if self.on_this_page():
        self.find_by(self.back_locator).click()
        from pageobjects.bc_wallet.home import HomePage
        return HomePage(self.driver)
        # else:
        #     raise Exception(f"App not on the {type(self)} page")

    def select_notification(self, context):
        search_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()
        search_input = WebDriverWait(context.driver, 30).until(
            EC.element_to_be_clickable((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        search_input.send_keys(keyword)
        time.sleep(5)

    def select_contacts(self):
        if self.on_this_page():
            self.find_by(self.contacts_locator).click()

            # return a new page object for the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}") 


    def select_scan(self):
        if self.on_this_page():
            # Inject image 
            self.find_by_accessibility_id(self.scan_locator).click()

            # return a new page object? The scan page.
            return ConnectingPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page") 


    def select_credentials(self):
        
        return CredentialsPage

    def select_settings(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.settings_locator).click()

            # return a new page objectfor the settings page
            return SettingsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page") 
        #return SettingsPage
