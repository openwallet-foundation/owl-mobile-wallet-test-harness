import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import WaitCondition

# BasePage to do common setup and functions


class WebBasePage(object):
    """A base page object to do things common to all web based page objects"""

    def on_this_page(self, locator, timeout=10):
        if type(locator) is tuple:
            if self.find_by(locator, timeout):
                return True
            else:
                return False
        else:
            found_locator = False
            i = 0
            while found_locator == False and i < timeout:
                if locator in self.get_page_source():
                    found_locator = True
                else:
                    found_locator = False
                i = i + 1
            return found_locator

    # Initialize and define the type of driver as WebDriver

    def __init__(self, driver):
        self.driver = driver

    def find_by(self, locator_tpl: tuple, timeout=20, wait_condition:WaitCondition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED):
        try:
            return WebDriverWait(self.driver, timeout).until(
                wait_condition(
                    (locator_tpl[0], locator_tpl[1]))
            )
        except:
            #self.driver.save_screenshot(f"CouldNotFindElement_{locator_tpl[0]}.png")
            #print(self.driver.page_source)
            raise Exception(
                f"Could not find element {locator_tpl[0]} with Locator {locator_tpl[1]}")


    def find_multiple_by(self, locator_tpl: tuple, timeout=20):
        try:
            # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (locator_tpl[0], locator_tpl[1]))
            )
        except:
            raise Exception(
                f"Could not find elements {locator_tpl[0]} with Locator {locator_tpl[1]}")

    def get_page_source(self):
        return self.driver.page_source