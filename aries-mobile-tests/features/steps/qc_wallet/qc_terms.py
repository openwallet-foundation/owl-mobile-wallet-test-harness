from bc_wallet.terms import *
from override_steps import overrides


@overrides('the users accepts the Terms and Conditions', 'given')
@overrides('the users accepts the Terms and Conditions', 'when')
def accept_terms_step_impl(context):
    context.thisTermsAndConditionsPage.select_accept()
# commit