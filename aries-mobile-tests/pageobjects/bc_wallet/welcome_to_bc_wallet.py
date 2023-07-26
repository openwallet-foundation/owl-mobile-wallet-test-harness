from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.settings import SettingsPage
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from pageobjects.bc_wallet.get_person_credential import GetPersonCredentialPage
from pageobjects.bc_wallet.credential_details import CredentialDetailsPage
from time import sleep


class WelcomeToBCWalletModal(BasePage):
    """Welcome to BC Wallet Modal page object"""

    # Locators
    on_this_page_text_locator = "Welcome to BC Wallet"
    dismiss_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Dismiss")
    use_app_guides_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay")
    dont_use_app_guides_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Cancel")

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator)
    
    def is_displayed(self):
        return self.on_this_page()

    def select_dismiss(self):
        self.find_by(self.dismiss_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

    def select_use_app_guides(self):
        self.find_by(self.use_app_guides_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()

    def select_dont_use_app_guides(self):
        self.find_by(self.dont_use_app_guides_button_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()



