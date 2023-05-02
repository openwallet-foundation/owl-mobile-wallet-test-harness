import time
from appium.webdriver.common.appiumby import AppiumBy
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
    who_locator = (AppiumBy.ID, "com.ariesbifold:id/HeaderText")
    attribute_locator = (AppiumBy.ID, "com.ariesbifold:id/AttributeName")
    value_locator = (AppiumBy.ID, "com.ariesbifold:id/AttributeValue")
    details_locator = (AppiumBy.ID, "com.ariesbifold:id/Details")
    share_locator = (AppiumBy.ID, "com.ariesbifold:id/Share")
    share_aid_locator = (AppiumBy.ACCESSIBILITY_ID, "Share")
    decline_locator = (AppiumBy.ID, "com.ariesbifold:id/Decline")
    credential_card_locator = (AppiumBy.ID, "com.ariesbifold:id/CredentialCard")


    def on_this_page(self):
        #return super().on_this_page(self.on_this_page_text_locator)
        return super().on_this_page(self.who_locator, timeout=20)

    def select_share(self):
        if self.on_this_page():
            try:
                self.find_by(self.share_locator).click()
            except:
                if self.current_platform == 'Android':
                    self.scroll_to_bottom()
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

    # def get_credentials_in_proof_request(self):
    #     if self.on_this_page():
    #         credential_card_elements = self.find_multiple_by(self.credential_card_locator)
    #         return credential_card_elements[0].text
    #     else:
    #         raise Exception(f"App not on the {type(self)} page")
        
    def get_text_in_all_credential_cards_in_proof_request(self) ->list:
        if self.on_this_page():
            credential_card_elements = self.find_multiple_by(self.credential_card_locator)
            # for each credential card, get the text and append to a list
            credential_card_text_list = []
            for credential_card in credential_card_elements:
                credential_card_text_list.append(credential_card.text)
            # If the list is empty, there is no credential on the proof request screen
            return credential_card_text_list
        else:
            raise Exception(f"App not on the {type(self)} page")