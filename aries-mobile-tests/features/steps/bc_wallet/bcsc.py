# -----------------------------------------------------------
# Behave Step Definitions for a proof request to a wallet user
#
# -----------------------------------------------------------

from time import sleep
from behave import given, when, then

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation, table_to_str, create_non_revoke_interval
# import Page Objects needed
from pageobjects.bc_wallet.holder_get_invite_interface.bc_vp_holder_get_invite_interface import BCVPHolderGetInviteInterface
from pageobjects.bc_wallet.create_bc_digital_id import CreateABCDigitalIDPage

@given('the BCSC holder has a {credential}')
def step_impl(context, credential):
    context.execute_steps(f'''
        Given the BCVC Issuer sends a BC VC Pilot Certificate
        And the BCSC holder gets the invite QR Code from their email
        And they Scan the credential offer QR Code
        Then holder is brought to the credential offer screen
        When they select Accept
        And the holder is informed that their credential is on the way with an indication of loading
        And once the credential arrives they are informed that the Credential is added to your wallet
        And they select Done
        Then they are brought to the list of credentials
    ''')

    context.execute_steps(u'''
        Then the credential accepted is at the top of the list
        {table}
    '''.format(table=table_to_str(context.table)))

@given('the BCVC Issuer sends a BC VC Pilot Certificate')
def step_impl(context):
    context.issuer.send_credential()
    
@given('the BCSC holder gets the invite QR Code from their email')
def step_impl(context):
    context.holderGetInviteInterface = BCVPHolderGetInviteInterface("http://www.gmail.com")
    #sleep(2)
    assert context.holderGetInviteInterface.open_invitation_email()
    assert context.holderGetInviteInterface.select_invitation_link()
    qrcode =  context.holderGetInviteInterface.get_qr_code_invitation()
    context.device_service_handler.inject_qrcode(qrcode)

@then('they Close and go to Wallet')
@given('they are Home')
def step_impl(context):
    context.thisHomePage = context.thisNavBar.select_home()
    assert context.thisHomePage.on_this_page()


@when('they select Get your BC Digital ID')
def step_impl(context):
    context.thisHomePage.select_get_bc_digital_id()


@when('they select Share on the proof request from IDIM')
def step_impl(context):   
    context.execute_steps('''
        Then holder is brought to the proof request
        Then they select Share
    ''')


@when('they select Log in with BC Services Card in the Create a BC Digital ID Web page')
def step_impl(context):   
    if hasattr(context, 'thisCreateABCDigitalIDPage') == False:
        context.thisCreateABCDigitalIDPage = CreateABCDigitalIDPage(context.driver)
    context.thisBCServicesCardLoginPage = context.thisCreateABCDigitalIDPage.select_login_with_bc_services_card()


@when('they select {setup_option} on the Set up the BC Services Card app')
def step_impl(context, setup_option): 
    if setup_option == "Virtual testing":
        context.thisBCServicesCardLoginVTCSNPage = context.thisBCServicesCardLoginPage.select_virtual_testing()

@when('they enter in {card_serial_number} as the card serial number')
def step_impl(context, card_serial_number): 
    context.thisBCServicesCardLoginVTCSNPage.enter_card_serial_number(card_serial_number)
    context.thisBCServicesCardLoginVTPCPage = context.thisBCServicesCardLoginVTCSNPage.select_continue()


@when('they enter in {passcode} as the passcode')
def step_impl(context, passcode): 
    context.thisBCServicesCardLoginVTPCPage.enter_passcode(passcode)
    context.thisBCServicesCardReviewPage = context.thisBCServicesCardLoginVTPCPage.select_continue()

@when('they select I agree on the Review page')
def step_impl(context): 
    context.thisBCServicesCardReviewPage.i_agree()
    

@when('they select Send Credential')
def step_impl(context): 
    context.thisBCServicesCardCredentialIssuedPage = context.thisBCServicesCardReviewPage.send_credential()


@then('they get are told Your Credential has been Issued')
def step_impl(context): 
    assert context.thisBCServicesCardCredentialIssuedPage.on_this_page()

# # they Close and go to Wallet (select home for now)
# @then('they Close and go to Wallet')
# def step_impl(context): 
#     pass


@then('they select View on the new Credential Offer')
def step_impl(context): 
    context.thisCredentialOfferPage = context.thisHomePage.select_view_credential_offer()


@then('the BCVC Pilot credential is after the IDIM Person credential')
def step_impl(context): 
    pass