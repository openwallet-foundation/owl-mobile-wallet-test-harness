# -----------------------------------------------------------
# Behave Step Definitions for a proof request to a wallet user
#
# -----------------------------------------------------------

from time import sleep
from behave import given, when, then
from decouple import config
from steps.bc_wallet.credential_offer import get_expected_credential_name

# Local Imports
from agent_controller_client import agent_controller_GET, agent_controller_POST, expected_agent_state, setup_already_connected
from agent_test_utils import get_qr_code_from_invitation, table_to_str, create_non_revoke_interval
# import Page Objects needed
from pageobjects.bc_wallet.holder_get_invite_interface.bc_vp_holder_get_invite_interface import BCVPHolderGetInviteInterface
from pageobjects.bc_wallet.create_bc_digital_id import CreateABCDigitalIDPage


@when('the Student has credentials')
def step_impl(context):

    for row in context.table:
        credential_name = row["credential_name"]
        qrcode = context.issuer.send_credential(actor=context.actor, schema=credential_name)
        context.device_service_handler.inject_qrcode(qrcode)
        context.execute_steps('''
            Given they Scan the credential offer QR Code
            When the holder opens the credential offer
            Then holder is brought to the credential offer screen
            When they select Accept
            And the holder is informed that their credential is on the way with an indication of loading
            And once the credential arrives they are informed that the Credential is added to your wallet
            And they select Done
            Then they are brought to the list of credentials
        ''')


@when('the Student has a proof request')
def step_impl(context):

    for row in context.table:
        proof_request_name = row["proof_request"]
        qrcode = context.verifier.send_proof_request(actor=context.actor, proof=proof_request_name)
        context.device_service_handler.inject_qrcode(qrcode)
        context.execute_steps('''
            Given they Scan the proof request QR Code
            When the holder opens the proof request
            Then holder is brought to the proof request
        ''')

        # And they select Share
        # And the holder is informed that they are sending information securely
        # Then they are informed that the information sent successfully

@then('they have Access')
def step_impl(context):
    for row in context.table:
        proof_result = row["proof_result"]
        assert context.verifier.proof_success(proof_result)