import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BasePage to do common setup and functions
class BasePage(object):
    """A base page object to do things common to all page objects"""

    device = ""

    def back(self, context):
        pass


    def set_device(self, context):
        self.device = context.browser
        
    def on_the_right_page(self, context, title):
        title_element = WebDriverWait(self.device, 10).until(
            EC.title_is(title))
        if title_element.name() == title:
            return True
        else:
            return False
