# -----------------------------------------------------------
# Behave Step Definitions for a proof request to a wallet user
#
# -----------------------------------------------------------

from behave import given, when, then

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation, table_to_str, create_non_revoke_interval
# import Page Objects needed


@given('the BCSC holder has a {credential}')
def step_impl(context, credential):
    context.execute_steps(f'''
        Given the BCVC Issuer sends a BC VC Pilot Certificate
        And the BCSC holder opened thier email and clicked the invite link
        And the BCSC holder checked agree and selected agree #(has to be on a device that has access to bcvc pilot)
        And the BCSC holder selected Request Credential
        And the BCSC holder selected I confirm and agree
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

@given('the BCVC Issuer sends a BC VC Pilot Certificate')
def step_impl(context):
    context.issuer.send_credential()
    # And the Issuer selects New Invite
    # And the issuer fills out email, name, and program of IDIM Testing
    # And the issuer clicks invite
    
@given('the BCSC holder opened thier email and clicked the invite link')
def step_impl(context):
    context.holderGmailInterface.open_invitation_email()
    context.thisBCVCInvitationPage = context.holderGmailInterface.select_invitation_link()
    assert context.thisBCVCInvitationPage.on_this_page()

@given('the BCSC holder checked agree and selected agree')
def step_impl(context):
    context.thisBCVCInvitationPage.check_agree()
    context.thisBCVCRequestCredentialPage = context.thisBCVCInvitationPage.select_agree()
    assert context.thisBCVCRequestCredentialPage.on_this_page()

@given('the BCSC holder selected I confirm and agree')
def step_impl(context):
    context.thisBCVCRequestCredentialPage.check_confirm()
    context.thisBCVCQRCodePage = context.thisBCVCRequestCredentialPage.select_agree()
    assert context.thisBCVCQRCodePage.on_this_page()