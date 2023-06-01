from pageobjects.basepage import BasePage

class TemporarilyLockedPage(BasePage):
    """Temporarily Locked page object"""

    # Locators
    on_this_page_text_locator = "Temporarily Locked"

    def on_this_page(self):
        return super().on_this_page(self.on_this_page_text_locator, 50)
