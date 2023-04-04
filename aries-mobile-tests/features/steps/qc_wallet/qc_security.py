from bc_wallet.security import *
from pageobjects.bc_wallet.onboarding_biometrics import OnboardingBiometricsPage
from override_steps import overrides

@then('they select visibility toggle on the first PIN as "{pin}"')
def step_impl(context, pin):
    assert pin == context.thisPINSetupPage.get_pin()

@then('they select visibility toggle on the second PIN as "{pin}"')
def step_impl(context, pin):
    assert pin == context.thisPINSetupPage.get_second_pin()

@overrides('the User selects Create PIN', 'when')
def special_step_impl(context):
    next_page = context.thisPINSetupPage.create_pin()
    if type(next_page) == OnboardingBiometricsPage: 
        context.thisOnboardingBiometricsPage.on_this_page()

@then('they select ok on PINs error')
def step_impl(context):
    context.thisPINSetupPage.select_ok_on_modal()
