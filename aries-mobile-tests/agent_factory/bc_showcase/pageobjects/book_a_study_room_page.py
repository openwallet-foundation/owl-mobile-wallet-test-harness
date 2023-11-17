from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.start_booking_the_room_page import StartBookingTheRoomPage


# These classes can inherit from a BasePage to do commone setup and functions
class BookAStudyRoomPage(WebBasePage):
    """BC Wallet Showcase Book a Study Room page object"""

    # Locators
    on_this_page_text_locator = "needs a study room for some peace and quiet"
    start_locator = (By.XPATH, "//button[normalize-space()='START']")

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_start(self) -> StartBookingTheRoomPage:
        try:
            self.find_by(self.start_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return StartBookingTheRoomPage(self.driver)
