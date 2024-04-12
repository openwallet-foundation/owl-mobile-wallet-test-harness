from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.bc_wallet.welcome_to_bc_wallet import WelcomeToBCWalletModal


class WelcomeToQCWalletModal(WelcomeToBCWalletModal):
    """Welcome to BC Wallet Modal page object"""

    on_this_page_text_locator = "Welcome to QC Wallet"
    on_this_page_locator = (AppiumBy.NAME, "Welcome to QC Wallet")

    def on_this_page(self):
        language = self.get_app_language()
        if language == "French":
            self.on_this_page_text_locator = "Bienvenue à Aries Bifold"
            self.on_this_page_locator = (AppiumBy.NAME, "Bienvenue à Aries Bifold")
        return super().on_this_page()
