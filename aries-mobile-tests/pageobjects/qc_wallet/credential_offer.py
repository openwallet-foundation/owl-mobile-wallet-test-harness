from time import sleep
from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.credential_on_the_way import CredentialOnTheWayPage
from pageobjects.qc_wallet.are_you_sure_decline_credential import AreYouSureDeclineCredentialPageQC

class CredentialOfferPageQC(CredentialOfferPage):
    """Credential Offer Notification QC page object"""

    def __init__(self, driver):
        super().__init__(driver)

    def select_accept(self, scroll=False):
        if self.on_this_page():
            # if the credential has a lot of attributes it could need to scroll
            if scroll == True:
                try: 
                    self.scroll_to_element(self.accept_aid_locator[1])
                except:
                    sleep(5)
                    self.scroll_to_element(self.accept_aid_locator[1])
                self.find_by(self.accept_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            else:
                self.find_by(self.accept_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            return CredentialOnTheWayPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_decline(self, scroll=False):
        if self.on_this_page():
            # if the credential has a lot of attributes it could need to scroll
            if scroll == True:
                try: 
                    self.find_by(self.decline_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
                except:
                    self.scroll_to_element(self.accept_aid_locator[1])
                    self.find_by(self.decline_locator, timeout=30, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE).click()
            else:
                self.find_by(self.decline_locator).click()
            return AreYouSureDeclineCredentialPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
