# -----------------------------------------------------------
# Behave Step Definitions for New User Onboarding
#
# -----------------------------------------------------------

from behave import given, when, then, step
import json

# Local Imports
from agent_controller_client import (
    agent_controller_GET,
    agent_controller_POST,
    expected_agent_state,
    setup_already_connected,
)
from agent_test_utils import get_qr_code_from_invitation

# import Page Objects needed
from pageobjects.bc_wallet.onboarding_is_this_app_for_you import OnboardingIsThisAppForYouPage
from pageobjects.bc_wallet.onboarding_a_different_smart_wallet import OnboardingADifferentSmartWalletPage
from pageobjects.bc_wallet.onboarding_private_confidential import OnboardingPrivateConfidentialPage
from pageobjects.bc_wallet.onboarding_digital_credentials import OnboardingDigitalCredentialsPage
from pageobjects.bc_wallet.termsandconditions import TermsAndConditionsPage


@given("the new user has opened the app for the first time")
def step_impl(context):
    # App opened already buy appium.
    # Intialize the page we should be on
    context.thisOnboardingIsThisAppForYouPage = OnboardingIsThisAppForYouPage(context.driver)
    

@given('the user is on the Is this app for you screen')
def step_impl(context):
    assert context.thisOnboardingIsThisAppForYouPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingIsThisAppForYouPage

@step(u'the user selects confirms that the app is for them')
def step_impl(context):
    context.thisOnboardingIsThisAppForYouPage.select_confirm()

@step(u'they select Continue')
def step_impl(context):
    context.thisOnboardingADifferentSmartWalletPage = context.thisOnboardingIsThisAppForYouPage.select_continue()
    context.currentOnboardingPage = context.thisOnboardingADifferentSmartWalletPage


@when("the user selects Next")
def step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_next()
    if type(thisOnboardingPage) == OnboardingADifferentSmartWalletPage:
        context.thisOnboardingADifferentSmartWalletPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingPrivateConfidentialPage:
        context.thisOnboardingPrivateConfidentialPage = thisOnboardingPage
    elif type(thisOnboardingPage) == OnboardingDigitalCredentialsPage:
        context.thisOnboardingDigitalCredentialsPage = thisOnboardingPage


@when('they are brought to the A different smart wallet screen')
def step_impl(context):
    assert context.thisOnboardingADifferentSmartWalletPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingADifferentSmartWalletPage


@when('they are brought to the Digital credentials screen')
def step_impl(context):
    assert context.thisOnboardingDigitalCredentialsPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingDigitalCredentialsPage


@when('they are brought to the Private and confidential screen')
def step_impl(context):
    assert context.thisOnboardingPrivateConfidentialPage.on_this_page()
    # set a current onboarding page so the select Next step can be reused across these pages
    context.currentOnboardingPage = context.thisOnboardingPrivateConfidentialPage


@then("they can select Get started")
def step_impl(context):
    context.thisTermsAndConditionsPage = context.thisOnboardingPrivateConfidentialPage.select_get_started()


@then("are brought to the Terms and Conditions screen")
def step_impl(context):
    assert context.thisTermsAndConditionsPage.on_this_page()


@given('the user is on the "{screen}"')
@given("the user is on the onboarding {screen}")
def step_impl(context, screen):

    if screen == "A different smart wallet screen":
        context.execute_steps(f'''
            When they are brought to the A different smart wallet screen
        ''')

    elif screen == "Digital credentials screen":
        context.execute_steps(f'''
            When they are brought to the A different smart wallet screen
            And the user selects Next
            And they are brought to the Digital credentials screen
        ''')
    elif screen == "Private and confidential screen":
        context.execute_steps(f'''
            When they are brought to the A different smart wallet screen
            And the user selects Next
            And they are brought to the Digital credentials screen
            And the user selects Next
            And they are brought to the Private and confidential screen
        ''')
    else:
        raise Exception(f"Unexpected screen, {screen}")


# @when('the user selects Skip')
# def step_impl(context):
#     context.thisTermsAndConditionsPage = context.currentOnboardingPage.select_skip()


@when("the user selects Back")
def step_impl(context):
    thisOnboardingPage = context.currentOnboardingPage.select_back()
    if type(thisOnboardingPage) == OnboardingADifferentSmartWalletPage:
        context.thisOnboardingADifferentSmartWalletPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingADifferentSmartWalletPage
    elif type(thisOnboardingPage) == OnboardingPrivateConfidentialPage:
        context.thisOnboardingPrivateConfidentialPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingPrivateConfidentialPage
    elif type(thisOnboardingPage) == OnboardingDigitalCredentialsPage:
        context.thisOnboardingDigitalCredentialsPage = thisOnboardingPage
        context.currentOnboardingPage = context.thisOnboardingDigitalCredentialsPage


@then("are brought to the {previous_screen}")
def step_impl(context, previous_screen):
    if previous_screen == "Store your credentials securely screen":
        assert context.thisOnboardingADifferentSmartWalletPage.on_this_page()
    elif previous_screen == "Share only what is neccessary screen":
        assert context.thisOnboardingDigitalCredentialsPage.on_this_page()


@when("the user quits the app")
def step_impl(context):
    # close the app and reopen
    context.driver.reset()


@when("they reopen the app")
def step_impl(context):
    # app was opened in the driver.reset() call in the last step.
    pass


@then('they land on the A different smart wallet screen')
def step_impl(context):
    context.execute_steps(
        f"""
        Given the new user has opened the app for the first time
        And the user is on the onboarding {'A different smart wallet screen'}
    ''')


@when("the user selects Learn more about BC Wallet")
def step_impl(context):
    context.thisOnboardingTakeControlPage.select_learn_more()


@then("they are brought to thier browser with more info about BC wallet")
def step_impl(context):
    # TODO how to check for this?
    print(context.driver.get().getContextHandles())
    print(context.driver.getContext())
