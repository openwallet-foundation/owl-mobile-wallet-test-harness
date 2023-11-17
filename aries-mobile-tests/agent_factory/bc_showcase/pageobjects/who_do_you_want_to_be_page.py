from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.lets_get_started_page import LetsGetStartedPage


# These classes can inherit from a BasePage to do commone setup and functions
class WhoDoYouWantToBePage(WebBasePage):
    """BC Wallet Showcase Who Do You Want to Be page object"""

    # Locators
    on_this_page_text_locator = "Who do you want to be" or "Meet Alice" or "Meet Joyce"
    student_locator = (By.XPATH, "//img[@alt='Alice']")
    lawyer_locator = (By.XPATH, "//img[@class='m-auto h-16 w-16 p-2 sm:h-20 sm:w-20 md:h-24 md:w-24 md:p-4 lg:h-36 lg:w-36 lg:p-8 rounded-full bg-bcgov-white dark:bg-bcgov-black my-6 shadow shadow-xl ring-4 ring-bcgov-gold']")
    next_locator = (By.XPATH, "//button[normalize-space()='NEXT']")


    def on_this_page(self):     
        #return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.student_locator, timeout=20) or super().on_this_page(self.lawyer_locator, timeout=20)

    def select_student(self):
        try:
            self.find_by(self.student_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
    
    def select_lawyer(self):
        try:
            self.find_by(self.lawyer_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e

    def select_next(self) -> LetsGetStartedPage:
        try:
            self.find_by(self.next_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return LetsGetStartedPage(self.driver)
