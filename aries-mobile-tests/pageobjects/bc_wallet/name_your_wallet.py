import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition


class NameYourWalletPage(BasePage):
    """Name Your Wallet page object"""

    # Locators
    on_this_page_text_locator = "Name your wallet"
    back_locator = (AppiumBy.ID, "com.ariesbifold:id/Back")
    wallet_name_input_locator = (AppiumBy.ID, "com.ariesbifold:id/NameInput")
    save_locator = (AppiumBy.ID, "com.ariesbifold:id/Save")
    cancel_locator = (AppiumBy.ID, "com.ariesbifold:id/Cancel")
        

    def __init__(self, driver, calling_page=None):
        super().__init__(driver)
        # Edit Wallet name page can be called from the Settings page or the Scan my QR code page
        # calling page is set on the constructor and used to navigate back to the calling page in the methods below
        self.calling_page = calling_page
        # Instantiate possible Modals and Alerts for this page
        self.wallet_name_error_modal = WalletNameErrorModal(driver)
        self.wallet_name_cant_be_empty_modal = WalletNameCantBeEmptyModal(driver)
        self.wallet_name_character_count_exceeded_modal = WalletNameCharacterCountExceededModal(driver)

    def on_this_page(self):     
        return super().on_this_page(self.on_this_page_text_locator) 


    def get_wallet_name(self) -> str:
        return self.find_by(self.wallet_name_input_locator).text


    def enter_wallet_name(self, wallet_name:str):
        # Check if the app is on the correct page
        if not self.on_this_page():
            raise Exception(f"App not on the {type(self)} page")

        # Enter the new wallet name in the text field
        wallet_name_input = self.find_by(self.wallet_name_input_locator)
        wallet_name_input.clear()
        wallet_name_input.send_keys(wallet_name)



    def select_save(self):
        # Check if the app is on the correct page
        if not self.on_this_page():
            raise Exception(f"App not on the {type(self)} page")

        self.find_by(self.save_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

        return self.calling_page



    def select_cancel(self):
        # Check if the app is on the correct page
        if not self.on_this_page():
            raise Exception(f"App not on the {type(self)} page")

        self.find_by(self.cancel_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

        return self.calling_page
    

    def select_back(self):
        self.find_by(self.back_locator).click()
        return self.calling_page
    


class WalletNameErrorModal(BasePage):
    """Wallet Name Error Modal page object"""

    # Locators
    error_title_locator = (AppiumBy.ID, "com.ariesbifold:id/HeaderText")
    error_details_locator = (AppiumBy.ID, "com.ariesbifold:id/BodyText")
    okay_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay") 

    def on_this_page(self):
        return super().on_this_page(self.okay_locator)
    
    def is_displayed(self):
        return self.on_this_page()

    def get_error_title(self) -> str:
        return self.find_by(self.error_title_locator).text

    def get_error_details(self) -> str:
        return self.find_by(self.error_details_locator).text

    def select_okay(self):
        self.find_by(self.okay_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

class WalletNameCantBeEmptyModal(WalletNameErrorModal):
    """Wallet Name Can't be Empty Modal page object"""

    # Locators
    on_this_page_text_locator = "Wallet name can't be empty"

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)
    
    def is_displayed(self):
        return self.on_this_page()


class WalletNameCharacterCountExceededModal(WalletNameErrorModal):
    """Wallet Name Character Count Exeeded Modal page object"""

    # Locators
    on_this_page_text_locator = "Character count exceeded"

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)
    
    def is_displayed(self):
        return self.on_this_page()