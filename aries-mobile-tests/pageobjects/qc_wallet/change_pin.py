from pageobjects.basepage import WaitCondition
from pageobjects.bc_wallet.change_pin import (ChangePINPage,
                                              SuccessfullyChangedPINModal)


class ChangePINPageQC(ChangePINPage):
    """PIN Change page object"""

    def __init__(self, driver):
        super().__init__(driver)
        # Instantiate possible Modals and Alerts for this page
        self.successfully_changed_pin_modal = SuccessfullyChangedPINModalQC(driver)


class SuccessfullyChangedPINModalQC(SuccessfullyChangedPINModal):
    """Successully Changed PIN Modal page object"""

    # Locators
    def select_okay(self):
        self.find_by(
            self.okay_locator, wait_condition=WaitCondition.ELEMENT_TO_BE_CLICKABLE
        ).click()
        from pageobjects.qc_wallet.settings import SettingsPageQC

        return SettingsPageQC(self.driver)
