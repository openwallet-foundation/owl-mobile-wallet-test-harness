import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects import BasePage

class PINSetupPage(BasePage):
    """A sample test class to show how page object works"""

    # def __init__ (self, context):
    #     #self.device = context.browser
    #     self.context = context

    #def __init__ (self):

    first_pin = self.device.find_element_by_id("43000000-0000-0000-F31B-000000000000")
    second_pin = self.device.find_element_by_id("75000000-0000-0000-F31B-000000000000")
    create_pin_button = self.device.find_element_by_id("70000000-0000-0000-F31B-000000000000")

    def enter_pin(self, context, pin):
        search_element = WebDriverWait(context.browser, 10).until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()
        search_input = WebDriverWait(context.browser, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        search_input.send_keys(keyword)
        time.sleep(5)

    def enter_second_pin(self, context, pin):
        elems = context.browser.find_elements_by_class_name("android.widget.TextView")
        return elems

    def create_pin(self, context):
        elems = context.browser.find_elements_by_class_name("android.widget.TextView")
        return elems    
