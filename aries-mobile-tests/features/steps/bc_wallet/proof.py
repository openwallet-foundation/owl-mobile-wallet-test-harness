# -----------------------------------------------------------
# Behave Step Definitions for a proof request to a wallet user
#
# -----------------------------------------------------------

from behave import given, when, then
import json
from time import sleep

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation, table_to_str, create_non_revoke_interval
# import Page Objects needed
# from pageobjects.bc_wallet.credential_offer_notification import CredentialOfferNotificationPage
from pageobjects.bc_wallet.information_sent_successfully import InformationSentSuccessfullyPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from pageobjects.bc_wallet.home import HomePage


@given('the holder has a Non-Revocable credential')
def step_impl(context):
    context.execute_steps(u'''
        Given the user has a credential offer
        When they select Accept
        And the holder is informed that their credential is on the way with an indication of loading
        And once the credential arrives they are informed that the Credential is added to your wallet
        And they select Done
        Then they are brought to the list of credentials
        And the credential accepted is at the top of the list
        {table}
    '''.format(table=table_to_str(context.table)))

@given('the holder has a credential of {credential}')
def step_impl(context, credential):
    context.execute_steps(f'''
        Given the user has a credential offer of {credential}
        When they select Accept
        And the holder is informed that their credential is on the way with an indication of loading
        And once the credential arrives they are informed that the Credential is added to your wallet
        And they select Done
        Then they are brought to the list of credentials
    ''')

@given('the holder has another credential of {credential_2}')
def step_impl(context, credential_2):
    context.execute_steps(f'''
        Given a connection has been successfully made
        Given the holder has a credential of {credential_2}
    ''')

@when('the Holder receives a proof of non-revocation with {proof} at {interval}')
@when('the Holder receives a proof request of {proof}')
@when('the Holder receives a proof request')
def step_impl(context, proof=None, interval=None):
    # Make sure the connection is successful first.
    context.execute_steps('''
        Then there is a connection between "verifier" and Holder
    ''')

    if proof is None:
        context.verifier.send_proof_request()
    else:
        #open the proof data file
        try:
            proof_json_file = open("features/data/" + proof.lower() + ".json")
            proof_json = json.load(proof_json_file)
            # check if we are adding a revocation interval to the proof request and add it.
            if interval:
                proof_json["non_revoked"] = (create_non_revoke_interval(interval)["non_revoked"])
            context.verifier.send_proof_request(request_for_proof=proof_json)
        except FileNotFoundError:
            print("FileNotFoundError: features/data/" + proof.lower() + ".json")


@then('holder is brought to the proof request')
def step_impl(context):

    context.thisProofRequestPage = ProofRequestPage(context.driver)
    assert context.thisProofRequestPage.on_this_page()

@then('they can only select Decline')
def step_impl(context):
    context.thisAreYouSureDeclineProofRequest = context.thisProofRequestPage.select_decline()

@then('they are asked if they are sure they want to decline the Proof')
def step_impl(context):
    context.thisAreYouSureDeclineProofRequest.on_this_page()

@then('they Confirm the decline')
def step_impl(context):
    context.thisHomePage = context.thisAreYouSureDeclineProofRequest.select_confirm()

@then('they can view the contents of the proof request')
def step_impl(context):

    who, attributes, values=get_expected_proof_request_detail(
        context)
    # The below doesn't have locators in build 127. Calibrate in the future fixed build
    actual_who, actual_attributes, actual_values = context.thisProofRequestPage.get_proof_request_details()
    assert who in actual_who
    assert all(item in attributes for item in actual_attributes)
    assert all(item in values for item in actual_values)


@given('the user has a proof request')
def step_impl(context):
    context.execute_steps(f'''
        When the Holder scans the QR code sent by the "verifier"
        And the Holder is taken to the Connecting Screen/modal
        And the Connecting completes successfully
        And the Holder receives a proof request
        Then holder is brought to the proof request
    ''')

@when('the user has a proof request for {proof}')
@when('the user has a proof request for {proof} including proof of non-revocation at {interval}')
@given('the user has a proof request for {proof}')
def step_impl(context, proof, interval=None):
    context.execute_steps('''
        When the Holder scans the QR code sent by the "verifier"
        And the Holder is taken to the Connecting Screen/modal
        And the Connecting completes successfully
    ''')

    if interval:
        context.execute_steps(f'''
            When the Holder receives a proof of non-revocation with {proof} at {interval}
        ''')
    else:
        context.execute_steps(f'''
            When the Holder receives a proof request of {proof}
        ''')        

    context.execute_steps('''
        Then holder is brought to the proof request
    ''')


@then('<credential_name> is selected as the credential to verify the proof')
def step_impl(context, credential_name):
    context.thisProofRequestDetailsPage = context.thisProofRequestPage.select_details()
    credential_details = context.thisProofRequestDetailsPage.get_first_credential_details()
    assert credential_name in credential_details
    context.thisProofRequestPage = context.thisProofRequestDetailsPage.select_back()


@then('they select Share')
@when('they select Share')
def step_impl(context):
    context.thisSendingInformationSecurleyPage = context.thisProofRequestPage.select_share()

@then('the holder is informed that they are sending information securely')
@when('the holder is informed that they are sending information securely')
def step_impl(context):
    assert context.thisSendingInformationSecurleyPage.on_this_page()


@then('once the proof is verified they are informed of such')
@when('once the proof is verified they are informed of such')
def step_impl(context):
    # The Cred is on the way screen is temporary, loop until it goes away and create the cred added page.
    timeout=20
    i=0
    while context.thisSendingInformationSecurleyPage.on_this_page() and i < timeout:
        # need to break out here incase we are stuck on connecting?
        # if we are too long, we need to click the Go back to home button.
        sleep(1)
        i+=1
    if i == 20: # we timed out and it is still connecting
        context.thisHomePage = context.thisSendingInformationSecurleyPage.select_back_to_home()
    else:
        #assume credential added
        context.thisInformationSentSuccessfullyPage = InformationSentSuccessfullyPage(context.driver)
        assert context.thisInformationSentSuccessfullyPage.on_this_page()

@then('they select Done on the verfified information')
@when('they select Done on the verfified information')
def step_impl(context):
    context.thisHomePage = context.thisInformationSentSuccessfullyPage.select_done()


@then(u'they are brought Home')
def step_impl(context):
    context.thisHomePage.on_this_page()


@given('the credential has been revoked by the issuer')
def step_impl(context):
    context.issuer.revoke_credential()


def get_expected_proof_request_detail(context):
    verifier_type_in_use=context.verifier.get_issuer_type()
    found=False
    for row in context.table:
        if row["verifier_agent_type"] == verifier_type_in_use:
            who=row["who"]
            attributes=row["attributes"].split(';')
            values=row["values"].split(';')
            found=True
            # get out of loop at the first found row. Can't see a reason for multiple rows of the same agent type
            break
    if found == False:
        raise Exception(
            f"No credential details in table data for {verifier_type_in_use}"
        )
    return who, attributes, values
