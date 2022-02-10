# -----------------------------------------------------------
# Behave Step Definitions for Changing language
# 
# -----------------------------------------------------------

from behave import given, when, then
import json

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
# import Page Objects needed
from pageobjects.bc_wallet.languagesplash import LanguageSplashPage


# @given('the new user has opened the app for the first time')
# def step_impl(context):
#     # App opened already buy appium. 
#     # Intialize the page we should be on
#     context.thisLanguageSplashPage = LanguageSplashPage(context.driver)
    

@given('they are in the initial select language screen')
def step_impl(context):
    assert context.thisLanguageSplashPage.on_this_page()


@when('the new user selects "{language}"')
def step_impl(context, language):

    if language == 'English':
        context.thisLanguageSplashPage.select_english()
    elif language == "French":
        context.thisLanguageSplashPage.select_french()
    else:
        raise Exception(f"Unexpected language, {language}")

