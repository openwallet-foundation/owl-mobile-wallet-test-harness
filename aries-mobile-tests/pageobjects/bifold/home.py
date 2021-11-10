import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects import BasePage

class HomePage(BasePage):
    """A sample test class to show how page object works"""

    # def __init__ (self, context):
    #     #self.device = context.browser
    #     self.context = context

    #def __init__ (self):

    def select_notification(self, context):
        search_element = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()
        search_input = WebDriverWait(context.browser, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        search_input.send_keys(keyword)
        time.sleep(5)


    def select_contacts(self, context):
        
        return ContactsPage


    def select_scan(self, context):
        
        return ScanPage


    def select_credentials(self, context):
        
        return CredentialsPage

    def select_settings(self, context):
        
        return SettingsPage
