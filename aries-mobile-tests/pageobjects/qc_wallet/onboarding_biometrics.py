import os
from time import sleep

from pageobjects.bc_wallet.onboarding_biometrics import \
    OnboardingBiometricsPage
from pageobjects.qc_wallet.initialization import InitializationPageQC


class OnboardingBiometricsPageQC(OnboardingBiometricsPage):
    """Onboarding Biometrics page object"""

    # Locators
    on_this_page_text_locator = "Use biometrics to unlock wallet?"

    def select_biometrics(self):
        if self.on_this_page():
            self.find_by(self.use_biometrics_toggle_locator).click()
            return True
        else:
            raise Exception(f"App not on the {type(self)} page")

    def select_continue(self):
        if self.on_this_page():
            self.find_by(self.continue_button_locator).click()

            # return the wallet initialization page
            return InitializationPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
