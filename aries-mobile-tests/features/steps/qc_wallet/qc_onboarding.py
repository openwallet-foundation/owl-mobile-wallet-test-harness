from bc_wallet.onboarding import *
from override_steps import overrides
from pageobjects.qc_wallet.onboardingwelcome import OnboardingWelcomePageQC

@overrides('the new user has opened the app for the first time', 'given')
def special_step_impl(context):
    # App opened already buy appium. 
    # Intialize the page we should be on
    context.thisOnboardingWelcomePage = OnboardingWelcomePageQC(context.driver)
