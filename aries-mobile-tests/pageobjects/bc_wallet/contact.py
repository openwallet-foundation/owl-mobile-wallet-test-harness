import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.contact_details import ContactDetailsPage


class ContactPage(BasePage):
    """Contact page object"""

    # Locator
    #on_this_page_text_locator = "Contacts"
    contact_locator = (AppiumBy.ID, "com.ariesbifold:id/Settings")
    

    def on_this_page(self):     
        return super().on_this_page(self.contact_locator) 

    def select_info(self):
        if self.on_this_page():
            self.find_by(self.contact_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

            # return a new page object for the Contacts page
            return ContactDetailsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)}") 


