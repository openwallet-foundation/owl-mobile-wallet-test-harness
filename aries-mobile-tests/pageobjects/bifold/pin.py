import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bifold.home import HomePage

class PINPage(BasePage):
    """A sample test class to show how page object works"""

    # def __init__ (self, context):
    #     #self.device = context.driver
    #     self.context = context

    #def __init__ (self):

    def enter_pin(self, context, pin):
        search_element = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        )
        search_element.click()
        search_input = WebDriverWait(context.driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        )
        search_input.send_keys(keyword)
        time.sleep(5)

    def submit_pin(self, context:
        thisHomePage = context.driver.find_elements_by_class_name("android.widget.TextView")
        return thisHomePage