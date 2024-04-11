from pageobjects.bc_wallet.pin import PINPage
from pageobjects.qc_wallet.initialization import InitializationPageQC


class PINPageQC(PINPage):
    """PIN QC Entry page object"""

    def __init__(self, driver):
        super().__init__(driver)

    def select_enter(self):
        if self.on_this_page():
            self.find_by(self.enter_button_locator).click()

            # return the wallet initialization page
            return InitializationPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
