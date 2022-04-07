import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.sending_information_securely import SendingInformationSecurelyPage


# These classes can inherit from a BasePage to do common setup and functions
class ProofRequestPage(BasePage):
    """Proof Request Details page object"""

    # Locators
    # Wireframes state different text here, so it will probably change to this
    #on_this_page_text_locator = "is requesting the following"
    on_this_page_text_locator = "is requesting you to share"
    who_locator = "Who"
    attribute_locator = "attribute"
    value_locator = "value"
    details_locator = "Details"
    share_locator = "Share"
    decline_locator = "Decline"


    def on_this_page(self):
        print(self.driver.page_source)
        return super().on_this_page(self.on_this_page_text_locator)

    def select_share(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.share_locator).click()
            return SendingInformationSecurelyPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_decline(self):
        if self.on_this_page():
            self.find_by_accessibility_id(self.accept_locator).click()
            # Not sure what is returned here yet
            # return CredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_proof_request_details(self):
        if self.on_this_page():
            who = self.find_by_accessibility_id(self.who_locator).text
            #cred_type = self.find_by_accessibility_id(self.cred_type_locator).text
            attribute_elements = self.find_multiple_by_id(self.attribute_locator)
            value_elements = self.find_multiple_by_id(self.values_locator)
            attributes = []
            for attribute in attribute_elements:
                attributes = attributes.append[attribute.text]
            values = []
            for value in value_elements:
                values = values.append[value.text]
            return who, attributes, values
        else:
            raise Exception(f"App not on the {type(self)} page")
