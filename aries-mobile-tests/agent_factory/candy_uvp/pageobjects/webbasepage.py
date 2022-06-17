import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BasePage to do common setup and functions


class WebBasePage(object):
    """A base page object to do things common to all web based page objects"""

    def on_this_page(self, locator, timeout=10):
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

    def find_by(self, locator_tpl: tuple, timeout=20):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (locator_tpl[0], locator_tpl[1]))
            )
        except:
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