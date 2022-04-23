# -----------------------------------------------------------
# Behave Step Definitions for Connecting an issuer to a wallet user
# 
# -----------------------------------------------------------

from behave import given, when, then
import json

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
# import Page Objects needed
from pageobjects.bifold.termsofservice import TermsOfServicePage
from pageobjects.bifold.pinsetup import PINSetupPage
from pageobjects.bifold.home import HomePage

# Instantiate the page objects needed
# Can I pass the context here on instantiation or should we do it in the steps? 
# We could put a page factory somewhere that instantiates all pages for a given app. 
# thisTermOfServicePage = TermsOfServicePage()
# thisPINSetupPage = PINSetupPage()
# thisHomePage = HomePage()

@given('the terms of service has been accepted')
def step_impl(context):
    context.thisTermOfServicePage = TermsOfServicePage(context.driver)
    context.thisTermOfServicePage.select_accept()
    context.thisPINSetupPage = context.thisTermOfServicePage.submit()

@given('a PIN has been set up')
def step_impl(context):
    # TODO Move the data into the feature file
    context.thisPINSetupPage.enter_pin("369369")
    context.thisPINSetupPage.enter_second_pin("369369")
    context.thisHomePage = context.thisPINSetupPage.create_pin()

@when('the wallet user scans the QR code sent by the issuer')
def step_impl(context):
    (resp_status, resp_text) = agent_controller_POST(context.issuer_url, "connections", operation="create-invitation")
    assert resp_status == 200, f'resp_status {resp_status} is not 200; {resp_text}'
    invitation_json = json.loads(resp_text)
    qrimage = get_qr_code_from_invitation(invitation_json, context.print_qr_code_on_creation, context.save_qr_code_on_creation)

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
    
    
