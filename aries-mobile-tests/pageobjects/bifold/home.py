import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bifold.contacts import ContactsPage
from device_service_handler.device_service_handler_interface import DeviceServiceHandlerInterface


class HomePage(BasePage):
    """Home page object"""

    # Locators
    title_locator = "Home"
    home_locator = "Home"
    scan_locator = "Scan"
    credentials_locator = "Credentials"
    settings_locator = "Settings"
    contacts_locator = "Contacts"

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
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.contacts_locator).click()

            # return a new page objectfor the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page") 
        #return ContactsPage


    def select_scan(self):
        if self.on_the_right_page(self.title_locator):
            # Inject image 
            self.find_by_accessibility_id(self.scan_locator).click()

            # return a new page object? The scan page.
            #return ScanPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page") 


    def select_credentials(self):
        
        return CredentialsPage

    def select_settings(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.settings_locator).click()

            # return a new page objectfor the settings page
            #return SettingsPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page") 
        #return SettingsPage
