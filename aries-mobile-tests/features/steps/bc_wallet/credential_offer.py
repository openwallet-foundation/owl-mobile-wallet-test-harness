# -----------------------------------------------------------
# Behave Step Definitions for an issuer offering a credential to a wallet user
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
from pageobjects.bc_wallet.credential_offer import CredentialOfferPage
from pageobjects.bc_wallet.credential_added import CredentialAddedPage
from pageobjects.bc_wallet.home import HomePage


@given('a connection has been successfully made')
def step_impl(context):
    context.execute_steps('''
        When the Holder scans the QR code sent by the "issuer"
        And the Holder is taken to the Connecting Screen/modal
        And the Connecting completes successfully
        Then there is a connection between "issuer" and Holder
    ''')


@when('the Holder receives a Non-Revocable credential offer')
def step_impl(context):
    context.issuer.send_credential()

    assert context.thisConnectingPage.wait_for_connection()
    # context.thisCredentialOfferNotificationPage = CredentialOfferNotificationPage(context.driver)
    # assert context.thisCredentialOfferNotificationPage.on_this_page()



@given('the Holder receives a credential offer of {credential}')
@when('the Holder receives a credential offer of {credential}')
@when('the Holder receives a credential offer of {credential} with revocable set as {revocation}') 
def step_impl(context, credential, revocation=None):
    # Open cred data file
    try:
        credential_json_file = open(
            "features/data/" + credential.lower() + ".json")
        credential_json = json.load(credential_json_file)

        # add the credential json to a collection on the context so that it can be used in other steps
        if hasattr(context, 'credential_json_collection') == False:
            context.credential_json_collection = {}
        context.credential_json_collection[credential] = credential_json

        # add others here as they come up that may need a schema and cred def.
        if context.issuer.get_issuer_type() == "AATHIssuer":
            # get schema name from cred data
            cred_type = credential_json['schema_name']
            # open schema file
            try:
                cred_type_json_file = open(
                    f"features/data/schema_{cred_type.lower()}.json")
                cred_type_json = json.load(cred_type_json_file)
                # check if the credential is revokable
                if revocation == None:
                    if "support_revocation" in cred_type_json and cred_type_json["support_revocation"] == True:
                        rev = True
                    else:
                        rev = False
                else:
                    if revocation == "True":
                        rev = True
                    else:
                        rev = False
                context.issuer.send_credential(
                    schema=cred_type_json, credential_offer=credential_json, revokable=rev)
            except FileNotFoundError:
                print(
                    f"FileNotFoundError: features/data/schema_{cred_type.lower()}.json")
        else:
            if "Connectionless" in context.tags:
                # We are expecting a QR code on the send credential if connectionless
                qrimage = context.issuer.send_credential(
                    credential_offer=credential_json)
                context.device_service_handler.inject_qrcode(qrimage)
            else:
                context.issuer.send_credential(
                    credential_offer=credential_json)

    except FileNotFoundError:
        print("FileNotFoundError: features/data/" +
              credential.lower() + ".json")


@when('the Holder taps on the credential offer notification')
def step_impl(context):
    context.thisCredentialOfferPage = context.thisHomePage.select_credential_offer_notification()
    #context.thisCredentialOfferPage = context.thisCredentialOfferNotificationPage.select_credential()


@then('holder is brought to the credential offer screen')
def step_impl(context):
    # Workaround for bug 645
    context.execute_steps(f'''
        When the connection takes too long reopen app and select notification
    ''')

    #assert context.thisConnectingPage.wait_for_connection()

    context.thisCredentialOfferPage = CredentialOfferPage(context.driver)
    assert context.thisCredentialOfferPage.on_this_page()


@when('the connection takes too long reopen app and select notification')
def step_impl(context):
    # Workaround for bug 645
    if "Workaround645" in context.tags:
        if context.thisConnectingPage.is_connecting_taking_too_long():
            context.thisHomePage = context.thisConnectingPage.select_go_back_to_home()
            context.execute_steps(f'''
                When they have closed the app
                When they relaunch the app
                When authenticates with thier biometrics
            ''')
            # Check for the notification on the Home Page
            context.thisHomePage.select_credential_offer_notification()


