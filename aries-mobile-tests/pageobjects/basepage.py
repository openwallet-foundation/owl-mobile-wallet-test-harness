import time
from enum import Enum
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import xml.etree.ElementTree as ET

class WaitCondition(Enum):
    ELEMENT_TO_BE_CLICKABLE = EC.element_to_be_clickable
    PRESENCE_OF_ELEMENT_LOCATED = EC.presence_of_element_located
    VISIBILITY_OF_ELEMENT_LOCATED = EC.visibility_of_element_located
    INVISIBILITY_OF_ELEMENT_LOCATED = EC.invisibility_of_element_located

# BasePage to do common setup and functions
class BasePage(object):
    """A base page object to do things common to all page objects"""

    def back(self, context):
        pass

    def set_device(self, context):
        self.driver = context.driver

    def on_this_page(self, locator, timeout=10):
        if type(locator) is tuple:
            try:
                self.find_by(locator, timeout)
                return True
            except:
                return False
            # if self.find_by(locator, timeout):
            #     return True
            # else:
            #     return False
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
        self.current_platform = driver.capabilities['platformName']

    def find_by(self, locator_tpl: tuple, timeout=20, wait_condition:WaitCondition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED):
        if locator_tpl[0] == MobileBy.ACCESSIBILITY_ID or locator_tpl[0] == AppiumBy.ACCESSIBILITY_ID:
            return self.find_by_accessibility_id(locator_tpl[1], timeout, wait_condition)
        elif locator_tpl[0] == MobileBy.ID or locator_tpl[0] == AppiumBy.ID:
            return self.find_by_element_id(locator_tpl[1], timeout, wait_condition)


    def find_multiple_by(self, locator_tpl: tuple, timeout=20):
        if locator_tpl[0] == MobileBy.ACCESSIBILITY_ID or locator_tpl[0] == AppiumBy.ACCESSIBILITY_ID:
            return self.find_multiple_by_accessibility_id(locator_tpl[1], timeout)
        elif locator_tpl[0] == MobileBy.ID or locator_tpl[0] == AppiumBy.ID:
            # It may be that Android will return none when looking for multiple
            # so if we get an empty element array here try find_by instead.
            elems = self.find_multiple_by_id(locator_tpl[1], timeout)
            if len(elems) == 0:
                elem = self.find_by_element_id(locator_tpl[1], timeout)
                elems.append(elem)
            return elems
            #return self.find_multiple_by_id(locator_tpl[1], timeout)

    # Locate by Accessibility id
    def find_by_accessibility_id(self, locator, timeout=20, wait_condition:WaitCondition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED):
        try:
            # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                wait_condition(
                    (AppiumBy.ACCESSIBILITY_ID, locator))
            )
        except:
            # try:
            #     # If there is a problem with the accessibility id, try doing it by name.
            #     # return WebDriverWait(self.driver, 20).until(
            #     #     EC.presence_of_element_located((MobileBy.NAME, locator))
            #     # )
            #     return self.driver.find_element_by_name(locator)
            # except:
            raise Exception(
                f"Could not find element by Accessibility id Locator {locator}")

    # Locate multiple elements by Accessibility id.
    # this is a workaround for when iOS may have translated the labels down into text and input fields.
    # we shouldn't be calling this very much, and when we have to, we should log an issue with the wallet for unique accessibilituy IDs
    def find_multiple_by_accessibility_id(self, locator, timeout=20):
        try:
            # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (AppiumBy.ACCESSIBILITY_ID, locator))
            )
        except:
            raise Exception(
                f"Could not find elements by Accessibility id {locator}")

    # Locate multiple elements by id.
    def find_multiple_by_id(self, locator, timeout=20):
        try:
            # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (AppiumBy.ID, locator))
            )
        except:
            raise Exception(
                f"Could not find elements by id {locator}")

    # Locate by id
    def find_by_element_id(self, locator, timeout=20, wait_condition:WaitCondition=WaitCondition.PRESENCE_OF_ELEMENT_LOCATED):
        try:
            # The location of a single element gets the location of a single element
            return WebDriverWait(self.driver, timeout).until(
                wait_condition((AppiumBy.ID, locator))
            )
        except TimeoutException:
            raise
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

    # def scroll_to_element(self, locator, incremental_scroll_amount=500, timeout=20, find_by=MobileBy.ACCESSIBILITY_ID):
    #     """ deprecated """
    #     element = None
    #     i = 0
    #     while element == None and i < timeout:
    #         try: 
    #             if find_by == MobileBy.ACCESSIBILITY_ID:
    #                 element = self.find_by_accessibility_id(locator)
    #             else:
    #                 element = self.find_by_element_id(locator)
    #             self.driver.swipe(500, incremental_scroll_amount, 500, 100)
    #         except:
    #             # not found try again
    #             i = i + 1
    #     if element:
    #         return True
    #     else:
    #         return False

    def scroll_to_element(self, locator, direction='down'):
        """ Scroll to the element based on the accessibility id given. """
        """ The locator MUST be an accessibility id. """
        """ Can give a direction and the direction only applies to iOS. Default is down. """
        
        # Works great for Android, but iOS has different parameters
        if self.current_platform == "Android":
            self.driver.execute_script('mobile: scroll', {"strategy": 'accessibility id', "selector": locator})
        else:
            # Message: Mobile scroll supports the following strategies: name, direction, predicateString, and toVisible. Specify one of these
            # iOS
            el = self.driver.find_element(MobileBy.ACCESSIBILITY_ID, locator)
            self.driver.execute_script("mobile: scroll", {"direction": direction, 'element': el})

    def scroll_to_bottom(self):
        # Get the screen size
        screen_size = self.driver.get_window_size()
        screen_height = screen_size['height']

        # Scroll down the page until the bottom is reached
        while True:
            if self.current_platform == 'iOS':
                before_source_ios = self.driver.page_source
                self.driver.execute_script('mobile: scroll', {'direction': 'down'})
            else:
                # Scroll for android takes an accessibility id, however it will scroll to the bottom looking for that id and if it doesn't exist,
                # will throw and error. If we give it a non-existent accessibility id, and catch the error and continue we should be at the bottom.
                try:
                    self.scroll_to_element("this element doesn't exist, it is here to make android scroll to the bottom")
                except:
                    pass

            # Get the current scroll position
            if self.current_platform == 'iOS':
                after_source_ios = self.driver.page_source
                # Parse the hierarchies using an XML parser
                root = ET.fromstring(before_source_ios.encode('utf-8'))
                new_root = ET.fromstring(after_source_ios.encode('utf-8'))
                if ET.tostring(root) == ET.tostring(new_root):
                    break
            else:
                window_rect = self.driver.get_window_rect()
                current_scroll_position = window_rect['y'] + screen_height

                # Check if the bottom of the page has been reached
                if current_scroll_position >= screen_size['height']:
                    break
