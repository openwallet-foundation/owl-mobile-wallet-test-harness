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
from pageobjects.bc_wallet.home import HomePage


@given('a connection has been successfully made')
def step_impl(context):
    context.execute_steps(f'''
        When the Holder scans the QR code sent by the issuer
        And the Holder is taken to the Connecting Screen/modal
        And the Connecting completes successfully
        Then there is a connection between Issuer and Holder
    ''')


@when('the Holder receives a Non-Revocable credential offer')
def step_impl(context):
    context.issuer.send_credential()

    # context.thisCredentialOfferNotificationPage = CredentialOfferNotificationPage(context.driver)
    # assert context.thisCredentialOfferNotificationPage.on_this_page()


@when('the Holder taps on the credential offer notification')
def step_impl(context):
    # The connecting screen is temporary.
    # What if the connecting screen goes away too fast before this next line runs? Maybe check at home? Let the page object do it?
    context.thisCredentialOfferPage = context.thisHomePage.select_credential_offer_notification()
    #context.thisCredentialOfferPage = context.thisCredentialOfferNotificationPage.select_credential()


@then('holder is brought to the credential offer screen')
def step_impl(context):
    assert context.thisCredentialOfferPage.on_this_page()


@then('they can view the contents of the credential')
def step_impl(context):
    assert context.thisCredentialOfferPage.on_this_page()

    who, cred_type, attributes, values = get_expected_credential_detail(context)
    actual_who, actual_cred_type, actual_attributes, actual_values = context.thisCredentialOfferPage.get_credential_details()
    assert who in actual_who
    assert cred_type in actual_cred_type
    assert attributes in actual_attributes
    assert values in actual_values


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
