import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.contacts import ContactsPage
from pageobjects.bc_wallet.connecting import ConnectingPage


class SettingsPage(BasePage):
    """Home page object"""

    # Locators
    on_this_page_text_locator = "App Preferences"
    back_locator = "Go Back"
    contacts_locator = "Contacts"

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_notification(self, context):
        search_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()
        search_input = WebDriverWait(context.driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        search_input.send_keys(keyword)
        time.sleep(5)


    def select_contacts(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.contacts_locator).click()

            # return a new page objectfor the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}") 
        #return ContactsPage

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
