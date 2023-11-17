from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.connect_with_best_bc_college_page import ConnectWithBestBCCollegePage


# These classes can inherit from a BasePage to do commone setup and functions
class InstallBCWalletPage(WebBasePage):
    """BC Wallet Showcase Install BC Wallet page object"""

    # Locators
    on_this_page_text_locator = "install the BC Wallet app"
    skip_locator = (By.XPATH, "//button[normalize-space()='SKIP']")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_skip(self) -> ConnectWithBestBCCollegePage:
        try:
            self.find_by(self.skip_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return ConnectWithBestBCCollegePage(self.driver)