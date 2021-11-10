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
        