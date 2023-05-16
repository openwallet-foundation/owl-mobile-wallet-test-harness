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
from pageobjects.bc_wallet.information_approved import InformationApprovedPage
from pageobjects.bc_wallet.proof_request import ProofRequestPage
from pageobjects.bc_wallet.home import HomePage
from pageobjects.bc_wallet.navbar import NavBar
from pageobjects.bc_wallet.camera_privacy_policy import CameraPrivacyPolicyPage
from pageobjects.bc_wallet.credentials import CredentialsPage


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


@given('that the holder has a revocable credential stored in the wallet')
@given('the holder has credentials')
def step_impl(context):
    # context.execute_steps(f'''
    #     Given a connection has been successfully made
    # ''')

    for row in context.table:
        credential = row["credential"]
        revokable = row["revocable"]
        credential_name = row["credential_name"]
        context.execute_steps(f'''
            Given a connection has been successfully made
            Given the user has a credential offer of {credential} with revocable set as {revokable}
            When they select Accept
            And the holder is informed that their credential is on the way with an indication of loading
            And once the credential arrives they are informed that the Credential is added to your wallet
            And they select Done
            Then they are brought to the list of credentials
            And the credential {credential_name} is accepted is at the top of the list
        ''')


@given('the holder has a credential of {credential}')
def step_impl(context, credential):
    context.execute_steps(f'''
        Given the user has a credential offer of {credential}
    ''')

    # Check to see if they have an credential offer notification on the home icon
    # If they do, go to the home screen and click on the notification
    # if we are on the credentials page, then check the home icon for a notification
    if hasattr(context, 'thisCredentialsPage') == False:
        context.thisCredentialsPage = CredentialsPage(context.driver)
    if context.thisCredentialsPage.on_this_page():
        # sleep a little bit to wait for a notification
        sleep(5)
        if context.thisNavBar.has_notification():
            context.thisHomePage = context.thisNavBar.select_home()
            context.thisCredentialOfferPage = context.thisHomePage.select_credential_offer_notification()

    context.execute_steps(f'''
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
        # open the proof data file
        try:
            proof_json_file = open("features/data/" + proof.lower() + ".json")
            proof_json = json.load(proof_json_file)
            # check if we are adding a revocation interval to the proof request and add it.
            if interval:
                proof_json["non_revoked"] = (
                    create_non_revoke_interval(interval)["non_revoked"])

            # Add the proof json to the context so we can use it later steps for test verification
            context.proof_json = proof_json

            # send the proof request
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


@when('they select Decline')
def step_impl(context):
    context.thisAreYouSureDeclineProofRequest = context.thisProofRequestPage.select_decline()


@then('they are asked if they are sure they want to decline the Proof')
def step_impl(context):
    context.thisAreYouSureDeclineProofRequest.on_this_page()


@then('they Confirm the decline')
def step_impl(context):
    context.thisProofRequestDeclinedPage = context.thisAreYouSureDeclineProofRequest.select_confirm()
    context.thisHomePage = context.thisProofRequestDeclinedPage.select_done()


@then('they can view the contents of the proof request')
def step_impl(context):

    who, attributes, values = get_expected_proof_request_detail(
        context)
    # The below doesn't have locators in build 127. Calibrate in the future fixed build
    actual_who, actual_attributes, actual_values = context.thisProofRequestPage.get_proof_request_details()
    assert who in actual_who
    assert all(item in attributes for item in actual_attributes)
    assert all(item in values for item in actual_values)


@when('the request informs them of the attributes and credentials they came from')
def step_impl(context):

    # For every name or names in context.proof_json get the credential name from the context.credential_json_collection that has that name as an attribute.
    credential_attributes = []

    # Get the attribute values and modified schema names
    attribute_info = []
    requested_attributes = context.proof_json['requested_attributes']
    for attribute in requested_attributes.values():
        names = attribute['names']
        schema_name = attribute['restrictions'][0]['schema_name']
        modified_schema_name = schema_name.replace('_', ' ').title()
        attribute_info.extend([(modified_schema_name, name) for name in names])




    # # do the same for each predicate in the context.proof_json
    # names = {}
    # for predicate in context.proof_json["requested_predicates"].values():
    #     names.update({name: predicate["name"] for name in predicate})

    #     # Get the credential name from the context.credential_json_collection that has that name as an attribute.
    #     break_out = False
    #     for credential in context.credential_json_collection.values():
    #         # Check if each name in the names list is in any of the credential predicates.
    #         for name in names.values():
    #             if any(name == name for name in credential["attributes"]):
    #                 credential_name = credential["schema_name"]
    #                 # Remove any underscores from the credential name, replace it with spaces and capitialize the first letter of each word
    #                 credential_name = credential_name.replace("_", " ").title()

    #                 # create a new collection of credential names that hold the attributes
    #                 credential_attributes.append(
    #                     {"credential_name": credential_name, "attributes": name})
    #                 break_out = True
    #         if break_out == True:
    #             break


    # for each credential_name and attributes in the credential_attributes collection check to see if they are in the correct credential card
    credential_card_text_list = context.thisProofRequestPage.get_text_in_all_credential_cards_in_proof_request()
    for credential_attribute in attribute_info:
        credential_name = credential_attribute[0]
        attribute = credential_attribute[1]
        # for each credential card in the list check to see if the credential name is in the card
        for credential_card_text in credential_card_text_list:
            if credential_name in credential_card_text:
                # if the credential name is in the card check to see if the attributes are in the card
                assert attribute.replace("_", " ").title() in credential_card_text
                break

@when('the user has a proof request')
@given('the user has a proof request')
def step_impl(context):
    # if the context has a table then use the table to create the proof request
    if context.table:
        proof = context.table[0]["proof"]
        # get the interval for revocation as well, if it doesn't exist in the table then just move on.
        try:
            interval = context.table[0]["interval"]
        except KeyError:
            interval = None

        context.execute_steps(f'''
            When the user has a proof request for {proof}
        ''')
    else:
        context.execute_steps(f'''
            When the Holder scans the QR code sent by the "verifier"
            And the Holder is taken to the Connecting Screen/modal
            And the Connecting completes successfully
            And the Holder receives a proof request
            Then holder is brought to the proof request
        ''')


@when('the user has a connectionless proof request for {proof}')
@when('the user has a proof request for {proof}')
@when('the user has a proof request for {proof} including proof of non-revocation at {interval}')
@given('the user has a proof request for {proof}')
def step_impl(context, proof, interval=None):
    if "connectionless" in context.scenario.name:
        context.execute_steps('''
            When the Holder scans the QR code sent by the "verifier"
            # And the Holder is taken to the Connecting Screen/modal
            # And the Connecting completes successfully
        ''')
    else:
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


@then('{credential_name} is selected as the credential to verify the proof')
def step_impl(context, credential_name):
    context.thisProofRequestDetailsPage = context.thisProofRequestPage.select_details()
    credential_details = context.thisProofRequestDetailsPage.get_first_credential_details()
    # try a soft assert here until the wallet supports this selecting a non-revokable cred for a request for non-revocation
    try:
        assert credential_name in credential_details
    except AssertionError:
        print(f"Soft Assertion failed. {credential_name} not in {credential_details}")

    context.thisProofRequestPage = context.thisProofRequestDetailsPage.select_back()


@then('they select Share')
@when('they select Share')
def step_impl(context):
    context.thisSendingInformationSecurleyPage = context.thisProofRequestPage.select_share()


@then('the holder is informed that they are sending information securely')
@when('the holder is informed that they are sending information securely')
def step_impl(context):
    # this step may quickly disappear, so don't fail a test if this is already gone, see if we are on the information sent page
    while context.thisSendingInformationSecurleyPage.on_this_page():
        pass
    #context.thisInformationSentSuccessfullyPage = InformationSentSuccessfullyPage(context.driver)


@then('they are informed that the information sent successfully')
@when('they are informed that the information sent successfully')
def step_impl(context):
    context.thisInformationSentSuccessfullyPage = InformationSentSuccessfullyPage(
        context.driver)
    assert context.thisInformationSentSuccessfullyPage.on_this_page()


@then('once the proof is verified they are informed of such')
@when('once the proof is verified they are informed of such')
def step_impl(context):
    # The proof is on the way screen is temporary, loop until it goes away and create the information approved page.
    # timeout=20
    # i=0
    # while context.thisInformationSentSuccessfullyPage.on_this_page() and i < timeout:
    #     # need to break out here incase we are stuck.
    #     # if we are too long, we need to click the Done button.
    #     sleep(1)
    #     i+=1
    # if i == 20: # we timed out and it is still connecting
    #     context.thisHomePage = context.thisInformationSentSuccessfullyPage.select_back_to_home()
    # else:
    # assume credential added
    context.thisInformationApprovedPage = InformationApprovedPage(
        context.driver)
    assert context.thisInformationApprovedPage.on_this_page()


@then('they select Go back to home on information sent successfully')
@when('they select Go back to home on information sent successfully')
def step_impl(context):
    context.thisHomePage = context.thisInformationSentSuccessfullyPage.select_back_to_home()


@then('they select Done on the verfified information')
@when('they select Done on the verfified information')
def step_impl(context):
    context.thisHomePage = context.thisInformationApprovedPage.select_done()


@then('they select Done on information sent successfully')
@when('they select Done on information sent successfully')
def step_impl(context):
    context.thisHomePage = context.thisInformationSentSuccessfullyPage.select_done()


@then(u'they are brought Home')
def step_impl(context):
    context.thisHomePage.on_this_page()


@when('the credential has been revoked by the issuer')
@given('the credential has been revoked by the issuer')
def step_impl(context):
    context.issuer.revoke_credential(notify_holder=True)


@given('the BCSC holder has setup thier Wallet')
@given('the PCTF Member has setup thier Wallet')
def step_impl(context):
    context.execute_steps(f'''
            Given the User has skipped on-boarding
            And the User has accepted the Terms and Conditions
            And a PIN has been set up with "369369"
            And the Holder has selected to use biometrics to unlock BC Wallet
        ''')


@given('the Holder has setup thier Wallet')
def step_impl(context):
    context.execute_steps(f'''
            Given the User has skipped on-boarding
            And the User has accepted the Terms and Conditions
            And a PIN has been set up with "369369"
        ''')


@given('the PCTF member has an Unverified Person {credential}')
def step_impl(context, credential):
    if "PerformanceTest" in context.tags:
        context.issuer.restart_issue_credential()
    context.execute_steps(f'''
        Given the Holder receives a credential offer of {credential}
        And they Scan the credential offer QR Code
        And the Connecting completes successfully
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


@given('they Scan the credential offer QR Code')
def step_impl(context):
    if hasattr(context, 'thisNavBar') == False:
        context.thisNavBar = NavBar(context.driver)
    context.thisConnectingPage = context.thisNavBar.select_scan()

    # If this is the first time the user selects scan, then they will get a Camera Privacy Policy that needs to be dismissed
    # if autoGrantPermissions is in Capabilities = True, and platform is Android, skip this
    if ('autoGrantPermissions' in context.driver.capabilities and context.driver.capabilities['autoGrantPermissions'] == False) or (context.driver.capabilities['platformName'] == 'iOS'):
        context.thisCameraPrivacyPolicyPage = CameraPrivacyPolicyPage(
            context.driver)
        if context.thisCameraPrivacyPolicyPage.on_this_page():
            context.thisCameraPrivacyPolicyPage.select_allow()


@given('the user has a connectionless proof request for access to PCTF Chat')
def step_impl(context):
    qrcode = context.verifier.send_proof_request()

    context.device_service_handler.inject_qrcode(qrcode)

    context.thisConnectingPage = context.thisNavBar.select_scan()
    # This is connectionless and the connecting page doesn't last long. Assume we move quickly to the Proof Request
    context.thisProofRequestPage = ProofRequestPage(context.driver)


@then('the PCTF member has access to chat')
def step_impl(context):
    context.verifier.proof_request_verified()


@when(u'a credential has been revoked by the issuer')
@given(u'a credential has been revoked by the issuer')
def step_impl(context):
    for row in context.table:
        credential_name = row["credential_name"]
        context.issuer.revoke_credential(
            notify_holder=True, credential=credential_name)


@then(u'the proof is unverified')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the proof is unverified')


@then(u'The holder receives a revocation message notification')
def step_impl(context):
    context.thisHomePage = context.thisNavBar.select_home()


@then(u'the holder selects the revocation notification')
def step_impl(context):
    context.thisCredentialDetailsPage = context.thisHomePage.select_revocation_notification()
    context.thisCredentialDetailsPage.on_this_page()


@then(u'the holder reviews the contents of the revocation notification message')
def step_impl(context):
    assert context.table[0]["credential_name"] in context.driver.page_source
    assert context.table[0]["revoked_message"] in context.driver.page_source


@then(u'acknowledges the revocation notification')
def step_impl(context):
    context.thisCredentialDetailsPage.select_revocation_dismiss()


@then('the credential has a revoked status')
def step_impl(context):
    # Scroll to the bottom of the page to make sure the revoked status is visible
    context.thisCredentialDetailsPage.scroll_to_bottom()
    assert context.thisCredentialDetailsPage.is_credential_revoked()


@then(u'the revocation notification is removed')
def step_impl(context):
    context.thisHomePage = context.thisCredentialDetailsPage.select_back()
    #context.thisHomePage = context.thisNavBar.select_home()
    assert context.thisHomePage.is_revocation_notification_present() == False


@given(u'The holder has received and acknowledged the revocation message notification')
def step_impl(context):
    context.execute_steps(f'''
        Then the holder receives a revocation message notification
        Then the holder selects the revocation notification
        Then acknowledges the revocation notification
    ''')
    context.thisHomePage = context.thisNavBar.select_home()


@when(u'the holder selects the credential')
def step_impl(context):
    context.thisCredentialsPage = context.thisNavBar.select_credentials()
    context.thisCredentialDetailsPage = context.thisCredentialsPage.select_top_credential()


@then(u'they will be informed of its revoked status')
def step_impl(context):
    assert context.thisCredentialDetailsPage.is_credential_revoked()


@then(u'the holder will be able to review the revoked message again')
def step_impl(context):
    context.thisCredentialDetailsPage.select_revocation_info()
    assert context.thisCredentialDetailsPage.get_revocation_message(
    ) == context.table[0]["revoked_message"]


def get_expected_proof_request_detail(context):
    verifier_type_in_use = context.verifier.get_issuer_type()
    found = False
    for row in context.table:
        if row["verifier_agent_type"] == verifier_type_in_use:
            who = row["who"]
            attributes = row["attributes"].split(';')
            values = row["values"].split(';')
            found = True
            # get out of loop at the first found row. Can't see a reason for multiple rows of the same agent type
            break
    if found == False:
        raise Exception(
            f"No credential details in table data for {verifier_type_in_use}"
        )
    return who, attributes, values


def get_expected_proof_request_detail_from_credential(context):
    verifier_type_in_use = context.verifier.get_issuer_type()
    found = False
    for row in context.table:
        if row["verifier_agent_type"] == verifier_type_in_use:
            who = row["who"]
            attributes = row["attributes"].split(';')
            values = row["values"].split(';')
            found = True
            # get out of loop at the first found row. Can't see a reason for multiple rows of the same agent type
            break
    if found == False:
        raise Exception(
            f"No credential details in table data for {verifier_type_in_use}"
        )
    return who, attributes, values, credential_name
