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


@given('the new user has opened the app for the first time')
def step_impl(context):
    # App opened already buy appium. 
    # Intialize the page we should be on
    context.thisLanguageSplashPage = LanguageSplashPage(context.driver)
    

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


@when('the wallet user scans the QR code sent by the issuer')
def step_impl(context):
    (resp_status, resp_text) = agent_controller_POST(context.issuer_url, "connections", operation="create-invitation")
    assert resp_status == 200, f'resp_status {resp_status} is not 200; {resp_text}'
    invitation_json = json.loads(resp_text)
    qrimage = get_qr_code_from_invitation(invitation_json)

    context.thisHomePage.inject_connection_invite_qr_code(qrimage)
    # Do we need to load the scan page after image injection? probably not. 
    #context.thisScanPage = context.thisHomePage.select_scan()
    context.thisHomePage.select_scan()
    #context.thisHomePage.select_settings()
    #thisScanPage.

@when('accepts the connection')
def step_impl(context):
    # click yes on notification? 
    pass

@then('there is a connection between Issuer and wallet user')
def step_impl(context):
    # Check the connections for a new connection
    context.thisContactsPage = context.thisHomePage.select_contacts()
    
    
