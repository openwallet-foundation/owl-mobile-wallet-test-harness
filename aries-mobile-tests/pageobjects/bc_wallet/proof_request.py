import time
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageobjects.basepage import BasePage
from pageobjects.bc_wallet.sending_information_securely import SendingInformationSecurelyPage
from pageobjects.bc_wallet.are_you_sure_decline_proof_request import AreYouSureDeclineProofRequestPage
from pageobjects.bc_wallet.proof_request_details import ProofRequestDetailsPage


# These classes can inherit from a BasePage to do common setup and functions
class ProofRequestPage(BasePage):
    """Proof Request page object"""

    # Locators
    # Wireframes state different text here, so it will probably change to this
    #on_this_page_text_locator = "is requesting the following"
    on_this_page_text_locator = "is requesting you to share"
    who_locator = (MobileBy.ID, "com.ariesbifold:id/HeaderText")
    attribute_locator = (MobileBy.ID, "com.ariesbifold:id/AttributeName")
    value_locator = (MobileBy.ID, "com.ariesbifold:id/AttributeValue")
    details_locator = (MobileBy.ID, "com.ariesbifold:id/Details")
    share_locator = (MobileBy.ID, "com.ariesbifold:id/Share")
    share_aid_locator = (MobileBy.ACCESSIBILITY_ID, "Share")
    decline_locator = (MobileBy.ID, "com.ariesbifold:id/Decline")


    def on_this_page(self):
        #return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.who_locator)

    def select_share(self):
        if self.on_this_page():
            try:
                self.find_by(self.share_locator).click()
            except:
                self.scroll_to_element(self.share_aid_locator[1])
                self.find_by(self.share_locator).click()
            return SendingInformationSecurelyPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_details(self):
        if self.on_this_page():
            self.find_by(self.details_locator).click()
            return ProofRequestDetailsPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_decline(self):
        if self.on_this_page():
            self.find_by(self.decline_locator).click()
            # Not sure what is returned here yet
            return AreYouSureDeclineProofRequestPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def get_proof_request_details(self):
        if self.on_this_page():
            who = self.find_by(self.who_locator).text
            #cred_type = self.find_by_accessibility_id(self.details_locator).text
            attribute_elements = self.find_multiple_by(self.attribute_locator)
            value_elements = self.find_multiple_by(self.value_locator)
            attributes = []
            for attribute in attribute_elements:
                attributes.append(attribute.text)
            values = []
            for value in value_elements:
                values.append(value.text)
            return who, attributes, values
        else:
            raise Exception(f"App not on the {type(self)} page")
