from bc_wallet.onboarding import *
from override_steps import overrides
from pageobjects.qc_wallet.onboardingtakecontrol import OnboardingTakeControlPageQC
from pageobjects.qc_wallet.onboardingwelcome import OnboardingWelcomePageQC


@overrides('they can select Get started', 'then')
def get_started_step_impl(context):
    context.thisOnboardingTakeControlPage = OnboardingTakeControlPageQC(context.driver)
    context.thisTermsAndConditionsPage = context.thisOnboardingTakeControlPage.select_get_started()

@overrides('the new user has opened the app for the first time', 'given')
def special_step_impl(context):
    # App opened already buy appium. 
    # Intialize the page we should be on
    context.thisOnboardingWelcomePage = OnboardingWelcomePageQC(context.driver)
