from bc_wallet.terms import *
from override_steps import overrides
from pageobjects.qc_wallet.termsandconditions import TermsAndConditionsPageQC
from pageobjects.qc_wallet.pinsetup import PINSetupPageQC


@overrides("the users accepts the Terms and Conditions", "given")
@overrides("the users accepts the Terms and Conditions", "when")
def accept_terms_step_impl(context):
    context.thisTermsAndConditionsPageQC.select_accept()

@overrides('the User is on the Terms and Conditions screen', "given")
@then("the User is on the Terms and Conditions screen")
def step_impl(context):
        context.thisTermsAndConditionsPageQC = TermsAndConditionsPageQC(context.driver)
        assert context.thisTermsAndConditionsPageQC.on_this_page()

@overrides('the user clicks continue', "given")
@overrides('the user clicks continue', "when")
def step_impl(context):
    context.thisTermsAndConditionsPageQC.select_continue()


@overrides('the User is on the PIN creation screen', "given")
@overrides('the user transitions to the PIN creation screen', "then")
def step_impl(context):
    context.thisPINSetupPageQC = PINSetupPageQC(context.driver)
    context.thisPINSetupPageQC.on_this_page()

@when("the user clicks continue without accepting the Terms and Conditions")
def step_impl(context):
    context.thisTermsAndConditionsPageQC.select_continue()

