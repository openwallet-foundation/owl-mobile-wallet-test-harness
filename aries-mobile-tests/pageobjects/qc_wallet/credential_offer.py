from time import sleep
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.credential_on_the_way import CredentialOnTheWayPage
from pageobjects.bc_wallet.decline_credential_offer import DeclineCredentialOfferPage
from pageobjects.qc_wallet.are_you_sure_decline_credential import AreYouSureDeclineCredentialPageQC

class CredentialOfferPageQC(CredentialOfferPage):
    """Credential Offer Notification QC page object"""

    def __init__(self, driver):
        super().__init__(driver)

    def select_accept(self, scroll=False):
        if self.on_this_page():
            # if the credential has a lot of attributes it could need to scroll
            if scroll == True:
                el_visible = self.is_element_visible(self.accept_locator)
                timeout=30
                while not el_visible and timeout > 0:
                    self.swipe_down()
                    el_visible = self.is_element_visible(self.accept_locator)
                    timeout-=1
                self.find_by(self.accept_locator).click()
            else:
                self.find_by(self.accept_locator).click()
            return CredentialOnTheWayPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_decline(self, scroll=False):
        if self.on_this_page():
            # if the credential has a lot of attributes it could need to scroll
            if scroll == True:
                el_visible = self.is_element_visible(self.decline_locator)
                timeout=30
                while not el_visible and timeout > 0:
                    self.swipe_down()
                    el_visible = self.is_element_visible(self.decline_locator)
                    timeout-=1
                self.find_by(self.decline_locator).click()
            else:
                self.find_by(self.decline_locator).click()
            return DeclineCredentialOfferPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