@then('they can view the contents of the credential')
def step_impl(context):
    assert context.thisCredentialOfferPage.on_this_page()

    who, cred_type, attributes, values = get_expected_credential_detail(
        context)
    # TODO The below doesn't have locators in build 127. Calibrate in the future fixed build
    #actual_who, actual_cred_type, actual_attributes, actual_values = context.thisCredentialOfferPage.get_credential_details()
    #assert who in actual_who
    #assert cred_type in actual_cred_type
    #assert attributes in actual_attributes
    #assert values in actual_values


@given('the user has a credential offer')
def step_impl(context):
    context.execute_steps(f'''
        When the Holder receives a Non-Revocable credential offer
        Then holder is brought to the credential offer screen
    ''')



@given('the user has a credential offer of {credential}')
@given('the user has a credential offer of {credential} with revocable set as {revocation}')
def step_impl(context, credential, revocation=None):
    if revocation == None:
        context.execute_steps(f'''
            When the Holder receives a credential offer of {credential}
        ''')
    else:
        context.execute_steps(f'''
            When the Holder receives a credential offer of {credential} with revocable set as {revocation}
        ''')

    context.execute_steps(f'''
            Then holder is brought to the credential offer screen
        ''')


@then('they select Accept')
@when('they select Accept')
def step_impl(context):
    context.thisCredentialOnTheWayPage = context.thisCredentialOfferPage.select_accept(
        scroll=True)

@given('the holder declines the credential offer')
def step_impl(context):
    context.thisDeclineCredentialOffer = context.thisCredentialOfferPage.select_decline(
        scroll=True)
    context.thisHomePage = context.thisDeclineCredentialOffer.select_decline()

@then('the holder is informed that their credential is on the way with an indication of loading')
@when('the holder is informed that their credential is on the way with an indication of loading')
def step_impl(context):
    # sometimes the workflow is farther ahead than the test thinks it is, so put in a soft assert here.
    if context.thisCredentialOnTheWayPage.on_this_page():
        assert True
    else:
        pass


@then('once the credential arrives they are informed that the Credential is added to your wallet')
@when('once the credential arrives they are informed that the Credential is added to your wallet')
def step_impl(context):
    try:
        context.thisCredentialAddedPage = context.thisCredentialOnTheWayPage.wait_for_credential()
        assert context.thisCredentialAddedPage.on_this_page()
    except:
        context.thisHomePage = context.thisCredentialOnTheWayPage.select_home()


@then('they select Done')
@when('they select Done')
def step_impl(context):
    # TODO we could be on the home page at this point. Should we fail the last step, fail this one, or try the cred accept again?
    if hasattr(context, 'thisCredentialsPage') == False:
        # This means we probably went to the Home Page above. Revisit this if the this happens too much.
        context.thisCredentialAddedPage = CredentialAddedPage(context.driver)
    context.thisCredentialsPage = context.thisCredentialAddedPage.select_done()


@then(u'they are brought to the list of credentials')
def step_impl(context):
    context.thisCredentialsPage.on_this_page()


@then(u'the credential {credential_name} is accepted is at the top of the list')
@then(u'the IDIM Person credential accepted is at the top of the list')
@then(u'the credential accepted is at the top of the list')
def step_impl(context, credential_name=None):
    # if the platform is iOS 15+ or android 
    if (context.driver.capabilities['platformName'] and context.driver.capabilities['platformVersion'] >= '15') or context.driver.capabilities['platformName'] == "Android":
        json_elems = context.thisCredentialsPage.get_credentials()
        if credential_name == None:
            credential_name = get_expected_credential_name(context)

        assert credential_name in json_elems["credentials"][0]["text"]
    else:
        if credential_name == None:
            credential_name = get_expected_credential_name(context)
        assert context.thisCredentialsPage.credential_exists(credential_name)


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
