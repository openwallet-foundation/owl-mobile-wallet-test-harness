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

@when('the Holder scans the QR code sent by the "{agent}"')
def step_impl(context, agent):
    if agent == "issuer":
        qrimage = context.issuer.create_invitation(print_qrcode=context.print_qr_code_on_creation, save_qrcode=context.save_qr_code_on_creation)
    elif agent == "verifier":
        qrimage = context.verifier.create_invitation()
    else:
        raise Exception(f"Invalid agent type: {agent}")


    context.thisNavBar.inject_connection_invite_qr_code(qrimage)

    #context.thisConnectingPage = context.thisHomePage.select_scan()
    context.thisConnectingPage = context.thisNavBar.select_scan()


@when('the Holder is taken to the Connecting Screen/modal')
def step_impl(context):
    # The connecting screen is temporary. 
    # What if the connecting screen goes away too fast before this next line runs? Maybe check at home?
    assert context.thisConnectingPage.on_this_page()
    # context.connecting_is_done = False
    # if context.thisConnectingPage.on_this_page():
    #     assert True
    # else:
    #     # We are probably already on the home screen
    #     # TDOD as of build 164 this isn't needed. It seems the page doesn't automatically go to the home screen after a while
    #     assert context.thisHomePage.on_this_page()
    #     context.connecting_is_done = True

@when('the Connecting completes successfully')
def step_impl(context):
    # The connecting screen is temporary, loop until it goes away and return home.
    # if context.connecting_is_done == False:
    #     timeout=20
    #     i=0
    #     while context.thisConnectingPage.on_this_page() and i < timeout:
    #         # need to break out here incase we are stuck on connecting? 
    #         # if we are too long, we need to click the Go back to home button.
    #         sleep(1)
    #         i+=1
    #     if i == 20: # we timed out and it is still connecting
    #         context.thisHomePage = context.thisConnectingPage.select_go_back_to_home()
    #     else:
    #         #assume we are home
    #         assert context.thisHomePage.on_this_page()
    
    timeout=20
    i=0
    while context.issuer.connected() == False and i < timeout:
        sleep(1)
        i+=1
    if i == 20: # we timed out and it is still connecting
        raise Exception(f'Failed to connected in timeout of {timeout} seconds')
        #context.thisHomePage = context.thisConnectingPage.select_go_back_to_home()
    else:
        # One last check
        assert context.issuer.connected()

@then('there is a connection between "{agent}" and Holder')
def step_impl(context, agent):
    # Check the contacts for a new connection

    if agent == "issuer":
        assert context.issuer.connected()
    elif agent == "verifier":
        assert context.verifier.connected()
    else:
        raise Exception(f"Invalid agent type: {agent}")
    #assert context.issuer.connected()
    
    
