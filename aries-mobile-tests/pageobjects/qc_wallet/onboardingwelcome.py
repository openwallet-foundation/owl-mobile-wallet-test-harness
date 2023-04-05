from pageobjects.bc_wallet.onboardingwelcome import OnboardingWelcomePage
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC

# These classes can inherit from a BasePage to do common setup and functions
class OnboardingWelcomePageQC(OnboardingWelcomePage):
    """Onboarding Welcome Screen QC page object"""   

    def __init__(self, driver):
        super().__init__(driver)

    def select_skip(self):
        if self.on_this_page():
            self.find_by(self.skip_locator).click()
            return TermsAndConditionsPageQC(self.driver)
        else:
            raise Exception(f"App not on the {type(self)} page")
