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

@given('the user is on the "{screen}"')
@given('the user is on the onboarding {screen}')
def step_impl(context, screen):
    # Assume for now they start on the welcome screen

    # Detemrine what onboarding screen they are on, then migrate them to the screen passed in.
    if screen == "Welcome screen":
        # at the start of a test call the intial steps.
        context.execute_steps(f'''
            Given the user is on the onboarding Welcome screen
        ''')

    elif screen == "Store your credentials securely screen":
        context.execute_steps(f'''
            Given the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
        ''')

    elif screen == "Share only what is neccessary screen":
        context.execute_steps(f'''
            Given the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
            And the user selects Next
            And they are brought to the Share only what is neccessary screen
        ''')
    elif screen == "Take control of your information screen":
        context.execute_steps(f'''
            Given the user is on the onboarding Welcome screen
            When the user selects Next
            And they are brought to the Store your credentials securely screen
            And the user selects Next
            And they are brought to the Share only what is neccessary screen
            And the user selects Next
            And they are brought to the Take control of your information screen
        ''')
    else:
        raise Exception(f"Unexpected screen, {screen}")


@when('the user selects Skip')
def step_impl(context):
    context.thisTermsAndConditionsPage = context.currentOnboardingPage.select_skip()


@when('the user selects Back')
def step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_back()
    if type(thisOnboardingPage) == OnboardingWelcomePage:
        context.thisOnboardingWelcomePage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingWelcomePage
    if type(thisOnboardingPage) == OnboardingStoreCredsSecurelyPage:
        context.thisOnboardingStoreCredsSecurelyPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingStoreCredsSecurelyPage
    elif type(thisOnboardingPage) == OnboardingTakeControlPage:
        context.thisOnboardingTakeControlPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingTakeControlPage
    elif type(thisOnboardingPage) == OnboardingShareNecessaryPage:
        context.thisOnboardingShareNecessaryPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingShareNecessaryPage


@then('are brought to the {previous_screen}')
def step_impl(context, previous_screen):
    if previous_screen == "Welcome screen":
        assert context.thisOnboardingWelcomePage.on_this_page()
    elif previous_screen == "Store your credentials securely screen":
        assert context.thisOnboardingStoreCredsSecurelyPage.on_this_page()
    elif previous_screen == "Share only what is neccessary screen":
        assert context.thisOnboardingShareNecessaryPage.on_this_page()


@when('the user quits the app')
def step_impl(context):
    # close the app and reopen
    context.driver.reset()


@when('they reopen the app')
def step_impl(context):
    # app was opened in the driver.reset() call in the last step.
    pass


@then('they land on the Welcome screen')
def step_impl(context):
    context.execute_steps(f'''
        Given the new user has opened the app for the first time
        Given the user is on the onboarding Welcome screen
    ''')


@when('the user selects Learn more about BC Wallet')
def step_impl(context):
    context.thisOnboardingTakeControlPage.select_learn_more()


@then('they are brought to thier browser with more info about BC wallet')
def step_impl(context):
    # TODO how to check for this?
    print(context.driver.get().getContextHandles())
    print(context.driver.getContext())
    #raise NotImplementedError(u'STEP: Then they are brought to thier browser with more info about BC wallet')