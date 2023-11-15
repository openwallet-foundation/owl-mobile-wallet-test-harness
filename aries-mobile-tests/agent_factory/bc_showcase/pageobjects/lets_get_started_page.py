from PIL import Image
from agent_factory.candy_uvp.pageobjects.webbasepage import WebBasePage
from selenium.webdriver.common.by import By
from pageobjects.basepage import WaitCondition
import base64
from agent_factory.bc_showcase.pageobjects.install_bc_wallet_page import InstallBCWalletPage


# These classes can inherit from a BasePage to do commone setup and functions
class LetsGetStartedPage(WebBasePage):
    """BC Wallet Showcase Lets Get Started page object"""

    # Locators
    on_this_page_text_locator = "BC Wallet is a new app for storing and using credentials"
    next_locator = (By.XPATH, "//button[normalize-space()='NEXT']")


    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def select_next(self) -> InstallBCWalletPage:
        try:
            self.find_by(self.next_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
        except Exception as e:
            if not self.on_this_page():
                raise Exception(f"App not on the {type(self)} page")
            else:
                raise e
        return InstallBCWalletPage(self.driver)