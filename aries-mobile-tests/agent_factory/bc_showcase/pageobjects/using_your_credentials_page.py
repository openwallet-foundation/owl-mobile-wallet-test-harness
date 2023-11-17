from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.getting_a_student_discount_page import GettingAStudentDiscountPage
from agent_factory.bc_showcase.pageobjects.book_a_study_room_page import BookAStudyRoomPage


# These classes can inherit from a BasePage to do commone setup and functions
class UsingYourCredentialsPage(WebBasePage):
    """BC Wallet Showcase Using Your Credentials page object"""

    # Locators
    on_this_page_text_locator = "You'll be asked to share"
    cool_clothes_online_start_locator = (By.XPATH, "(//button[@class='text-sm bg-bcgov-blue dark:bg-bcgov-white text-white dark:text-black w-24 h-8 py-1.5 px-4 rounded font-semibold shadow-sm opacity-100'][normalize-space()='START'])[1]")
    bestbc_online_start_locator = (By.XPATH, "(//button[@class='text-sm bg-bcgov-blue dark:bg-bcgov-white text-white dark:text-black w-24 h-8 py-1.5 px-4 rounded font-semibold shadow-sm opacity-100'][normalize-space()='START'])[2]")

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_cool_clothes_online_start(self) -> GettingAStudentDiscountPage:
        try:
            self.find_by(self.cool_clothes_online_start_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return GettingAStudentDiscountPage(self.driver)
    

    def select_bestbc_college_start(self) -> BookAStudyRoomPage:
        try:
            self.find_by(self.bestbc_online_start_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return BookAStudyRoomPage(self.driver)