# -----------------------------------------------------------
# Behave Step Definitions for Connecting an issuer to a wallet user
# 
# -----------------------------------------------------------

from behave import given, when, then
import json
from time import sleep

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
# import Page Objects needed
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.home import HomePage

@given('a PIN has been set up with "{pin}"')
def step_impl(context, pin):
    context.execute_steps(f'''
        Given the User is on the PIN creation screen
        When the User enters the first PIN as "{pin}"
        And the User re-enters the PIN as "{pin}"
        And the User selects Create PIN
        Then the User has successfully created a PIN
    ''')

@when ('the Holder scans the QR code sent by the {agent}')
@when('the Holder scans the QR code sent by the issuer')
def step_impl(context, agent="issuer"):
    qrimage = exec(f"context.{agent}.create_invitation()")
    #qrimage = context.issuer.create_invitation()
    #qrimage = context.issuer.create_invitation(oob=True)
    # (resp_status, resp_text) = agent_controller_POST(
    #     context.issuer_url + "/agent/command/", "connection", operation="create-invitation"
    # )
    # assert resp_status == 200, f'resp_status {resp_status} is not 200; {resp_text}'
    # invitation_json = json.loads(resp_text)
    # qrimage = get_qr_code_from_invitation(invitation_json)

    context.thisHomePage.inject_connection_invite_qr_code(qrimage)
    # Do we need to load the scan page after image injection? probably not.
    #context.thisScanPage = context.thisHomePage.select_scan()
    context.thisConnectingPage = context.thisHomePage.select_scan()


@when('the Holder is taken to the Connecting Screen/modal')
def step_impl(context):
    # The connecting screen is temporary. 
    # What if the connecting screen goes away too fast before this next line runs? Maybe check at home?
    context.connecting_is_done = False
    if context.thisConnectingPage.on_this_page():
        assert True
    else:
        # We are probably already on the home screen
        assert context.thisHomePage.on_this_page()
        context.connecting_is_done = True

@when('the Connecting completes successfully')
def step_impl(context):
    # The connecting screen is temporary, loop until it goes away and return home.
    if context.connecting_is_done == False:
        timeout=20
        i=0
        while context.thisConnectingPage.on_this_page() and i < timeout:
            # need to break out here incase we are stuck on connecting? 
            # if we are too long, we need to click the Go back to home button.
            sleep(1)
            i+=1
        if i == 20: # we timed out and it is still connecting
            context.thisHomePage = context.thisConnectingPage.select_go_back_to_home()
        else:
            #assume we are home
            assert context.thisHomePage.on_this_page()


@then('there is a connection between Issuer and Holder')
def step_impl(context):
    # Check the contacts for a new connection
    # TODO the contacts list is created on scan not on successful connection made. Will have to check the issuer for successful connection
    #context.thisSettingsPage = context.thisHomePage.select_settings()

    assert context.issuer.connected()
    
    
