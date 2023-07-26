import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage

class ContactsPage(BasePage):
    """Contacts page object"""

    # Locators
    title_locator = "Contacts"
    contact_locator = "hmmm"

    def select_contact(self):
        if self.on_the_right_page(self.title_locator):
            self.find_by_accessibility_id(self.contact_locator).click()

            # return a new page objectfor the Contacts page
            #return ContactPage(self.driver)
        else:
            raise Exception(f"App not on the {self.title_locator} page") 
        #return ContactPage


