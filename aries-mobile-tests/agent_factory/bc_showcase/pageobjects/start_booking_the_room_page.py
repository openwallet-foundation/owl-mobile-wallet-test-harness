from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64


# These classes can inherit from a BasePage to do commone setup and functions
class StartBookingTheRoomPage(WebBasePage):
    """BC Wallet Showcase Start Booking the Room page object"""

    # Locators
    on_this_page_text_locator = "Imagine you're on the room booking page for BestBC College"
    qr_code_locator = (By.XPATH, "//div[@class='relative bg-none']//canvas")
    next_locator = (By.XPATH, "//button[normalize-space()='NEXT']")
    proof_success_locator = (By.XPATH, "(//p[normalize-space()='Success! You can continue.'])[1]")
    complete_locator = (By.XPATH, "(//button[contains(@class,'cursor-pointer dark:text-white')])[1]")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 

    def get_qr_code(self):
        try:
            qr_code = self.find_by(self.qr_code_locator, wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return qr_code


    def select_next(self): #-> ConnectWithBestBCCollegePage:
        try:
            self.find_by(self.next_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        #return ConnectWithBestBCCollegePage(self.driver)

    def proof_success(self) -> bool:
        try:
            self.find_by(self.proof_success_locator, wait_condition=WaitCondition.VISIBILITY_OF_ELEMENT_LOCATED)
            self.select_next()
            self.find_by(self.complete_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return True
        except Exception as e:
            return False