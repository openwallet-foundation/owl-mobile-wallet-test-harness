from pageobjects.basepage import BasePage


# These classes can inherit from a BasePage to do common setup and functions
class SendingInformationSecurelyPage(BasePage):
    """Sending Proof Information Securely page object"""

    # Locators
    on_this_page_text_locator = "Sending the information securely"

    def on_this_page(self):
        #print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)



