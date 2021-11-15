import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects import BasePage

# These classes can inherit from a BasePage to do commone setup and functions
class TermsOfServicePage(BasePage):
    """A sample test class to show how page object works"""

    # def __init__ (self, context):
    #     #self.device = context.browser
    #     self.context = context

    #def __init__ (self):

    #iOS Locators
    # terms_of_service_agree = self.device.find_element_by_id("2F000000-0000-0000-F31B-000000000000")
    # submit_button = self.device.find_element_by_id("2A000000-0000-0000-F31B-000000000000")

    #Android Locators

    def select_accept(self, context):
        # if self.on_the_right_page(context, "Terms of Service"):
            
        # else:
            

        # search_element = WebDriverWait(context.browser, 10).until(
        #     EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        # )
        # search_element.click()
        # search_input = WebDriverWait(context.browser, 30).until(
        #     EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        # )
        # search_input.send_keys(keyword)
        time.sleep(5)

    def submit(self, context):
        elems = context.browser.find_elements_by_class_name("android.widget.TextView")
        return elems