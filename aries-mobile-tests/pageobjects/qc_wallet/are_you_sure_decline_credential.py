from pageobjects.bc_wallet.are_you_sure_decline_proof_request import AreYouSureDeclineProofRequestPage


class AreYouSureDeclineCredentialPageQC(AreYouSureDeclineProofRequestPage):
    """Comfirm the decline of credential page object"""

    # Locators
    on_this_page_text_locator = "Are you sure you want to decline this credential"

    def __init__(self, driver):
        super().__init__(driver)

    def select_confirm(self):
        if self.on_this_page():
            self.find_by(self.confirm_locator).click()
            from pageobjects.qc_wallet.credential_declined import CredentialDeclinedPage
            return CredentialDeclinedPage(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
