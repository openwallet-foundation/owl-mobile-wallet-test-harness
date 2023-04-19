from bc_wallet.proof import *
from override_steps import overrides

@overrides('they can view the contents of the proof request', 'then')
def step_impl(context):
    assert context.thisProofRequestPage.on_this_page()
    # who, attributes, values=get_expected_proof_request_detail(
    #     context)
    # # The below doesn't have locators in build 127. Calibrate in the future fixed build
    # actual_who, actual_attributes, actual_values = context.thisProofRequestPage.get_proof_request_details()
    # assert who in actual_who
    # assert all(item in attributes for item in actual_attributes)
    # assert all(item in values for item in actual_values)
