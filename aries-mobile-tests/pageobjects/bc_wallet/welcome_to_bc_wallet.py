from appium.webdriver.common.appiumby import AppiumBy
from pageobjects.basepage import BasePage, WaitCondition


class WelcomeToBCWalletModal(BasePage):
    """Welcome to BC Wallet Modal page object"""

    # Locators
    on_this_page_text_locator = "Welcome to BC Wallet"
    on_this_page_locator = (AppiumBy.NAME, "Welcome to BC Wallet")
    dismiss_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Dismiss")
    use_app_guides_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Okay")
    dont_use_app_guides_button_locator = (AppiumBy.ID, "com.ariesbifold:id/Cancel")

    def on_this_page(self):
        if self.current_platform.lower() == "Android".lower():
            return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.on_this_page_locator)

    def is_displayed(self):
        return self.on_this_page()

    def select_dismiss(self):
        self.find_by(
            self.dismiss_button_locator,
            wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE,
        ).click()

    def select_use_app_guides(self):
        self.find_by(
            self.use_app_guides_button_locator,
            wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE,
        ).click()

    def select_dont_use_app_guides(self):
        self.find_by(
            self.dont_use_app_guides_button_locator,
            wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE,
        ).click()
