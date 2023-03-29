import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage


class ContactsPage(BasePage):
    """Contacts page object"""

    # Locators
    on_this_page_text_locator = "Contacts"
    contact_locator = (AppiumBy.ID, "com.ariesbifold:id/Contact")

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def select_contact(self, name:str):
        if self.on_this_page():
            contact_locator = (AppiumBy.ACCESSIBILITY_ID, name)
            self.find_by(self.contacts_locator).click()

            # return a new page object for the Contacts page
            return ContactsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}") 


