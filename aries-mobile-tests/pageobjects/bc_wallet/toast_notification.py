import os
from pageobjects.basepage import BasePage

class ToastNotification(BasePage):
    """base class for the toast notification page object"""

    # Locators
    on_this_page_text_locator:str
    notification_locator:tuple

    def on_this_page(self):   
        timeout = 50
        if "Local" in os.environ['DEVICE_CLOUD']:
            timeout = 100
        return super().on_this_page(self.on_this_page_text_locator, timeout)  

    def dismiss_notification(self):
        if self.on_this_page():
            self.find_by(self.notification_locator).click()
            # Not sure what is returned here yet
            # return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
