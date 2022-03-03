import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# BasePage to do common setup and functions


class BasePage(object):
    """A base page object to do things common to all page objects"""

    def back(self, context):
        pass

    def set_device(self, context):
        self.driver = context.driver

    def on_this_page(self, locator, timeout=10):

        # replace this sleep when there is an accessibility id on page titles.
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
        self.current_platform = driver.capabilities['platformName']

    # Locate by Accessibility id
    def find_by_accessibility_id(self, locator, timeout=20):
        try:
	        # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(
                    (MobileBy.ACCESSIBILITY_ID, locator))
            )
        except:
            try:
                # If there is a problem with the accessibility id, try doing it by name.
                # return WebDriverWait(self.driver, 20).until(
                #     EC.presence_of_element_located((MobileBy.NAME, locator))
                # )
                return self.driver.find_element_by_name(locator)
            except:
                raise Exception(
                    f"Could not find element by Accessibility id or Name Locator {locator}")

    # Locate multiple elements by Accessibility id.
    # this is a workaround for when iOS may have translated the labels down into text and input fields.
    # we shouldn't be calling this very much, and when we have to, we should log an issue with the wallet for unique accessibilituy IDs
    def find_multiple_by_accessibility_id(self, locator, timeout=20):
        try:
	        # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (MobileBy.ACCESSIBILITY_ID, locator))
            )
        except:
            raise Exception(
                f"Could not find elements by Accessibility id {locator}")

    # Locate by id
    def find_by_element_id(self, locator):
        try:
	        # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((MobileBy.ID, locator))
            )
        except:
            raise Exception(
                f"Could not find element by element id Locator {locator}")

    def get_page_source(self):
        return self.driver.page_source

    # Positioning according to xpath
    def find_by_xpath(self, locator):
        try:
	    # The location of a single element gets the location of a single element
            return self.driver.find_element_by_xpath(locator)
        except:
	    # To locate multiple same xpath elements, you can get a list. You can use the list query for the location of a specific element (xpath is the only location, generally it is not necessary to use this method)
            return self.driver.find_elements(locator)

    # Positioning according to classname
    def find_by_classname(self, *locator):
	# classname location is rarely used. It is generally used when id location and xpath location cannot be used. What you get is a list. You can use the list to query the location of a specific element
        return self.driver.find_elements_by_class_name(*locator)
