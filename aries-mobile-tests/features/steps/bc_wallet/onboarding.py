# -----------------------------------------------------------
# Behave Step Definitions for New User Onboarding
# 
# -----------------------------------------------------------

from behave import given, when, then
import json

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
# import Page Objects needed
from pageobjects.bc_wallet.onboardingwelcome import OnboardingWelcomePage
from pageobjects.bc_wallet.onboardingstorecredssecurely import OnboardingStoreCredsSecurelyPage
from pageobjects.bc_wallet.onboardingtakecontrol import OnboardingTakeControlPage
from pageobjects.bc_wallet.onboardingsharenecessary import OnboardingShareNecessaryPage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage


@given('the new user has opened the app for the first time')
def step_impl(context):
    # App opened already buy appium. 
    # Intialize the page we should be on
    context.thisOnboardingWelcomePage = OnboardingWelcomePage(context.driver)
    

@given('the user is on the onboarding Welcome screen')
def step_impl(context):
    assert context.thisOnboardingWelcomePage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingWelcomePage

@when('the user selects Next')
def step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_next()
    if type(thisOnboardingPage) == OnboardingStoreCredsSecurelyPage:
        context.thisOnboardingStoreCredsSecurelyPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingTakeControlPage:
        context.thisOnboardingTakeControlPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingShareNecessaryPage:
        context.thisOnboardingShareNecessaryPage = thisOnboardingPage


@when('they are brought to the Store your credentials securely screen')
def step_impl(context):
    assert context.thisOnboardingStoreCredsSecurelyPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingStoreCredsSecurelyPage


@when('they are brought to the Share only what is neccessary screen')
def step_impl(context):
    assert context.thisOnboardingShareNecessaryPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingShareNecessaryPage


@when('they are brought to the Take control of your information screen')
def step_impl(context):
    assert context.thisOnboardingTakeControlPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingTakeControlPage


@then('they can select Get started')
def step_impl(context):
    context.thisTermsAndConditionsPage = context.thisOnboardingTakeControlPage.select_get_started()


@then('are brought to the Terms and Conditions screen')
def step_impl(context):
    assert context.thisTermsAndConditionsPage.on_this_page()

