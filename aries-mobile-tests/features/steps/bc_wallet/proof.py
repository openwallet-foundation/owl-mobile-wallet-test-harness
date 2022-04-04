# -----------------------------------------------------------
# Behave Step Definitions for a proof request to a wallet user
#
# -----------------------------------------------------------

from behave import given, when, then
import json
from time import sleep

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation
# import Page Objects needed
#from pageobjects.bc_wallet.credential_offer_notification import CredentialOfferNotificationPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from pageobjects.bc_wallet.credential_added import CredentialAddedPage
from pageobjects.bc_wallet.home import HomePage


@given('the holder has a Non-Revocable credential')
def step_impl(context):
    context.execute_steps(f'''
        Given the user has a credential offer
        When they select Accept
        And the holder is informed that their credential is on the way with an indication of loading
        And once the credential arrives they are informed that the Credential is added to your wallet
        And they select Done
        Then they are brought to the list of credentials
        And the credential accepted is at the top of the list
    ''')


@when('the Holder receives a proof request')
def step_impl(context):
    context.verifier.send_proof_request()


@then('holder is brought to the proof request')
def step_impl(context):
    assert context.thisProofRequestPage.on_this_page()


@then('they can view the contents of the proof request')
def step_impl(context):
    assert context.thisProofRequestPage.on_this_page()

    who, cred_type, attributes, values = get_expected_credential_detail(context)
    # The below doesn't have locators in build 127. Calibrate in the future fixed build
    #actual_who, actual_cred_type, actual_attributes, actual_values = context.thisCredentialOfferPage.get_credential_details() 
    #assert who in actual_who
    #assert cred_type in actual_cred_type
    #assert attributes in actual_attributes
    #assert values in actual_values


@given('the user has a credential offer')
def step_impl(context):
    context.execute_steps(f'''
        When the Holder receives a Non-Revocable credential offer
        And the Holder taps on the credential offer notification
        Then holder is brought to the credential offer screen
    ''')


@when('they select Accept')
def step_impl(context):
    context.thisCredentialOnTheWayPage = context.thisCredentialOfferPage.select_accept()


@when('the holder is informed that their credential is on the way with an indication of loading')
def step_impl(context):
    assert context.thisCredentialOnTheWayPage.on_this_page()


@when('once the credential arrives they are informed that the Credential is added to your wallet')
def step_impl(context):
    # The Cred is on the way screen is temporary, loop until it goes away and create the cred added page.
    timeout=20
    i=0
    while context.thisCredentialOnTheWayPage.on_this_page() and i < timeout:
        # need to break out here incase we are stuck on connecting? 
        # if we are too long, we need to click the Go back to home button.
        sleep(1)
        i+=1
    if i == 20: # we timed out and it is still connecting
        context.thisHomePage = context.thisCredentialOnTheWayPage.select_cancel()
    else:
        #assume credential added 
        context.thisCredentialAddedPage = CredentialAddedPage(context.driver)
        assert context.thisCredentialAddedPage.on_this_page()


@when('they select Done')
def step_impl(context):
    context.thisCredentialsPage = context.thisCredentialAddedPage.select_done()


@then(u'they are brought to the list of credentials')
def step_impl(context):
    context.thisCredentialsPage.on_this_page()


@then(u'the credential accepted is at the top of the list')
def step_impl(context):
    assert context.thisCredentialsPage.credential_exists(get_expected_credential_name(context))
    # TODO when testIDs are implemented on this page, get the specific data and assert
    # also check that it is at the top. 

def get_expected_credential_name(context):
    issuer_type_in_use = context.issuer.get_issuer_type()
    found = False
    for row in context.table:
        if row["issuer_agent_type"] == issuer_type_in_use:
            cred_name = row["credential_name"]
            found = True
            # get out of loop at the first found row. Can't see a reason for multiple rows of the same agent type
            break
    if found == False:
        raise Exception(
            f"No credential name in table data for {issuer_type_in_use}"
        )
    return cred_name

def get_expected_credential_detail(context):
    issuer_type_in_use = context.issuer.get_issuer_type()
    found = False
    for row in context.table:
        if row["issuer_agent_type"] == issuer_type_in_use:
            who = row["who"]
            cred_type = row["cred_type"]
            attributes = row["attributes"].split(';')
            values = row["values"].split(';')
            found = True
            # get out of loop at the first found row. Can't see a reason for multiple rows of the same agent type
            break
    if found == False:
        raise Exception(
            f"No credential details in table data for {issuer_type_in_use}"
        )
    return who, cred_type, attributes, values
