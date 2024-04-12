from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.youre_all_set_page import YoureAllSetPage


# These classes can inherit from a BasePage to do commone setup and functions
class ConnectWithBestBCCollegePage(WebBasePage):
    """BC Wallet Showcase Connect With Best BC College page object"""

    # Locators
    on_this_page_text_locator = "Use your BC Wallet to scan the QR code from the website"
    qr_code_locator = (By.XPATH, "//div[@class='relative bg-none']//canvas")
    i_already_have_my_credential_locator = (By.XPATH, "//button[normalize-space()='I Already Have my Credential']")
    next_locator = (By.XPATH, "//button[normalize-space()='NEXT']")


    def on_this_page(self):     
        self.wait_for_page_load_complete()
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

    def select_i_already_have_my_credential(self):
        if self.on_this_page():
            self.find_by(self.i_already_have_my_credential_locator).click()
            return YoureAllSetPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_next(self): #-> ConnectWithBestBCCollegePage:
        if self.on_this_page():
            self.find_by(self.next_locator).click()
            #return ConnectWithBestBCCollegePage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
