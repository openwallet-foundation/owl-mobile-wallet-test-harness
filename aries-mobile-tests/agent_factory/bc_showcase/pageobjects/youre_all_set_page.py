from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.using_your_credentials_page import UsingYourCredentialsPage


# These classes can inherit from a BasePage to do commone setup and functions
class YoureAllSetPage(WebBasePage):
    """BC Wallet Showcase Your All Set page object"""

    # Locators
    on_this_page_text_locator = "you’ve just received your first digital credentials"
    finish_locator = (By.XPATH, "//button[normalize-space()='FINISH']")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_finish(self) -> UsingYourCredentialsPage:
        try:
            self.find_by(self.finish_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return UsingYourCredentialsPage(self.driver)