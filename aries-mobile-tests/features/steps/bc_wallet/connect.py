# -----------------------------------------------------------
# Behave Step Definitions for Connecting an issuer to a wallet user
# 
# -----------------------------------------------------------

from pageobjects.bc_wallet.navbar import NavBar
from behave import given, when, then
import json
from time import sleep


# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
# import Page Objects needed
from pageobjects.bc_wallet.connecting import ConnectingPage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.camera_privacy_policy import CameraPrivacyPolicyPage

@given('a PIN has been set up with "{pin}"')
def step_impl(context, pin):
    # context.execute_steps(f'''
    #     Given the User is on the PIN creation screen
    #     When the User enters the first PIN as "{pin}"
    #     And the User re-enters the PIN as "{pin}"
    #     And the User selects Create PIN
    #     And the User selects to use Biometrics
    #     Then the User has successfully created a PIN
    # ''')
    context.execute_steps(f'''
        Given the User is on the PIN creation screen
        When the User enters the first PIN as "{pin}"
        And the User re-enters the PIN as "{pin}"
        And the User selects Create PIN
    ''')

@when('the Holder scans the QR code sent by the "{agent}"')
def step_impl(context, agent):
    if agent == "issuer":
        qrimage = context.issuer.create_invitation(print_qrcode=context.print_qr_code_on_creation, save_qrcode=context.save_qr_code_on_creation)
    elif agent == "verifier":
        qrimage = context.verifier.create_invitation(print_qrcode=context.print_qr_code_on_creation, save_qrcode=context.save_qr_code_on_creation)
    else:
        raise Exception(f"Invalid agent type: {agent}")


    context.device_service_handler.inject_qrcode(qrimage)

    if hasattr(context, 'thisNavBar') == False:
        context.thisNavBar = NavBar(context.driver)
    context.thisConnectingPage = context.thisNavBar.select_scan()

    # If this is the first time the user selects scan, then they will get a Camera Privacy Policy that needs to be dismissed
    # TODO only do this if the platorm is iOS. Android is not showing the policy page at present in Sauce Labs becasue we have autoGrantPermissions on. 
    if context.driver.capabilities['platformName'] == 'iOS':
        context.thisCameraPrivacyPolicyPage = CameraPrivacyPolicyPage(context.driver)
        if context.thisCameraPrivacyPolicyPage.on_this_page():
            context.thisCameraPrivacyPolicyPage.select_allow()


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

@given('the Connecting completes successfully')
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
    if i == timeout: # we timed out and it is still connecting
        raise Exception(f'Failed to connect. Checked connection status {timeout} times.')
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
    
    

@given('the holder is connected to an Issuer')
def step_impl(context):
    context.execute_steps('''
        Given the Holder has setup thier wallet
        And the Holder has selected to use biometrics to unlock BC Wallet
        And a connection has been successfully made
    ''')

@given('there are {no_credentials} issued by this Contact in the holders wallet')
def step_impl(context, no_credentials):

    if no_credentials == "Offered and Rejected":
        context.execute_steps('''
            Given the user has a credential offer
            And the holder declines the credential offer
        ''')

    elif no_credentials == "Issued and Deleted":
        pass
    elif no_credentials == "Issued Revoked and Deleted":
        pass


@when('the holder Removes this Contact')
def step_impl(context):
    context.thisSettingsPage = context.thisHomePage.select_settings()
    context.thisContactsPage = context.thisSettingsPage.select_contacts()
    context.thisContactPage = context.thisContactsPage.select_contact(context.issuer.get_name())
    context.thisContactDetailsPage = context.thisContactPage.select_info()
    context.thisRemoveFromWalletPage = context.thisContactDetailsPage.select_remove_from_wallet()


@when(u'the holder reviews more details on removing Contacts')
def step_impl(context):
    # get the details from the context table object.
    details = context.table[0]["details"]
    assert details in context.thisRemoveFromWalletPage.get_details_text()


@when(u'the holder confirms to Remove this Contact')
def step_impl(context):
    context.thisContactsPage = context.thisRemoveFromWalletPage.select_remove_from_wallet()


@then(u'the holder is taken to the Contact list')
def step_impl(context):
    context.thisContactsPage.on_this_page()


@then(u'the holder is informed that the Contact has been removed')
def step_impl(context):
    # this message is displayed for a few seconds then disappears. 
    # TODO: need to think of a foolproof way to get a handle on this. With appium being so slow if may already be gone.
    # pass for now and chekc that the contact is correctly removed from the list
    pass


@then(u'the Contact is removed from the wallet')
def step_impl(context):
    # check that the contact is not in the list
    #assert context.issuer.get_name() not in context.thisContactsPage.get_contact_list()
    #context.thisContactsPage.select_contact(context.issuer.get_name())
    assert context.thisContactsPage.is_contact_present(context.issuer.get_name()) == False

    
