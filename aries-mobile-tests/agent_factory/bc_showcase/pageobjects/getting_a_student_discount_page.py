from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.start_proving_youre_a_student_page import StartProvingYoureAStudentPage


# These classes can inherit from a BasePage to do commone setup and functions
class GettingAStudentDiscountPage(WebBasePage):
    """BC Wallet Showcase Getting a Student Discount page object"""

    # Locators
    on_this_page_text_locator = "get a student discount on her online purchase"
    start_locator = (By.XPATH, "(//button[normalize-space()='START'])[1]")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_start(self) -> StartProvingYoureAStudentPage:
        try:
            self.find_by(self.start_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return StartProvingYoureAStudentPage(self.driver)
    