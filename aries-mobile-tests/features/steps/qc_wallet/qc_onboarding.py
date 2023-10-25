from bc_wallet.onboarding import *
from override_steps import overrides
from pageobjects.qc_wallet.onboardingsharenecessary import (
    OnboardingShareNecessaryPageQC,
)
from pageobjects.qc_wallet.onboardingstorecredssecurely import (
    OnboardingStoreCredsSecurelyPageQC,
)
from pageobjects.qc_wallet.onboardingtakecontrol import OnboardingTakeControlPageQC
from pageobjects.qc_wallet.onboardingwelcome import OnboardingWelcomePageQC


@overrides("the new user has opened the app for the first time", "given")
def special_step_impl(context):
    # App opened already buy appium.
    # Intialize the page we should be on
    context.thisOnboardingWelcomePage = OnboardingWelcomePageQC(context.driver)


@overrides("the user selects Next", "when")
def step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_next()
    if type(thisOnboardingPage) == OnboardingStoreCredsSecurelyPageQC:
        context.thisOnboardingStoreCredsSecurelyPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingTakeControlPageQC:
        context.thisOnboardingTakeControlPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingShareNecessaryPageQC:
        context.thisOnboardingShareNecessaryPage = thisOnboardingPage


@overrides("they can select Get started", "then")
def get_started_step_impl(context):
    context.thisOnboardingTakeControlPage = OnboardingTakeControlPageQC(context.driver)
    context.thisTermsAndConditionsPage = (
        context.thisOnboardingTakeControlPage.select_get_started()
    )
